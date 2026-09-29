"""Engine CLI."""
from __future__ import annotations
import sys
from datetime import date
from pathlib import Path
import click
from engine.workspace import Workspace
from engine.artifact_graph import ArtifactGraph
from engine.findings import FindingCollection
from engine.gates.base import GateRegistry
from engine.checks.markers import NoUnresolvedFailMarkersGate
from engine.waivers import WaiverError, WaiverRegister, validate_scope
from engine.reporters.markdown import render_markdown
from engine.reporters.junit import render_junit
from engine.reporters.sarif import render_sarif

def _default_registry() -> GateRegistry:
    from engine.gates.phase01 import Phase01Gate
    from engine.gates.phase02 import Phase02Gate
    from engine.gates.phase03 import Phase03Gate
    from engine.gates.phase04 import Phase04Gate
    from engine.gates.phase05 import Phase05Gate
    from engine.gates.phase06 import Phase06Gate
    from engine.gates.phase07 import Phase07Gate
    from engine.gates.phase08 import Phase08Gate
    from engine.gates.phase09 import Phase09Gate
    reg = GateRegistry()
    reg.register(NoUnresolvedFailMarkersGate())
    from engine.checks.generation_staleness import GenerationStalenessGate
    reg.register(GenerationStalenessGate())  # M10-08-T06: report-only (MEDIUM/INFO)
    reg.register(Phase01Gate())
    reg.register(Phase02Gate())
    reg.register(Phase03Gate())
    reg.register(Phase04Gate())
    reg.register(Phase05Gate())
    reg.register(Phase06Gate())
    reg.register(Phase07Gate())
    reg.register(Phase08Gate())
    reg.register(Phase09Gate())
    return reg

@click.group()
def main() -> None:
    """srs-skills validation kernel."""

@main.command()
def doctor() -> None:
    """Run pre-flight diagnostics."""
    from engine.doctor import run
    sys.exit(run())


@main.command("new-project")
@click.argument("name")
@click.option("--methodology", type=click.Choice(["waterfall", "agile", "hybrid"]), required=True)
@click.option("--domain", required=True)
@click.option("--example", default=None, help="Optional example name under examples/")
def new_project(name: str, methodology: str, domain: str, example: str | None) -> None:
    """Scaffold a new project workspace under projects/<name>/."""
    from engine.scaffold import scaffold
    scaffold(Path("projects") / name, methodology, domain, example)
    click.echo(f"Scaffolded projects/{name}.")


@main.command()
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.option("--junit", type=click.Path(), default=None)
@click.option("--sarif", type=click.Path(), default=None)
@click.option("--markdown", "md_path", type=click.Path(), default=None)
@click.option("--break-something", is_flag=True, hidden=True,
              help="Inject synthetic findings (used by demo CI to prove gates can fail).")
def validate(project: str, junit: str | None, sarif: str | None,
             md_path: str | None, break_something: bool) -> None:
    """Validate a project workspace and exit non-zero on blocking findings."""
    workspace = Workspace.load(Path(project))
    graph = ArtifactGraph.build(workspace)
    findings = FindingCollection()
    _default_registry().run_all(graph, findings)
    from engine.gates.hybrid import HybridSyncGate
    HybridSyncGate(workspace.root).evaluate(graph, findings)
    waivers = WaiverRegister.load(workspace.root / "_registry" / "waivers.yaml")
    waived, remaining_list = waivers.apply(findings, today=date.today())
    remaining = FindingCollection()
    remaining.extend(remaining_list)
    if break_something:
        from engine.findings import Finding, Severity
        for gate_id in (
            "kernel.no_unresolved_fail_markers",
            "phase02.smart_nfr",
            "phase09.traceability",
        ):
            remaining.add(Finding(
                gate_id=gate_id,
                severity=Severity.HIGH,
                message="synthetic finding (--break-something)",
                location=None, line=None,
            ))
    md = render_markdown(remaining, waived, project=workspace.root.name)
    if md_path:
        Path(md_path).write_text(md, encoding="utf-8")
    if junit:
        Path(junit).write_text(render_junit(remaining), encoding="utf-8")
    if sarif:
        Path(sarif).write_text(render_sarif(remaining), encoding="utf-8")
    if remaining.is_blocking:
        click.echo("ENGINE CONTRACT: FAIL")
        for f in remaining:
            click.echo(f"- [{f.severity.name}] {f.gate_id}: {f.message}")
        sys.exit(1)
    click.echo("ENGINE CONTRACT: PASS")

