# Contribuir a md-osi-fiscal-mx

Gracias por tu interés en mejorar la espec semántica fiscal mexicana.

Este documento explica el proceso para proponer cambios. Las reglas aquí son
**estrictas** porque cada error en este repo se propaga a 4+ productos del
Stack Fiscal MD y eventualmente al cumplimiento fiscal real de clientes.

---

## Quién puede contribuir

| Tipo de contribución | Quién |
|---|---|
| Reglas nuevas o cambios mayores | Mantenedores MD Consultoría SC |
| Correcciones de tipos / typos / docs | Cualquier persona |
| Reglas inferidas vía IA (DOF/RMF auto-detect) | PR bot del módulo Monitor DOF de Escudo Fiscal — pasa al mismo proceso |
| Implementaciones de referencia adicionales (Rust, Go, etc.) | Cualquier persona — mismo proceso |

## Proceso para una regla nueva (RN-XXX)

### 1. Abrir issue antes del PR

Antes de escribir el YAML, abre un issue con la plantilla `regla-nueva.md`.
Necesitamos:

- **Problema observado** — qué situación operativa motiva la regla
- **Base legal candidata** — artículo, ley, RMF, jurisprudencia
- **Productos afectados** — qué consumidores deben ajustarse al merge
- **Caso operativo real** — cliente o expediente donde se aplicó (anonimizado)

Sin issue previo, el PR se cierra. No discutimos reglas en abstracto.

### 2. Estructura del YAML

Cada regla vive en `spec/reglas/RN-{numero}-{slug}.yaml`. El schema
canónico está en `spec/schemas/regla.schema.json`. Campos obligatorios:

```yaml
id: RN-001
nombre: "Bucket MXP/USD por moneda CFDI"
version: "1.0.0"
estado: stable  # stable | beta | deprecated
descripcion: "..."
base_legal:
  - ley: LIVA
    articulo: 1-B
    parrafo: 1
    texto: "..."
  - rmf:
    referencia: 2.7.1.43
ambito:
  - iva_cobrado
  - iva_pagado
inputs:
  - nombre: cfdi.moneda
    tipo: string
    valores: [MXN, USD, EUR, ...]
outputs:
  - nombre: bucket
    tipo: enum
    valores: [MXP, USD]
condiciones: |
  Si moneda == "MXN" → bucket = "MXP"
  Si moneda != "MXN" → bucket = "USD" (genérico)
ejemplos:
  - input: { moneda: "MXN", monto: 100.00 }
    output: { bucket: "MXP" }
  - input: { moneda: "USD", monto: 5.00 }
    output: { bucket: "USD" }
test_fixtures:
  - tests/fixtures/RN-001/case-1-mxn.json
  - tests/fixtures/RN-001/case-2-usd.json
historial:
  - version: "1.0.0"
    fecha: "2026-04-26"
    cambio: "Regla inicial"
    autor: "Marx Chávez"
referencias_cruzadas:
  - cfdi-motor: "REGLAS-NEGOCIO.md#RN-001"
  - documento_origen: "VEOLIA_DEC-014"
```

### 3. Test fixtures obligatorios

Toda regla NUEVA debe traer al menos 3 fixtures:
- 1 caso "happy path" (la regla aplica claramente)
- 1 caso límite (frontera donde la regla apenas aplica)
- 1 caso "no aplica" (input que no dispara la regla)

Fixtures van en `tests/fixtures/RN-{numero}/case-{n}-{descripcion}.json`.

### 4. Cross-audit

Todo PR de regla pasa por **dos validaciones** antes de mergear:

1. **CI automática:** valida JSON Schema, ejecuta fixtures, lintea YAML.
2. **Cross-audit IA:** un mantenedor invoca Gemini CLI o Claude AI con el
   diff y la base legal. El cross-audit busca:
   - Conflictos con reglas existentes
   - Base legal inexistente o citada incorrectamente
   - Lagunas (caso real conocido que la regla no cubre)
   - Inconsistencias terminológicas con `spec/domains/`

3. **Aprobación humana final:** un mantenedor MD Consultoría SC.

### 5. SemVer en el repo

- Regla nueva con `estado: stable` → bump MINOR del repo (ej. 1.0.0 → 1.1.0)
- Cambio breaking en una regla existente → bump MAJOR (ej. 1.x.x → 2.0.0)
- Corrección de typo, ejemplo nuevo, tag de fixture → bump PATCH

Cada release publica:
- PyPI: `md-osi-fiscal=={version}`
- npm: `@md/osi-fiscal-mx@{version}`

## Proceso para corrección menor (typo, doc fix)

PR directo, sin issue. Mantenedor revisa, aprueba, mergea. Sin cross-audit
para cambios non-fiscales.

## Cómo correr los tests localmente

```bash
git clone https://github.com/MarxCha/md-osi-fiscal-mx
cd md-osi-fiscal-mx

# Validar schema YAML
pip install -r implementations/python/requirements-dev.txt
python -m md_osi_fiscal.validate spec/

# Ejecutar test fixtures
pytest tests/
```

## Código de conducta

Trato profesional. Críticas a las reglas, no a las personas. Citar evidencia
es bienvenido; especular sin evidencia no.

## Licencia de tus contribuciones

Al abrir un PR aceptas que tu contribución se libere bajo Apache 2.0, igual
que el resto del repo.

## Contacto

**Marx Chávez** · CEO MD Consultoría SC · `mdsamca2025@gmail.com`
