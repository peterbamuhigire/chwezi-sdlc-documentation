"""Phase 03 - Design Documentation gate (ISO/IEC/IEEE 42010:2011)."""
from __future__ import annotations
import re
from engine.artifact_graph import Artifact, ArtifactGraph
from engine.checks.design_sufficiency import DesignSufficiencyCheck
from engine.findings import Finding, FindingCollection, Severity
from engine.gates.base import Gate
from engine.gates._shared import ClauseRef, attach_clause
from engine.figures import figures_in, load_manifest_index

_CLAUSE_ADR = ClauseRef("ISO/IEC/IEEE 42010:2011", "5.3")
_CLAUSE_INTERFACES = ClauseRef("ISO/IEC/IEEE 42010:2011", "5.4")
_CLAUSE_DATA = ClauseRef("ISO/IEC/IEEE 42010:2011", "5.5")
_CLAUSE_NFR_LINKS = ClauseRef("ISO/IEC/IEEE 42010:2011", "5.3.1")
_CLAUSE_SUFFICIENCY = ClauseRef("ISO/IEC/IEEE 42010:2011", "5.3.1")
_CLAUSE_THREAT = ClauseRef("ISO/IEC/IEEE 42010:2011", "5.3.2")
_CLAUSE_IOT = ClauseRef("ISO/IEC/IEEE 42010:2011", "5.5")
_CLAUSE_VIEWS = ClauseRef("ISO/IEC/IEEE 42010:2011", "5.6")

_ADR_DIR_TOKEN = "/adr/"
_ADR_ID_PREFIX = "ADR-"
_API_SPEC_TOKENS = ("/03-api-specification/", "/api-specification/")
_DB_DESIGN_TOKENS = ("/04-database-design/", "/database-design/")
_PHASE03_ROOT = "03-design-documentation/"
_THREAT_MODEL_SUFFIX = "threat-model.md"
_IOT_DIR_TOKEN = "/07-iot-system-design/"
_IOT_ROOT = "07-iot-system-design/"
_SIGNAL_INVENTORY_SUFFIXES = ("signal-inventory.md", "signals.md")
_NFR_PREFIX = "NFR-"
# HLD/LLD documents: a path segment or file name carrying one of these tokens.
_DESIGN_DOC_TOKEN_RE = re.compile(
    r"(?<![a-z])(hld|lld|high-level-design|low-level-design)(?![a-z])"
)

_HTTP_METHOD_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\b")
_RESPONSE_RE = re.compile(
    r"(response|status|\b200\b|\b201\b|\b204\b|\b400\b|\b404\b|\b500\b)",
    re.IGNORECASE,
)
_PRIMARY_KEY_RE = re.compile(r"\b(PRIMARY KEY|primary\s+key|\bPK\b)\b")


def _posix(path) -> str:
    return str(path).replace("\\", "/")


def _find_by_suffix(graph: ArtifactGraph, suffix: str):
    for art in graph.artifacts:
        if _posix(art.path).endswith(suffix):
            return art
    return None


