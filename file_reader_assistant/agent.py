""" 
Agente asistente de lectura de archivos 
Demuestra la integración de herramientas del MCP con ADK utilizando el servidor MCP 
del sistema de archivos. 
Referencia: https://google.github.io/adk-docs/tools-custom/mcp-tools/ 
""" 

from pathlib import Path

from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset 
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams 
from mcp import StdioServerParameters

# Define la carpeta para permitir el acceso al archivo (debe ser una ruta de acceso absoluta) 
ALLOWED_PATH = Path(__file__).resolve().parent / "my_files"

# Crea la carpeta si no existe 
ALLOWED_PATH.mkdir(exist_ok=True)

root_agent = Agent(
    model='gemini-3.5-flash',
    name='file_reader_assistant',
    description='Ayuda a los usuarios a leer y explorar archivos con las herramientas del MCP.',
    instruction=""" 
    Eres un asistente de lectura de archivos que ayuda a los usuarios a explorar 
    archivos. 
    Tus capacidades: - Mostrar una lista de archivos en los directorios con list_directory - Leer el contenido del archivo con read_file 
    Cuando ayudes a los usuarios: 
    1. Utiliza list_directory para mostrar los archivos disponibles. 
    2. Utiliza read_file para mostrar el contenido del archivo cuando se te solicite. 
    3. Describe lo que encuentras de una manera útil. 
    Expresa con claridad cuál es la carpeta con la que estás trabajando. 
    """,
    tools=[ 
        McpToolset( 
            connection_params=StdioConnectionParams( 
                server_params=StdioServerParameters( 
                    command='npx', 
                    args=[ 
                        '-y', 
                        '@modelcontextprotocol/server-filesystem', 
                        str(ALLOWED_PATH),
                    ], 
                ), 
                timeout=30.0,
            ), 
            # Filtra para exponer únicamente herramientas seguras y de solo lectura 
            tool_filter=['list_directory', 'read_file'], 
        ) 
    ],
)
