"""Tests de loading + validación schema de las 5 reglas iniciales."""
from __future__ import annotations

import pytest

from md_osi_fiscal import list_reglas, load_domain, load_regla


@pytest.mark.parametrize("rn_id", ["RN-001", "RN-002", "RN-003", "RN-004", "RN-005"])
def test_load_regla_basico(rn_id: str) -> None:
    regla = load_regla(rn_id)
    assert regla.id == rn_id
    assert regla.estado in ("stable", "beta", "deprecated", "experimental")
    assert regla.descripcion
    assert len(regla.ejemplos) >= 1


def test_list_reglas_stable_returns_5() -> None:
    reglas = list_reglas(estado="stable")
    ids = sorted(r.id for r in reglas)
    assert ids == ["RN-001", "RN-002", "RN-003", "RN-004", "RN-005"]


def test_load_domain_iva_cobrado() -> None:
    dom = load_domain("iva_cobrado")
    assert dom.id == "iva_cobrado"
    assert len(dom.terminos) >= 5
    ids = sorted(t.id for t in dom.terminos)
    assert "iva_cobrado" in ids
    assert "operacion_real_material" in ids


def test_rn001_base_legal_cita_liva_5_fraccion_i() -> None:
    regla = load_regla("RN-001")
    leyes = [b.ley for b in regla.base_legal]
    assert "LIVA" in leyes


def test_rn005_referencia_veolia_dec014() -> None:
    regla = load_regla("RN-005")
    refs = [str(r) for r in regla.referencias_cruzadas]
    assert any("DEC-014" in ref for ref in refs)
