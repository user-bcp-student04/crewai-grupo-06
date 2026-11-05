"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = "Implementa el recorrido del usuario según el contrato de API aprobado. \
Define campos, validaciones, acciones y mensajes. \
Cubre estados de carga, vacío, éxito y error, y evita envíos duplicados. \
Conserva etiquetas accesibles, navegación por teclado y foco visible. \
Incluye cómo comprobar el recorrido y sus errores. \
Entrega frontend_spec.md y código Angular con el formato de extracción que ya exige build_task."
agent = Agent(role='Desarrollador frontend Angular del portal de autenticación BCP',
              goal="Implementar en Angular el recorrido de usuario del Issue (formulario de login/autenticación) "
                   "según el contrato de API aprobado, cumpliendo sus criterios de aceptación, con estados de "
                   "carga, vacío, éxito y error, accesibilidad y pasos para verificarlo.",
              backstory="Eres un desarrollador frontend Angular del equipo que construye el portal de "
                        "autenticación del BCP. Consumes el contrato de API definido por Arquitectura y "
                        "Backend sin inventar endpoints ni campos, muestras al usuario los errores de la API "
                        "con mensajes claros, y cuidas la accesibilidad (etiquetas, teclado, foco visible) "
                        "y la prevención de envíos duplicados.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    'Especificación frontend_spec.md (campos, validaciones, acciones, mensajes, estados de '
                    'carga/vacío/éxito/error, accesibilidad y pasos para comprobar el recorrido y sus errores) '
                    'y código Angular en bloques markdown separados por archivo (p. ej. models.ts, '
                    'auth.service.ts, login.component.ts, login.component.html, login.component.css); '
                    'la primera línea de cada bloque con el nombre, como // auth.service.ts.'),
                agent=agent)
