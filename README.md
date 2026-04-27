# md-osi-fiscal-mx

> **Open Semantic Interchange (OSI) Fiscal MX** — espec semántica canónica para fiscalidad mexicana

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-1.0.0--rc1-orange.svg)](CHANGELOG.md)
[![Maintainer](https://img.shields.io/badge/maintainer-MD%20Consultor%C3%ADa%20SC-green.svg)](https://github.com/MarxCha)

---

## Qué es

`md-osi-fiscal-mx` es el repositorio público que define, en YAML estructurado y
verificable por máquina, las reglas de negocio, definiciones canónicas e
invariantes fiscales mexicanos derivados de:

- **CFF** (Código Fiscal de la Federación)
- **LISR** (Ley del Impuesto Sobre la Renta)
- **LIVA** (Ley del IVA)
- **RMF** (Resolución Miscelánea Fiscal)
- **Anexo 20** (CFDI 4.0)
- **Reglas operativas validadas** contra clientes reales (Veolia VME9307222H2,
  MD Consultoría MCO100329ED8)

Es la **fuente única de verdad semántica** para el Stack Fiscal MD: CFDI-Motor,
ERPNext-MX, CFDI-Suite, Escudo Fiscal.

## Por qué existe

Antes de este repo, las 22 reglas de negocio + 33 decisiones + spec
FISCAL-REQUIREMENTS vivían dispersas en `.context/` de cada producto. Esto
generaba tres problemas:

1. **Duplicación.** La misma regla copiada en 3 productos con 3 redacciones
   levemente distintas → divergencia silenciosa.
2. **No verificable.** Sin schema, sin CI, sin tests → nada garantiza que la
   regla escrita coincide con la implementación.
3. **No exportable.** Conocimiento atrapado en repos privados → no puede ser
   citado, validado externamente, o reutilizado por otros productos del holding
   (POA Dashboard, Odoo MD, productos futuros).

Este repo resuelve los tres: estructura formal, CI con validación de schema
JSON, distribución pública vía Apache 2.0.

## Filosofía

1. **Una fuente, muchos consumidores.** Reglas YAML aquí; productos las
   consumen vía PyPI (`md-osi-fiscal`), npm (`@md/osi-fiscal-mx`), o servidor
   MCP (`mcp-osi-fiscal:8804`).
2. **Determinismo por defecto.** El 70% de la lógica fiscal son reglas
   deterministas. La IA solo entra para casos genuinamente ambiguos.
3. **Base legal siempre.** Cada regla cita el artículo, párrafo, fracción,
   inciso. Sin base legal no entra al repo.
4. **Versionado SemVer estricto.** Cambios que rompan compatibilidad son MAJOR.
   Productos consumidores hacen pin explícito.
5. **Apertura como activo.** Repo público desde Day-1 → señal de seriedad
   profesional para adopción interna y externa al holding.

## Estructura del repo

```
md-osi-fiscal-mx/
├── LICENSE                  # Apache 2.0
├── README.md                # Este archivo
├── CONTRIBUTING.md          # Cómo proponer cambios
├── GOVERNANCE.md            # Modelo de gobernanza interno v1.0
├── METHODOLOGY.md           # Cómo se valida una regla antes de mergear
├── CHANGELOG.md             # Historial de releases SemVer
├── .github/workflows/       # CI: validación schema YAML + linting
│   └── ci.yml
├── spec/                    # La espec semántica
│   ├── reglas/              # Reglas de negocio RN-XXX (1 archivo por regla)
│   │   └── RN-001-bucket-mxp-usd.yaml
│   ├── domains/             # Dominios semánticos (iva_cobrado, isr, diot, ...)
│   │   └── iva_cobrado.yaml
│   └── schemas/             # JSON Schema para validar los YAML
│       ├── regla.schema.json
│       └── domain.schema.json
├── implementations/         # Implementaciones de referencia
│   └── python/              # md_osi_fiscal package (PyPI)
└── tests/                   # Test fixtures + tests cross-implementation
    └── fixtures/
```

## Quickstart consumidor

### Python

```bash
pip install md-osi-fiscal  # cuando se publique
```

```python
from md_osi_fiscal import load_regla, verify_invariant

regla = load_regla("RN-001")
print(regla.descripcion)
print(regla.base_legal)

# Verificar invariante
ok, hallazgos = verify_invariant("ANEXO20-OBLIGATORIO", cfdi_xml)
```

### TypeScript

```bash
pnpm add @md/osi-fiscal-mx  # cuando se publique
```

```typescript
import { loadRegla } from "@md/osi-fiscal-mx";
const regla = await loadRegla("RN-001");
```

### Vía MCP

```bash
# Servidor mcp-osi-fiscal:8804 expone tools:
# - get_definition(termino)
# - get_regla(rn_id)
# - verify_invariant(invariant_id, payload)
# - search_jurisprudencia(query)
```

## Estado actual

**Versión:** 1.0.0-rc1 (release candidate inicial)
**Reglas publicadas:** 5 / 22 objetivo (RN-001..RN-005)
**Dominios:** 1 (`iva_cobrado`)
**Implementaciones:** Python básica
**Distribución:** PyPI/npm pendiente al pasar a 1.0.0

## Roadmap

| Versión | Contenido | Estado |
|---|---|---|
| `1.0.0-rc1` | 5 reglas iniciales + dominio `iva_cobrado` + CI | 🟡 Sprint 0 actual |
| `1.0.0` | 22 reglas completas + dominios `isr`, `diot`, `nomina` | ⏳ Sprint 1-3 |
| `1.1.0` | Anexo 20 EBNF para constrained decoding | ⏳ Fase 1 |
| `2.0.0` | Schema breaking changes + BVI / e-invoicing internacional | ⏳ Fase 3 |

## Gobernanza

Mantenido por **MD Consultoría SC**. PRs externos bienvenidos siguiendo
[`CONTRIBUTING.md`](CONTRIBUTING.md). Mergeo final requiere:

1. CI verde (schema + tests)
2. Base legal citada y verificable
3. Aprobación de mantenedor MD Consultoría
4. Cross-audit de un segundo agente IA (Gemini CLI o Claude AI)

Detalles en [`GOVERNANCE.md`](GOVERNANCE.md) y [`METHODOLOGY.md`](METHODOLOGY.md).

## Productos del holding que consumen este repo

| Producto | Repo | Cómo consume |
|---|---|---|
| **CFDI-Motor** | `MarxCha/cfdi-motor` (privado) | Servidor MCP + import directo Python |
| **ERPNext-MX** | `MarxCha/erpnext-mexico` (privado) | Servidor MCP |
| **CFDI-Suite** | `MarxCha/cfdi-suite` (público Vercel) | Cliente TypeScript |
| **Escudo Fiscal** | `MarxCha/escudo-fiscal` (privado Sprint 0-3) | Servidor MCP + cliente TS |

## Licencia

Apache License 2.0 — ver [`LICENSE`](LICENSE).

## Contacto

**Marx Chávez** · CEO MD Consultoría SC · `mdsamca2025@gmail.com`

---

*Repo creado el 2026-04-26 como parte del Sprint 0 de Escudo Fiscal,
materializando ADR-003 de CFDI-Motor.*
