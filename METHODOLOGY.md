# METHODOLOGY.md — Cómo se valida una regla

**Aplica a:** todas las reglas en `spec/reglas/RN-XXX.yaml`
**Vigente desde:** 2026-04-26

---

## Por qué este documento existe

Una regla en `md-osi-fiscal-mx` no es opinión — es una afirmación verificable
sobre cómo se comporta el sistema fiscal mexicano. Antes de aceptar una regla
debe pasar **cinco filtros**.

Si una regla pasa los cinco, entra como `estado: stable`. Si pasa solo tres
o cuatro, puede entrar como `estado: beta` con plan explícito de cierre.

---

## Filtro 1 — Base legal

**Pregunta:** ¿la regla cita un artículo de ley, RMF, criterio normativo SAT,
o jurisprudencia tesis TFJA verificable?

**Cumple:**
- Artículo XX de la LISR / LIVA / CFF, con párrafo y fracción
- RMF YYYY regla X.X.X.X
- Criterio normativo SAT publicado
- Tesis aislada o jurisprudencia con número, año, sala, ponente

**No cumple:**
- "Es práctica común" sin sustento legal
- "El SAT lo aceptó en una revisión" sin oficio o documento
- "Lo dijo un asesor"

Si la regla no tiene base legal pero es operativamente necesaria (ej.
convención de redondeo entre productos), va al campo `base_practica` con
explicación. NO se confunde con `base_legal`.

## Filtro 2 — Caso operativo real

**Pregunta:** ¿la regla nace de un caso real observado, o es teórica?

**Cumple:**
- Cliente X presentó situación Y, motor produjo resultado Z, se identificó la
  necesidad de la regla
- Auditoría SAT a cliente X resultó en observación que la regla previene
- Diff entre dos productos del Stack Fiscal MD evidenció ambigüedad

**No cumple:**
- "Por si acaso pasara"
- "En teoría podría pasar"
- "La ley dice X, mejor escribimos regla aunque no haya pasado"

Si la regla es defensiva contra un escenario teórico, va con `estado: beta` y
plan de bajar a `stable` cuando se acumule evidencia operativa.

## Filtro 3 — Test fixtures determinísticos

**Pregunta:** ¿la regla puede expresarse como tests con input/output explícitos
que pasan o fallan deterministamente?

**Cumple:**
- 3 fixtures mínimos (happy path + frontera + no-aplica)
- Cada fixture tiene `input` y `output` esperado en JSON
- Fixtures pasan al ejecutar `pytest tests/fixtures/RN-XXX/`

**No cumple:**
- Regla escrita en prosa sin ejemplos numéricos
- Ejemplos sin output esperado ("debería resultar en algo razonable")
- Regla que requiere "criterio del contador" en runtime

Si la regla involucra criterio humano genuino (ambigüedad legal real), no es
una regla de este repo — es un ítem para módulo de copiloto IA con caveats
explícitos. NO entra al spec.

## Filtro 4 — Consistencia terminológica

**Pregunta:** ¿la regla usa términos definidos en `spec/domains/` o introduce
ambigüedad?

**Cumple:**
- Cada término técnico (`bucket`, `acreditable`, `efectivamente_cobrado`,
  `materialidad`) tiene una definición única en algún `domain.yaml`
- Si la regla introduce un término nuevo, también introduce su definición en
  el dominio correspondiente

**No cumple:**
- Reuso de un término con significado distinto al del dominio
- Términos coloquiales sin definición ("razonable", "apropiado", "claro")

## Filtro 5 — Cross-audit IA

**Pregunta:** ¿una segunda mente (IA) detecta conflictos, lagunas o errores?

**Comando:**
```bash
gemini audit-regla --diff PR-DIFF.md --regla RN-XXX
# o
claude review --regla spec/reglas/RN-XXX.yaml
```

El audit IA busca específicamente:

1. **Conflictos con reglas existentes** — ¿RN-XXX dice algo que contradice
   RN-YYY?
