"""Modelos Pydantic + loaders YAML para md-osi-fiscal."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


class BaseLegal(BaseModel):
    model_config = ConfigDict(extra="allow")
    ley: str | None = None
    articulo: str | int | None = None
    parrafo: str | int | None = None
    fraccion: str | int | None = None
    inciso: str | None = None
    rmf: dict[str, Any] | str | None = None
    criterio_normativo: str | None = None
    tesis: str | None = None
    texto: str | None = None
    base_practica: str | None = None


class HistorialEntry(BaseModel):
    version: str
    fecha: str
    cambio: str
    autor: str | None = None


class IOField(BaseModel):
    model_config = ConfigDict(extra="allow")
    nombre: str
    tipo: str
    valores: list[Any] | None = None
    descripcion: str | None = None


class EjemploRegla(BaseModel):
    model_config = ConfigDict(extra="allow")
    descripcion: str | None = None
    input: dict[str, Any] | list[Any]
    output: Any


class Regla(BaseModel):
    """Regla de negocio RN-XXX."""

    model_config = ConfigDict(extra="allow")
    id: str
    nombre: str
    version: str
    estado: str
    descripcion: str
    base_legal: list[BaseLegal] = Field(default_factory=list)
    base_practica: str | None = None
    ambito: list[str]
    inputs: list[IOField] = Field(default_factory=list)
    outputs: list[IOField] = Field(default_factory=list)
    condiciones: str
    ejemplos: list[EjemploRegla]
    test_fixtures: list[str] = Field(default_factory=list)
    historial: list[HistorialEntry]
    referencias_cruzadas: list[dict[str, Any]] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    deprecated_por: str | None = None
    fecha_deprecation: str | None = None


class Termino(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    nombre: str
    definicion: str
    base_legal: list[BaseLegal] = Field(default_factory=list)
    sinonimos: list[str] = Field(default_factory=list)
    antonimos: list[str] = Field(default_factory=list)
    tipo: str | None = None
    ejemplos: list[str] = Field(default_factory=list)


class Domain(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    nombre: str
    version: str
    descripcion: str
    terminos: list[Termino]
    reglas_relacionadas: list[str] = Field(default_factory=list)


def _spec_root() -> Path:
    """Ubicación del directorio spec/.

    Busca en orden: variable env MD_OSI_FISCAL_SPEC_DIR → ../../spec respecto
    al package → cwd/spec. Permite override para tests.
    """
    import os

    if (override := os.environ.get("MD_OSI_FISCAL_SPEC_DIR")):
        return Path(override).resolve()

    here = Path(__file__).resolve()
    candidate = here.parent.parent.parent.parent / "spec"
    if candidate.exists():
        return candidate

    cwd_candidate = Path.cwd() / "spec"
    if cwd_candidate.exists():
        return cwd_candidate

    raise FileNotFoundError(
        "No se encontró el directorio spec/ — setea MD_OSI_FISCAL_SPEC_DIR"
    )


@lru_cache(maxsize=128)
def load_regla(rn_id: str) -> Regla:
    """Carga una regla por ID (ej. 'RN-001')."""
    if not rn_id.startswith("RN-"):
        raise ValueError(f"ID de regla inválido (debe empezar con RN-): {rn_id}")
    spec_dir = _spec_root() / "reglas"
    matches = list(spec_dir.glob(f"{rn_id}-*.yaml"))
    if not matches:
        raise FileNotFoundError(f"Regla {rn_id} no encontrada en {spec_dir}")
    if len(matches) > 1:
        raise RuntimeError(f"Ambigüedad: {len(matches)} archivos para {rn_id}: {matches}")
    raw = yaml.safe_load(matches[0].read_text(encoding="utf-8"))
    return Regla.model_validate(raw)


def list_reglas(estado: str | None = None) -> list[Regla]:
    """Listar todas las reglas, opcionalmente filtradas por estado."""
    spec_dir = _spec_root() / "reglas"
    out: list[Regla] = []
    for path in sorted(spec_dir.glob("RN-*.yaml")):
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        regla = Regla.model_validate(raw)
        if estado is None or regla.estado == estado:
            out.append(regla)
    return out


@lru_cache(maxsize=32)
def load_domain(domain_id: str) -> Domain:
    """Carga un dominio semántico por ID (ej. 'iva_cobrado')."""
    spec_dir = _spec_root() / "domains"
    path = spec_dir / f"{domain_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Dominio {domain_id} no encontrado en {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Domain.model_validate(raw)
