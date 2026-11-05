"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = "Relaciona cada criterio de aceptación con una prueba y su resultado esperado. \
Incluye casos positivos, negativos, de borde e integración. \
Detalla preparación, datos de prueba, comandos y limpieza. \
Comprueba los contratos de API y persistencia y las correcciones propuestas. \
Marca NO EJECUTADO cuando no tengas una salida real. No inventes resultados. \
Entrega testing_report.md, pruebas y comandos reproducibles."
agent = Agent(role='Ingeniero de pruebas del Issue',
              goal="Convertir cada criterio de aceptación del Issue en casos de prueba "
                   "verificables y comandos reproducibles, sin afirmar resultados no ejecutados.",
              backstory="Eres el ingeniero de pruebas del equipo. Recibes el Issue con sus criterios "
                        "de aceptación y las entregas aprobadas de Arquitectura, Backend y Frontend. "
                        "Tu informe no sustituye la ejecución: una persona correrá tus comandos "
                        "y adjuntará la salida real.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output="testing_report.md con una tabla criterio -> prueba -> resultado esperado "
                                "-> estado (NO EJECUTADO salvo salida real), casos positivos, negativos, "
                                "de borde e integración, preparación, datos, comandos y limpieza; "
                                "más el código de las pruebas en bloques con nombre de archivo.",
                agent=agent)
