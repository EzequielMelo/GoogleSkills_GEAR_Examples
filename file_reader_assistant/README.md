# File Reader Assistant

Este proyecto conecta un agente de Google ADK con un servidor MCP de sistema de archivos. El agente puede enumerar y leer los archivos de muestra de `my_files` mediante herramientas que proporciona el servidor, sin implementar esas operaciones en Python.

## Resumen del tema

MCP (*Model Context Protocol*) es un protocolo abierto para conectar aplicaciones de IA con servidores que ofrecen herramientas y otros recursos. El PDF del curso presenta dos formas de integrarlo con ADK: consumir herramientas de un servidor existente o exponer herramientas de ADK a otros clientes MCP. Este ejercicio practica la primera.

El recorrido es:

```text
Pregunta del usuario → agente ADK → McpToolset → servidor MCP de archivos
                    ← resultado de la herramienta ←
```

`McpToolset` establece la conexión y descubre las herramientas del servidor. El modelo puede elegir una de las herramientas disponibles, enviarle argumentos y usar el resultado para responder. En comparación con una función propia como `get_capital_city` de [`geography_assistant`](../geography_assistant/), aquí la implementación de lectura vive en un proceso externo.

## Configuración de este agente

El servidor local se inicia como subproceso mediante `npx` y se comunica con ADK por entrada y salida estándar (*stdio*):

```python
McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                str(ALLOWED_PATH),
            ],
        ),
        timeout=30.0,
    ),
    tool_filter=["list_directory", "read_file"],
)
```

`ALLOWED_PATH` se calcula a partir de la ubicación de `agent.py`, de modo que siempre apunta a `file_reader_assistant/my_files`, aunque `adk web` se lance desde la carpeta general. Esa ruta limita el acceso del servidor de archivos. `tool_filter` reduce además las herramientas que ve el agente a operaciones de listado y lectura; no se le ofrecen herramientas de escritura.

El valor `timeout=30.0` da tiempo al servidor para arrancar. El límite original de cinco segundos produjo un error de conexión cuando `npx` tardó más en iniciar el paquete.

## Pruebas del ejercicio

Dentro de `my_files` hay dos archivos de muestra: `hello.txt` y `notes.txt`. Después de iniciar el agente, prueba:

| Pregunta | Herramienta esperada |
| --- | --- |
| «¿Qué archivos hay en la carpeta?» | `list_directory` para mostrar los archivos disponibles. |
| «Muéstrame el contenido de hello.txt» | `read_file` para leer el archivo. |
| «Enumera los archivos y después lee notes.txt» | Primero `list_directory` y luego `read_file`. |

Puedes inspeccionar los eventos de ADK para comprobar qué herramienta se llamó y con qué ruta. La respuesta redactada por el modelo puede variar.

## Preparar el entorno

Activa el entorno virtual con el que ejecutas ADK e instala allí el soporte opcional para MCP:

```bash
cd ~/GEAR/adk-workspace
source .venv/bin/activate
python -m pip install 'google-adk[mcp]'
```

Comprueba que se puede importar el paquete:

```bash
python -c 'import mcp; print("MCP disponible")'
```

También necesitas Node.js y npm, que proporcionan `npx`. Compruébalos en **la misma terminal** donde iniciarás ADK:

```bash
node --version
npx --version
```

En WSL, usa una instalación de Node.js para Linux dentro de WSL. Una ruta de `npx` que apunte a `/mnt/c/Program Files/nodejs/` puede fallar; en nuestro entorno devolvió `WSL 1 is not supported`. Al instalar Node.js en Linux, verifica que `command -v node` y `command -v npx` apunten a ejecutables de Linux.

Configura también `GOOGLE_API_KEY` en el `.env` local del proyecto y ejecuta desde `adk-workspace`:

```bash
adk web
```

Selecciona `file_reader_assistant` en la interfaz.

## Si aparece un error

- `SyntaxError` al cargar `agent.py`: comprueba que la configuración use `instruction=`, con un solo signo igual.
- `ImportError` de `McpToolset` o `ModuleNotFoundError: mcp`: instala `google-adk[mcp]` en el mismo entorno virtual que ejecuta `adk web`.
- `timed out ... waiting for the session to become ready`: comprueba que `npx --version` funcione en esa terminal. El agente ya espera 30 segundos; la primera ejecución también puede requerir descargar el servidor con `npx -y` y acceso a la red.
- «Agent ... will run without the tools from toolset»: ADK no logró conectar con el servidor MCP. El modelo podría responder sin haber leído archivos; revisa la conexión antes de confiar en su respuesta.
- Una herramienta no aparece: comprueba el nombre que anuncia la versión instalada del servidor. `tool_filter` solo deja visibles los nombres incluidos en la lista.

## Archivos

- `agent.py`: configura el agente, la ruta permitida y la conexión MCP.
- `my_files/hello.txt` y `my_files/notes.txt`: archivos de ejemplo.
- `__init__.py`: permite que ADK cargue el proyecto.

El servidor MCP se descarga y ejecuta mediante `npx`; el repositorio no incluye su código. El `.gitignore` general excluye el `.env` y los archivos locales generados por ADK.
