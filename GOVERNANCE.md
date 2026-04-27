# GOVERNANCE.md — md-osi-fiscal-mx

**Versión del modelo de gobernanza:** 1.0
**Vigente desde:** 2026-04-26
**Próxima revisión:** 2026-10-26 (cada 6 meses)

---

## Modelo

`md-osi-fiscal-mx` opera bajo un modelo de **gobernanza interna con apertura
estructurada** (Apache 2.0).

- **Mantenedor principal:** MD Consultoría SC (entidad legal mexicana, RFC
  MCO100329ED8). Marx Chávez como Lead Maintainer durante Fase 0 y 1.
- **Repo público:** cualquiera puede leer, fork, citar, abrir issues, abrir PRs.
- **Decisión final sobre merge:** Lead Maintainer + cross-audit IA.

Esta combinación maximiza:
- **Transparencia** (cualquiera audita la espec)
- **Rapidez** (no hay comité que ralentice un fix)
- **Seriedad técnica** (cross-audit obligatorio elimina decisiones impulsivas)

## Roles

### Lead Maintainer

Responsabilidades:
- Aprueba o rechaza PRs después de cross-audit
- Define roadmap (versionado)
- Cuts releases
- Comunica cambios major a productos consumidores del holding
- Garantiza que CI esté verde en `main`

**Persona actual:** Marx Chávez (CEO MD Consultoría SC)

### Mantenedores secundarios

Pueden aprobar PRs de fixes menores (typo, ejemplo, docs). NO pueden aprobar
reglas nuevas ni cambios de estado de regla.

**Personas actuales:** ninguna designada todavía. En Fase 1 se evalúa designar
1-2 mantenedores secundarios entre el equipo MD Consultoría TI.

### Validador Fiscal externo

Asesor designado para validar reglas con impacto fiscal alto antes de mergear.
Su firma cuenta como segundo criterio humano.

**Persona actual:** Benjamín Mora (despacho fiscal, asesor de Veolia VME9307222H2)

### Cross-audit IA

Toda regla nueva o cambio mayor pasa por al menos UNA de las siguientes:
- Gemini CLI (Google One AI Pro, v0.29.0+)
- Claude AI (Anthropic, opus o sonnet)

El audit es una segunda mente que busca conflictos, lagunas, base legal
mal citada. El audit NO toma la decisión final — informa al Lead Maintainer.

## Tipos de cambio y aprobación requerida

| Tipo | Cross-audit IA | Validador Fiscal | Lead Maintainer | Releases |
|---|---|---|---|---|
| Typo / doc fix | ❌ | ❌ | ✅ | PATCH |
| Nuevo fixture o ejemplo | ❌ | ❌ | ✅ | PATCH |
| Refactor sin cambio semántico | ✅ | ❌ | ✅ | PATCH |
| Regla nueva (estado=stable) | ✅ | ✅ | ✅ | MINOR |
| Cambio breaking en regla existente | ✅ | ✅ | ✅ | MAJOR |
| Deprecation de regla | ✅ | ✅ | ✅ | MINOR |
| Nuevo dominio (`spec/domains/X`) | ✅ | ✅ | ✅ | MINOR |
| Schema breaking | ✅ | ❌ | ✅ | MAJOR |

## Proceso de release

1. **Cut release branch:** `release/v{X}.{Y}.{Z}` desde `main`.
2. **Validar suite:** CI verde, todos los tests pasando, CHANGELOG actualizado.
3. **Tag git:** `vX.Y.Z` firmado.
4. **Publicar:** workflow CI publica a PyPI y npm.
5. **Notificar consumidores:** issue en cada repo del Stack Fiscal MD (CFDI-Motor,
   ERPNext-MX, CFDI-Suite, Escudo Fiscal) con changelog y guía de migración.

Releases mayores (MAJOR) requieren período de deprecation de **al menos 8
semanas** antes de remover funcionalidad. Productos consumidores deben tener
ventana razonable para hacer pin a versión nueva.

## Disputas y conflictos

Si un PR genera disputa entre mantenedores o entre IA cross-audits:

1. **Discusión técnica en el PR.** Citar base legal, jurisprudencia, casos.
2. **Si persiste:** abrir issue separado de "Decisión RN-XXX" con todos los
   argumentos.
3. **Decisión final:** Lead Maintainer publica resolución con razonamiento.
4. **Si la disputa es estructural** (modelo de gobernanza, dirección del repo):
   se discute en próxima revisión semestral del modelo.

## Cambios al modelo de gobernanza

Este documento (`GOVERNANCE.md`) puede modificarse SOLO con:
1. PR con propuesta detallada
2. Discusión abierta mínimo 14 días
3. Aprobación Lead Maintainer

## Forks y derivativos

Apache 2.0 permite fork, modificación y distribución. Pedimos que:
- Cites repositorio original
- Si tu fork agrega reglas relevantes para fiscal MX, considera abrir PR upstream
- NO uses el nombre `md-osi-fiscal-mx` en tu fork sin permiso (es marca
  de uso, no marca registrada)

## Confidencialidad y datos

Este repo es público. **NUNCA** committear:
- RFCs reales de clientes
- Montos reales asociables a un cliente
- CSDs, FIEL, sellos digitales
- Contenido de cuadernos de auditoría reales

Todo fixture debe usar RFC ficticios genéricos (`XAXX010101000`,
`EKU9003173C9`) o anonimización irreversible.

## Conexión con productos del holding

`md-osi-fiscal-mx` es activo público. Productos privados que lo consumen
(Stack Fiscal MD) operan bajo licencias propias. La separación es intencional:

- **Espec semántica** = público, exportable, citable
- **Implementación + UX + datos cliente** = privado, propiedad del holding

Si un competidor adopta `md-osi-fiscal-mx`, es señal de éxito (lock-in
semántico). El moat del holding está en la implementación + datos
operacionales, no en esta espec.

## Contacto

**Lead Maintainer:** Marx Chávez · `mdsamca2025@gmail.com`
**Issues:** https://github.com/MarxCha/md-osi-fiscal-mx/issues
**Discusiones técnicas:** GitHub Discussions del repo
