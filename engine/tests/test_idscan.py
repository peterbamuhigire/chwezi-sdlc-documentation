"""engine.idscan allowlist behaviour (M10-08 hand-off: EI prefix)."""
from engine.idscan import KIND_PREFIXES, find_ids, kind_of


def test_external_interface_ids_are_recognised():
    assert "EI" in KIND_PREFIXES
    assert find_ids("See **EI-003** and EI-PAY-012 for the gateway.") == {"EI-003", "EI-PAY-012"}
    assert kind_of("EI-003") == "EI"


def test_ei_inside_a_longer_token_is_not_an_identifier():
    assert find_ids("SEI-001 and EI-12 and xEI-004") == set()