@main.command()
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.option("--identifiers-only", is_flag=True,
              help="Write _registry/identifiers.yaml only; leave the glossary registry untouched.")
def sync(project: str, identifiers_only: bool) -> None:
    """Populate _registry/identifiers.yaml and _registry/glossary.yaml.

    Use --identifiers-only for projects whose glossary registry is deliberately
    absent (e.g. docs that embed many code-identifier tokens the glossary scan
    would otherwise demand as terms).
    """
    from engine.sync import sync as do_sync
    ws = Workspace.load(Path(project))
    ids, gloss, errors = do_sync(ws)
    if errors:
        for e in errors:
            click.echo(e)
        sys.exit(1)
    reg_dir = ws.root / "_registry"
    reg_dir.mkdir(exist_ok=True)
    ids.save(reg_dir / "identifiers.yaml")
    if identifiers_only:
        click.echo(f"Wrote {len(ids)} identifiers (glossary left untouched).")
    else:
        gloss.save(reg_dir / "glossary.yaml")
        click.echo(f"Wrote {len(ids)} identifiers and {len(gloss)} glossary terms.")

@main.command("validate-skills")
def validate_skills() -> None:
    """Scan skill files for legacy path references."""
    from engine.checks.legacy_paths import LegacyPathCheck
    findings = FindingCollection()
    chk = LegacyPathCheck()
    for d in ["00-meta-initialization", "01-strategic-vision", "02-requirements-engineering",
              "03-design-documentation", "04-development-artifacts", "05-testing-documentation",
              "06-deployment-operations", "07-agile-artifacts", "08-end-user-documentation",
              "09-governance-compliance"]:
        for p in Path(d).rglob("*.md"):
            chk.scan_file(p, findings)
    if findings.is_blocking:
        for f in findings:
            click.echo(f"- {f.location}:{f.line} {f.message}")
        sys.exit(1)
    click.echo("SKILLS OK: no legacy path references outside alias-blocks.")

@main.group()
def baseline() -> None:
    """Baseline snapshot / diff commands."""


@baseline.command("snapshot")
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.option("--label", required=True)
def baseline_snapshot(project: str, label: str) -> None:
    """Snapshot current identifier hashes under the project's baseline-delta dir."""
    from engine.baseline import snapshot, save_snapshot
    ws = Workspace.load(Path(project))
    graph = ArtifactGraph.build(ws)
    snap = snapshot(graph, label=label)
    out_dir = ws.root / "09-governance-compliance" / "07-baseline-delta"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{label}.yaml"
    save_snapshot(snap, out)
    click.echo(
        f"Wrote baseline {label} with {len(snap.entries)} entries to {out}"
    )


@baseline.command("diff")
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.argument("old_label")
@click.argument("new_label")
def baseline_diff(project: str, old_label: str, new_label: str) -> None:
    """Print added, removed, and modified identifiers between two baselines."""
    from engine.baseline import load_snapshot, diff
    base = Path(project) / "09-governance-compliance" / "07-baseline-delta"
    old = load_snapshot(base / f"{old_label}.yaml")
    new = load_snapshot(base / f"{new_label}.yaml")
    d = diff(old, new)
    click.echo(f"Added: {len(d['added'])}")
    for x in d["added"]:
        click.echo(f"  + {x}")
    click.echo(f"Removed: {len(d['removed'])}")
    for x in d["removed"]:
        click.echo(f"  - {x}")
    click.echo(f"Modified: {len(d['modified'])}")
    for x in d["modified"]:
        click.echo(f"  ~ {x}")
    dd = d["diagram"]
    if any(dd.values()):
        click.echo("Diagram elements (reports what changed; infers no impact or risk):")
        for key, sign in (("added", "+"), ("removed", "-"), ("changed", "~"), ("moved", ">")):
            click.echo(f"  {key.capitalize()}: {len(dd[key])}")
            for x in dd[key]:
                click.echo(f"    {sign} {x}")


