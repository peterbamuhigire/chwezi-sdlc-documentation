"""Phase 02 - Requirements Engineering gate."""
from __future__ import annotations
from engine.artifact_graph import ArtifactGraph
from engine.checks.glossary_registry import GlossaryRegistryCheck
from engine.checks.identifier_registry import IdentifierRegistryCheck
from engine.checks.nfr_smart import SmartNfrCheck
from engine.checks.requirement_semantics import RequirementSemanticsCheck
from engine.checks.source_reconciliation import SourceReconciliationCheck
from engine.checks.stimulus_response import StimulusResponseCheck
from engine.findings import FindingCollection, Severity
from engine.gates.base import Gate
from engine.gates._shared import ClauseRef, attach_clause

_CLAUSE_SMART_NFR = ClauseRef("IEEE Std 830-1998", "3.3.2")
_CLAUSE_STIMULUS = ClauseRef("IEEE Std 830-1998", "4.3.2")
_CLAUSE_SEMANTICS = ClauseRef("IEEE Std 830-1998", "3.2")
_CLAUSE_ID_REGISTRY = ClauseRef("IEEE Std 830-1998", "4.3")
_CLAUSE_GLOSSARY = ClauseRef("IEEE Std 830-1998", "3.1")


class Phase02Gate(Gate):
    id = "phase02"
    title = "Requirements Engineering phase gate"
    severity = Severity.HIGH

    def evaluate(self, graph: ArtifactGraph, findings: FindingCollection) -> None:
        self._run_labeled(
            SmartNfrCheck(f"{self.id}.smart_nfr"),
            _CLAUSE_SMART_NFR,
            graph,
            findings,
        )
        self._run_labeled(
            StimulusResponseCheck(f"{self.id}.stimulus_response"),
            _CLAUSE_STIMULUS,
            graph,
            findings,
        )
        self._run_labeled(
            RequirementSemanticsCheck(f"{self.id}.requirement_semantics"),
            _CLAUSE_SEMANTICS,
            graph,
            findings,
        )
        self._check_identifier_registry(graph, findings)
        self._check_glossary_registry(graph, findings)
        findings.extend(SourceReconciliationCheck().run(graph))

    def _run_labeled(self, check, clause: ClauseRef, graph: ArtifactGraph,
                     findings: FindingCollection) -> None:
        tmp = FindingCollection()
        check.run(graph, tmp)
        for f in tmp:
            findings.add(attach_clause(f, clause))

    def _check_identifier_registry(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        if graph.root is None:
            return
        registry_path = graph.root / "_registry" / "identifiers.yaml"
        if not registry_path.exists():
            return
        tmp = FindingCollection()
        IdentifierRegistryCheck(
            f"{self.id}.id_registry", registry_path
        ).run(graph, tmp)
        for f in tmp:
            findings.add(attach_clause(f, _CLAUSE_ID_REGISTRY))

    def _check_glossary_registry(
        self, graph: ArtifactGraph, findings: FindingCollection
    ) -> None:
        if graph.root is None:
            return
        registry_path = graph.root / "_registry" / "glossary.yaml"
        if not registry_path.exists():
            return
        tmp = FindingCollection()
        GlossaryRegistryCheck(
            f"{self.id}.glossary_registry", registry_path
        ).run(graph, tmp)
        for f in tmp:
            findings.add(attach_clause(f, _CLAUSE_GLOSSARY))
