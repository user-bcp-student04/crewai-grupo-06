"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'chapter'
LABEL = 'Chapter'
SPEC_FILE = 'chapter_review.md'
EXTRACT_CODE = False

INSTRUCTIONS = "Contrasta cada criterio de aceptación con arquitectura, persistencia, implementación, pruebas y seguridad.\n" \
               "Detecta contratos incompatibles, criterios sin cobertura y hallazgos pendientes.\n" \
               "Para cada observación indica responsable, cambio requerido y cómo verificarlo.\n" \
               "Justifica el veredicto con evidencia y señala las pruebas pendientes.\n" \
               "Conserva las aprobaciones humanas; tu informe no las sustituye.\n" \
               "Entrega chapter_review.md con VEREDICTO: APROBADO o RECHAZADO, motivos y correcciones."
agent = Agent(role='Chapter: revisor transversal del Issue',
              goal="Verificar que el Issue cumple todos sus criterios de aceptación en arquitectura, "
                   "persistencia, implementación, pruebas y seguridad, y emitir un veredicto justificado.",
              backstory="Eres el revisor de calidad del equipo. Auditas el trabajo entregado contra el Issue "
                        "con evidencia concreta, asignas responsables a cada hallazgo y nunca sustituyes "
                        "las aprobaciones humanas.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Contenido de chapter_review.md: cobertura por criterio de aceptación, '
                                'observaciones (responsable, cambio requerido, verificación), pruebas pendientes, '
                                'evidencia y una línea final "VEREDICTO: APROBADO" o "VEREDICTO: RECHAZADO" con motivos y correcciones.',
                agent=agent)
