"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = (
    "Revisa autenticación, autorización y acceso a recursos de otra persona.\n"
    "Comprueba validación de entradas, inyección, secretos y exposición de datos sensibles.\n"
    "Para cada hallazgo indica archivo, ubicación, impacto, evidencia y corrección.\n"
    "Propón una comprobación reproducible de la corrección.\n"
    "Distingue riesgos detectados, correcciones propuestas y verificaciones realmente ejecutadas.\n"
    "Entrega security_report.md con hallazgos, correcciones y comprobaciones."
)
agent = Agent(role='Revisor de seguridad de aplicaciones',
              goal="Revisar autenticación, autorización, validación de entradas, manejo de secretos, "
                   "datos sensibles e inyección, y entregar hallazgos priorizados, correcciones "
                   "concretas y comprobaciones para verificarlas.",
              backstory="Eres un Quality Engineer del equipo, encargado de cumplir los estándares "
                        "de calidad y de verificar que cada entrega cumpla los requisitos de seguridad.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Informe security_report.md con hallazgos (archivo, ubicación, impacto, '
                                'evidencia, corrección), comprobaciones reproducibles y una distinción '
                                'entre riesgos detectados, correcciones propuestas y verificaciones ejecutadas.', agent=agent)