2. **Base legal mal citada** — ¿el artículo citado realmente dice eso?
3. **Lagunas** — ¿qué casos válidos no cubre la regla?
4. **Implicaciones no declaradas** — ¿al aceptar esta regla, qué otras
   reglas necesitan ajustarse?
5. **Inconsistencia con otros dominios** — ¿la regla pertenece al dominio
   declarado, o a otro?

El audit produce un reporte. El Lead Maintainer decide qué hallazgos
incorporar antes de mergear.

---

## Estados de regla

| Estado | Significado | Filtros pasados | Pendiente |
|---|---|---|---|
| `stable` | Producción, productos consumidores la usan | Los 5 | — |
| `beta` | Operacional pero con caveats | 3-4 de 5 | Documentar qué falta |
| `deprecated` | Reemplazada o eliminada en versión futura | n/a | Plan de remoción + alternativa |
| `experimental` | Diseño en discusión, no usar en producción | <3 | Validación pendiente |

Reglas `experimental` viven en `spec/reglas/_experimental/` (subdirectorio
ignorado por la mayoría de consumidores).

---

## Procedimiento de bajar de `stable` a `deprecated`

1. PR que cambia `estado: stable` → `deprecated` en el YAML, agrega `reemplazo:
   RN-YYY` y `fecha_deprecation: YYYY-MM-DD`.
2. Cross-audit IA verifica que `RN-YYY` cubre todos los casos de la regla
   deprecada.
3. CHANGELOG.md anuncia la deprecation con ventana mínima 8 semanas.
4. Productos consumidores reciben notificación.
5. Tras la ventana, regla deprecada se mueve a `spec/reglas/_archive/`.

Reglas archivadas NO se borran del repo (auditoría histórica).

---

## Workflow de propuesta de regla nueva (resumen)

```
1. Issue con plantilla regla-nueva.md          (días 1)
2. Discusión técnica + base legal              (días 1-3)
3. Lead Maintainer aprueba o rechaza issue      (día 4)
4. PR con YAML + fixtures + diffs               (días 5-7)
5. CI corre validación schema + tests           (auto)
6. Cross-audit IA                               (día 8)
7. Validador Fiscal externo (si aplica)         (día 9-10)
8. Merge + bump versión + release               (día 11)
9. Notificación a productos consumidores        (día 11)
```

Tiempo total: **~2 semanas** desde issue hasta release. Reglas urgentes
(cambio DOF/RMF reciente que afecta operación) tienen path acelerado de **48-72
horas** con cross-audit obligatorio comprimido.

---

## Métricas de calidad del repo

Marx revisa cada último viernes del mes:

| Métrica | Meta |
|---|---|
| Reglas con base_legal verificable | 100% |
| Reglas con ≥3 fixtures | 100% |
| CI verde en main | 100% |
| Tiempo promedio issue→merge | <14 días |
| Reglas en estado `experimental` por >90 días | 0 (cierran o archivan) |
| Conflictos detectados post-merge por audit IA | <5% |

---

## Casos de excepción

### Regla emitida por el módulo Monitor DOF/RMF de Escudo Fiscal

El módulo 4.2 de Escudo Fiscal genera PRs automáticos cuando detecta cambios
en DOF/RMF. Estos PRs:
- Son tratados igual que cualquier PR humano (mismo proceso, mismos filtros)
- Tienen tag `bot:monitor-dof-rmf` en el PR para identificación
- Son revisados con prioridad si la base legal corresponde a publicación SAT
  reciente

### Regla heredada de CFDI-Motor

Las primeras 22 reglas migradas de `cfdi-motor/REGLAS-NEGOCIO.md` traen base
legal y test fixtures derivados del trabajo previo Veolia. Mantienen estado
`stable` desde Day-1 si la implementación CFDI-Motor las certificó al centavo
contra Veolia enero 2026.

---

## Contacto

**Lead Maintainer:** Marx Chávez · `mdsamca2025@gmail.com`
