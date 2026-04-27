# Changelog

Todos los cambios notables en `md-osi-fiscal-mx` se documentan aquí.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
versionado [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Implementación de referencia Python (`implementations/python/`) con
  `load_regla(id)`, `list_reglas(estado)`, `load_domain(id)`. Pydantic v2 +
  pyyaml. Pip-installable como `md-osi-fiscal`.
- Tests `tests/test_regla_loading.py` (9 pasan): valida los 5 RN + dominio
  iva_cobrado + referencias cruzadas.

### Pendiente
- Reglas RN-006..RN-022 (cierre Fase 1, Sprint 3 Escudo Fiscal)
- Dominios `isr`, `diot`, `nomina`, `materialidad`
- Implementación de referencia TypeScript (`@md/osi-fiscal-mx` en npm)
- Servidor MCP `mcp-osi-fiscal:8804`
- EBNF Anexo 20 para constrained decoding (Fase 1)

---

## [1.0.0-rc1] - 2026-04-26

### Added
- Repo creado bajo licencia Apache 2.0
- `README.md` — manifesto, estructura, quickstart consumidor
- `CONTRIBUTING.md` — proceso de contribución
- `GOVERNANCE.md` — modelo de gobernanza interna v1.0
- `METHODOLOGY.md` — cinco filtros de validación de regla
- `LICENSE` — Apache 2.0
- `.github/workflows/ci.yml` — CI: validación JSON Schema sobre YAML + linting
- `spec/schemas/regla.schema.json` — schema JSON canónico para reglas
- `spec/schemas/domain.schema.json` — schema JSON canónico para dominios
- `spec/reglas/RN-001-bucket-mxp-usd.yaml` — bucket MXP/USD por moneda CFDI
- `spec/reglas/RN-002-ncs-no-deducir.yaml` — NCs no se deducen del cobrado
- `spec/reglas/RN-003-tc-cfdi-prioridad.yaml` — TC CFDI prioridad sobre TC banco
- `spec/reglas/RN-004-dedup-reps-cancelados.yaml` — dedup REPs cancelados
- `spec/reglas/RN-005-gold-celda-especifica.yaml` — gold = celda específica
- `spec/domains/iva_cobrado.yaml` — dominio IVA cobrado con 5 términos canónicos
- `implementations/python/md_osi_fiscal/definitions.py` — implementación de
  referencia básica `load_regla(id) -> Regla`
- `tests/fixtures/` — fixtures iniciales por regla

### Notes
- Esta es la **release candidate inicial**. Productos consumidores del Stack
  Fiscal MD pueden hacer pin a esta versión, pero no debe usarse en producción
  hasta `1.0.0` final.
- Las 5 reglas iniciales están migradas de `cfdi-motor/REGLAS-NEGOCIO.md` con
  estado `stable` (certificadas al centavo contra Veolia enero 2026).
- CI verifica schema en cada PR. Reglas mal estructuradas son rechazadas
  automáticamente.

### Migrating from `cfdi-motor/REGLAS-NEGOCIO.md`
- Productos del Stack Fiscal MD que mantienen referencia a
  `REGLAS-NEGOCIO.md#RN-XXX` pueden continuar haciéndolo durante Sprint 0-1.
- A partir de Sprint 2, productos deben hacer pin a este repo y consumir vía
  servidor MCP o import directo.

---

## Convenciones del Changelog

- `Added` — funcionalidad nueva
- `Changed` — cambios en funcionalidad existente
- `Deprecated` — funcionalidad que se removerá en versión mayor futura
- `Removed` — funcionalidad removida
- `Fixed` — corrección de bug
- `Security` — corrección con implicación de seguridad

Cada release incluye fecha en formato YYYY-MM-DD.