@main.group()
def diagrams() -> None:
    """Diagram IR commands: validate, generate, manifest, verify-manifest (M10-07)."""


def _doc_filter(project: Path, doc: str | None):
    if doc is None:
        return None
    d = Path(doc)
    return (d if d.is_absolute() else (Path.cwd() / d)).resolve()


def _echo_diagnostic(d, root: Path) -> None:
    where = ""
    if d.path is not None:
        try:
            where = d.path.resolve().relative_to(root).as_posix()
        except ValueError:
            where = str(d.path)
    ptr = d.subject.get("path", "") if d.subject else ""
    click.echo(f"- [{d.severity.name}] {d.code} {where}{(' ' + ptr) if ptr else ''}: {d.message}")
    for fix in d.supported_fixes:
        click.echo(f"    fix: {fix}")


@diagrams.command("validate")
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.option("--doc", default=None, help="Limit to one document directory.")
@click.option("--json", "json_path", type=click.Path(), default=None,
              help="Also write the diagnostics as JSON.")
def diagrams_validate(project: str, doc: str | None, json_path: str | None) -> None:
    """Validate diagram IR and record the accepted candidates."""
    import json as _json
    from engine.checks.diagram_trace import DiagramTraceCheck
    from engine.diagram_ir import ir_files_by_doc, load_doc_irs, write_validated
    from engine.findings import Severity
    ws = Workspace.load(Path(project))
    root = ws.root
    groups = ir_files_by_doc(root)
    only = _doc_filter(root, doc)
    if only is not None:
        groups = {k: v for k, v in groups.items() if k.resolve() == only}
    if not groups:
        click.echo("No diagram IR found (expected <doc-dir>/diagrams/*.ir.json).")
        sys.exit(2)
    graph = ArtifactGraph.build(ws)
    diags = DiagramTraceCheck("phase03.diagram_trace", root).diagnostics(graph)
    doc_dirs = {k.resolve() for k in groups}
    reported = [d for d in diags
                if d.path is None or d.path.resolve().parent.parent in doc_dirs]
    blocking_paths = {d.path.resolve() for d in reported
                      if d.path is not None and d.severity >= Severity.HIGH}
    for d in reported:
        _echo_diagnostic(d, root)
    frozen = 0
    for doc_dir in sorted(groups):
        irs, load_diags = load_doc_irs(doc_dir)
        if load_diags or any(ir.path.resolve() in blocking_paths for ir in irs):
            click.echo(f"NOT VALIDATED: {doc_dir.relative_to(root).as_posix()}")
            continue
        write_validated(doc_dir, irs)
        frozen += len(irs)
        click.echo(f"VALIDATED: {doc_dir.relative_to(root).as_posix()} ({len(irs)} figure(s))")
    if json_path:
        Path(json_path).write_text(_json.dumps([
            {"code": d.code, "severity": d.severity.name, "message": d.message,
             "subject": d.subject, "evidence": d.evidence,
             "supported_fixes": list(d.supported_fixes)} for d in reported], indent=2),
            encoding="utf-8")
    if any(d.severity >= Severity.HIGH for d in reported):
        click.echo("DIAGRAMS: FAIL")
        sys.exit(1)
    click.echo(f"DIAGRAMS: PASS ({frozen} figure(s) validated)")