class Phase03Gate(Gate):
    id = "phase03"
    title = "Design Documentation phase gate"
    severity = Severity.HIGH

    def evaluate(self, graph: ArtifactGraph, findings: FindingCollection) -> None:
        self._check_architecture_decisions_recorded(graph, findings)
        self._check_interfaces_have_contracts(graph, findings)
        self._check_data_model_has_keys(graph, findings)
        self._check_nfrs_link_to_design_choices(graph, findings)
        self._check_requirements_have_design_evidence(graph, findings)
        self._check_security_threat_model_present(graph, findings)
        self._check_iot_signal_inventory_present(graph, findings)
        self._check_design_docs_have_figures(graph, findings)

    # -- Check 1: architecture decisions recorded ------------------------
    def _check_architecture_decisions_recorded(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        for art in graph.artifacts:
            if _ADR_DIR_TOKEN in f"/{_posix(art.path)}":
                return
        for ident in graph.all_identifiers():
            if ident.startswith(_ADR_ID_PREFIX):
                return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.architecture_decisions_recorded",
            severity=Severity.HIGH,
            message=(
                "No Architecture Decision Records found: expected an "
                "'adr/' directory or ADR-### identifiers in design artifacts"
            ),
            location=None,
            line=None,
        ), _CLAUSE_ADR))

    # -- Check 2: interfaces have contracts ------------------------------
    def _check_interfaces_have_contracts(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        for art in graph.artifacts:
            posix = f"/{_posix(art.path)}"
            if not any(tok in posix for tok in _API_SPEC_TOKENS):
                continue
            missing = []
            if not _HTTP_METHOD_RE.search(art.body):
                missing.append("HTTP method")
            if not _RESPONSE_RE.search(art.body):
                missing.append("response/status")
            if missing:
                findings.add(attach_clause(Finding(
                    gate_id=f"{self.id}.interfaces_have_contracts",
                    severity=Severity.HIGH,
                    message=(
                        f"API spec '{_posix(art.path)}' missing required "
                        f"contract fields: {', '.join(missing)}"
                    ),
                    location=art.path,
                    line=None,
                ), _CLAUSE_INTERFACES))

    # -- Check 3: data model has keys ------------------------------------
    def _check_data_model_has_keys(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        for art in graph.artifacts:
            posix = f"/{_posix(art.path)}"
            if not any(tok in posix for tok in _DB_DESIGN_TOKENS):
                continue
            if _PRIMARY_KEY_RE.search(art.body):
                continue
            findings.add(attach_clause(Finding(
                gate_id=f"{self.id}.data_model_has_keys",
                severity=Severity.HIGH,
                message=(
                    f"Database design artifact '{_posix(art.path)}' has "
                    f"no primary key declaration (expected 'PRIMARY KEY', "
                    f"'primary key', or 'PK')"
                ),
                location=art.path,
                line=None,
            ), _CLAUSE_DATA))

    # -- Check 4: NFRs link to design choices ----------------------------
    def _check_nfrs_link_to_design_choices(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        nfr_ids = sorted({
            i for i in graph.all_identifiers() if i.startswith(_NFR_PREFIX)
        })
        if not nfr_ids:
            return
        phase03_body_parts = []
        for art in graph.artifacts:
            if art.phase == "03" or _posix(art.path).startswith(_PHASE03_ROOT):
                phase03_body_parts.append(art.body)
        phase03_text = "\n".join(phase03_body_parts)
        for nfr in nfr_ids:
            if nfr in phase03_text:
                continue
            findings.add(attach_clause(Finding(
                gate_id=f"{self.id}.nfrs_link_to_design_choices",
                severity=Severity.HIGH,
                message=(
                    f"{nfr} is declared but not referenced in any "
                    f"Phase 03 design artifact"
                ),
                location=None,
                line=None,
            ), _CLAUSE_NFR_LINKS))

    # -- Check 5: FRs have concrete design evidence ----------------------
    def _check_requirements_have_design_evidence(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        tmp = FindingCollection()
        DesignSufficiencyCheck(
            f"{self.id}.requirements_have_design_evidence"
        ).run(graph, tmp)
        for f in tmp:
            findings.add(attach_clause(f, _CLAUSE_SUFFICIENCY))

    # -- Check 6: security threat model present --------------------------
    def _check_security_threat_model_present(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        for art in graph.artifacts:
            posix = _posix(art.path)
            if not posix.startswith(_PHASE03_ROOT):
                continue
            if posix.endswith(_THREAT_MODEL_SUFFIX):
                return
            if "threat model" in art.body.lower():
                return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.security_threat_model_present",
            severity=Severity.HIGH,
            message=(
                "No threat model found under 03-design-documentation/ "
                "(expected 'threat-model.md' file or 'threat model' "
                "reference in a design artifact)"
            ),
            location=None,
            line=None,
        ), _CLAUSE_THREAT))

    # -- Check 7: IoT signal inventory present ---------------------------
    def _check_iot_signal_inventory_present(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        is_iot = False
        for art in graph.artifacts:
            if _IOT_DIR_TOKEN in f"/{_posix(art.path)}":
                is_iot = True
                break
            if "IoT" in art.body:
                is_iot = True
                break
        if not is_iot:
            return
        for art in graph.artifacts:
            posix = _posix(art.path)
            if not posix.startswith(_PHASE03_ROOT):
                continue
            if _IOT_ROOT not in posix:
                continue
            if any(posix.endswith(sfx) for sfx in _SIGNAL_INVENTORY_SUFFIXES):
                return
        findings.add(attach_clause(Finding(
            gate_id=f"{self.id}.iot_signal_inventory_present",
            severity=Severity.HIGH,
            message=(
                "IoT scope detected but no signal inventory found "
                "(expected '07-iot-system-design/signal-inventory.md' "
                "or 'signals.md')"
            ),
            location=None,
            line=None,
        ), _CLAUSE_IOT))

    # -- Check 8: HLD/LLD documents carry a rendered design figure -------
    def _check_design_docs_have_figures(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        """Each HLD/LLD document needs at least one figure a reader can see.

        A document is the directory (or file) whose name carries an HLD/LLD
        token under 03-design-documentation/. A Mermaid code block alone does
        not count; see engine/figures.py for what does (M10-01-T12, AR-03).
        """
        groups: dict = {}
        for art in graph.artifacts:
            posix = _posix(art.path)
            if not posix.startswith(_PHASE03_ROOT):
                continue
            parts = posix[len(_PHASE03_ROOT):].split("/")
            for depth, part in enumerate(parts):
                if _DESIGN_DOC_TOKEN_RE.search(part.lower()):
                    key = _PHASE03_ROOT + "/".join(parts[: depth + 1])
                    groups.setdefault(key, []).append(art)
                    break
        if not groups:
            return
        root = graph.root
        index = load_manifest_index(root) if root is not None else {}
        for key in sorted(groups):
            if any(figures_in(art, root, index) for art in groups[key]):
                continue
            findings.add(attach_clause(Finding(
                gate_id=f"{self.id}.design_docs_have_figures",
                severity=Severity.HIGH,
                message=(
                    f"Design document '{key}' has no rendered design figure: "
                    f"expected an image whose file exists, or a Mermaid block "
                    f"rendered by scripts/render_diagrams.py (a code block "
                    f"alone is not a figure)"
                ),
                location=None,
                line=None,
            ), _CLAUSE_VIEWS))
