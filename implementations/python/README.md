# md-osi-fiscal — implementación Python

Implementación de referencia que carga y valida los YAML de `spec/` desde
disco. Usado por productos del Stack Fiscal MD para acceder a las reglas y
dominios sin parsear el YAML manualmente.

## Instalación

```bash
pip install md-osi-fiscal  # cuando se publique a PyPI
```

Para desarrollo:

```bash
cd implementations/python
pip install -e .
```

## Uso

```python
from md_osi_fiscal import load_regla, list_reglas, load_domain

# Cargar una regla por ID
regla = load_regla("RN-001")
print(regla.descripcion)
print(regla.base_legal[0].ley, regla.base_legal[0].articulo)

# Listar todas las reglas estables
for r in list_reglas(estado="stable"):
    print(f"{r.id}: {r.nombre}")

# Cargar un dominio semántico
dom = load_domain("iva_cobrado")
for t in dom.terminos:
    print(f"  {t.id}: {t.definicion[:80]}...")
```