@diagrams.command("generate")
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.option("--doc", default=None, help="Limit to one document directory.")
def diagrams_generate(project: str, doc: str | None) -> None:
    """Write _generated/<FIG>.mmd and _generated/trace-table.md from validated IR."""
    from engine.diagram_ir import ir_files_by_doc
    from engine.diagram_render import generate
    ws = Workspace.load(Path(project))
    root = ws.root
    groups = ir_files_by_doc(root)
    only = _doc_filter(root, doc)
    if only is not None:
        groups = {k: v for k, v in groups.items() if k.resolve() == only}
    if not groups:
        click.echo("No diagram IR found (expected <doc-dir>/diagrams/*.ir.json).")
        sys.exit(2)
    failed = False
    for doc_dir in sorted(groups):
        written, diags = generate(doc_dir)
        for d in diags:
            _echo_diagnostic(d, root)
        if diags:
            failed = True
            continue
        for path in written.values():
            click.echo(f"wrote {path.relative_to(root).as_posix()}")
    if failed:
        click.echo("GENERATE: FAIL")
        sys.exit(1)
    click.echo("GENERATE: PASS")


@diagrams.command("manifest")
@click.option("--doc-dir", required=True, type=click.Path(exists=True, file_okay=False))
@click.option("--name", required=True)
@click.option("--docx", required=True, type=click.Path())
def diagrams_manifest(doc_dir: str, name: str, docx: str) -> None:
    """Write <name>.figures.json beside the built .docx (called by build-doc.sh)."""
    from engine.diagram_manifest import write_manifest
    out = write_manifest(Path(doc_dir), name, Path(docx))
    if out is None:
        click.echo("figures manifest: no rendered figures for this document; none written")
        return
    click.echo(f"figures manifest: {out}")


@diagrams.command("verify-manifest")
@click.argument("target", type=click.Path(exists=True))
def diagrams_verify_manifest(target: str) -> None:
    """Re-hash every file a figures manifest records; fail naming changed figures."""
    from engine.diagram_manifest import find_manifests, verify
    manifests = find_manifests(Path(target))
    if not manifests:
        click.echo(f"No *.figures.json manifest found for {target}")
        sys.exit(2)
    problems = []
    for m in manifests:
        found = verify(m)
        problems.extend(f"{m.name}: {p}" for p in found)
        if not found:
            click.echo(f"OK: {m.name}")
    for p in problems:
        click.echo(f"- {p}")
    if problems:
        click.echo("VERIFY-MANIFEST: FAIL")
        sys.exit(1)
    click.echo("VERIFY-MANIFEST: PASS")


@main.command()
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.option("--gate", required=True)
@click.option("--scope", default="*")
@click.option("--reason", required=True)
@click.option("--approver", required=True)
@click.option("--days", type=int, default=30, show_default=True)
def waive(project: str, gate: str, scope: str, reason: str,
          approver: str, days: int) -> None:
    """Append a new waiver to the project's _registry/waivers.yaml."""
    from datetime import date, timedelta
    from ruamel.yaml import YAML
    if not 1 <= days <= 90:
        raise click.ClickException(f"--days must be between 1 and 90 (got {days})")
    for field, value in (("gate", gate), ("reason", reason), ("approver", approver)):
        if not value.strip():
            raise click.ClickException(f"--{field} must be a non-empty value")
    try:
        scope = validate_scope(scope)
    except WaiverError as exc:
        raise click.ClickException(str(exc)) from exc
    yaml = YAML()
    ws = Workspace.load(Path(project))
    reg_dir = ws.root / "_registry"
    reg_dir.mkdir(exist_ok=True)
    waivers_path = reg_dir / "waivers.yaml"
    if waivers_path.exists():
        try:
            WaiverRegister.load(waivers_path)
        except WaiverError as exc:
            raise click.ClickException(
                f"Existing waiver register is invalid; no change made: {exc}"
            ) from exc
        data = yaml.load(waivers_path.read_text(encoding="utf-8")) or {"waivers": []}
    else:
        data = {"waivers": []}
    existing_ids = {w.get("id", "") for w in data.get("waivers", []) or []}
    n = 1
    while f"WAIVE-{n:03d}" in existing_ids:
        n += 1
    new_id = f"WAIVE-{n:03d}"
    today = date.today()
    expires = today + timedelta(days=days)
    entry = {
        "id": new_id,
        "gate": gate,
        "scope": scope,
        "reason": reason,
        "approver": approver,
        "approved_on": today.isoformat(),
        "expires_on": expires.isoformat(),
    }
    data.setdefault("waivers", []).append(entry)
    with waivers_path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f)
    click.echo(f"Added {new_id} to {waivers_path} (expires {expires})")


