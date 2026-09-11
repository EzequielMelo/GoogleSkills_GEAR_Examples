# Product Extractor

Este proyecto muestra cómo convertir texto libre en datos estructurados. El usuario describe un producto y el agente extrae su nombre, precio, almacenamiento y color en un objeto JSON con una forma predecible.

## Conceptos practicados

- Creación de un modelo `ProductInfo` con Pydantic.
- Declaración de tipos y descripciones mediante `BaseModel` y `Field`.
- Uso de `output_schema` para exigir una estructura concreta en la respuesta.
- Valores predeterminados para información opcional, como el color.
- Uso de `output_key` para guardar el resultado bajo `extracted_product` en el estado de la sesión.

## Cómo funciona

`ProductInfo` actúa como contrato de salida:

```python
class ProductInfo(BaseModel):
    product_name: str
    price: float
    storage: str
    color: str = "No se especifica"
```

Al pasar este modelo como `output_schema`, el agente no devuelve solamente una frase: produce datos que otras partes de una aplicación pueden validar y procesar. Los tipos también ayudan a evitar resultados ambiguos; por ejemplo, `price` debe ser numérico.

El parámetro `output_key="extracted_product"` indica a ADK que almacene la salida final en el estado de la sesión. Así, otro agente o un paso posterior del flujo puede reutilizar los datos extraídos.

## Archivos

- `agent.py`: contiene el esquema Pydantic y la configuración del agente.
- `__init__.py`: expone el módulo como un paquete de Python.

## Ejecutar el agente

Desde la carpeta que contiene todos los proyectos:

```bash
adk web
```

Selecciona `product_extractor` y prueba un mensaje como:

```text
Quiero el teléfono Example Pro de 256 GB en color negro por 999.99 dólares.
```

La respuesta debería respetar los campos definidos en `ProductInfo`.