@main.command()
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.option("--gate", required=True, help="e.g. phase02, phase06, phase09")
@click.option("--signer", required=True)
@click.option("--role", required=True)
@click.option("--artifact", "artifacts", multiple=True, required=True,
              help="Repeat --artifact for each file in the signed-off set")
@click.option("--comment", default="")
def signoff(project: str, gate: str, signer: str, role: str,
            artifacts: tuple[str, ...], comment: str) -> None:
    """Append a sign-off entry to _registry/sign-off-ledger.yaml."""
    from datetime import date
    from ruamel.yaml import YAML
    yaml = YAML()
    ws = Workspace.load(Path(project))
    reg_dir = ws.root / "_registry"
    reg_dir.mkdir(exist_ok=True)
    ledger_path = reg_dir / "sign-off-ledger.yaml"
    if ledger_path.exists():
        data = yaml.load(ledger_path.read_text(encoding="utf-8")) or {"sign_offs": []}
    else:
        data = {"sign_offs": []}
    entry = {
        "gate": gate,
        "signer": signer,
        "role": role,
        "signed_on": date.today().isoformat(),
        "artifact_set": list(artifacts),
    }
    if comment:
        entry["comment"] = comment
    data.setdefault("sign_offs", []).append(entry)
    with ledger_path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f)
    click.echo(
        f"Signed off {gate} by {signer} ({role}) on {entry['signed_on']}"
    )


@main.command()
@click.argument("project", type=click.Path(exists=True, file_okay=False))
@click.option("--out", type=click.Path(), required=True)
def pack(project: str, out: str) -> None:
    """Build an evidence pack ZIP of _context, _registry, and 09-governance-compliance."""
    from engine.pack import build_evidence_pack
    build_evidence_pack(Path(project), Path(out))
    click.echo(f"Wrote evidence pack to {out}")


@main.group()
def controls() -> None:
    """Domain control-register commands (read-only; M10-08-T10)."""


@controls.command("search")
@click.argument("query")
@click.option("--domain", default=None, help="Limit to one domain, e.g. finance.")
@click.option("--framework", default=None,
              help="Case-insensitive substring of the regulatory framework, e.g. PCI.")
@click.option("--top", type=int, default=5, show_default=True)
@click.option("--json", "as_json", is_flag=True, help="Print the result as JSON.")
def controls_search(query: str, domain: str | None, framework: str | None,
                    top: int, as_json: bool) -> None:
    """Rank anchored controls for QUERY; abstain when nothing matches well."""
    import json as _json
    from engine.controls_search import search
    root = Path(__file__).resolve().parent.parent
    result = search(query, root=root, domain=domain, framework=framework, top=top)
    if as_json:
        click.echo(_json.dumps(result, indent=2, ensure_ascii=False))
        return
    if result["abstained"]:
        click.echo(f"ABSTAINED: no control scored at or above {result['threshold']} "
                   f"(best {result['best_score']}). Refine the query or read the registers.")
        return
    for hit in result["results"]:
        click.echo(f"{hit['id']}  {hit['title']}  [{hit['framework']} {hit['clause']}]  "
                   f"score={hit['score']}  {hit['registry_path']}")


if __name__ == "__main__":
    main()
