"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Analiza el Issue, sus criterios de aceptación y las interfaces del producto que estén disponibles.
No inventes requisitos ni detalles de API. Distingue la información explícita de los supuestos y señala lo que falte como pregunta pendiente.

Entrega user_story.md con estas secciones:
1. Resumen del cambio y alcance.
2. Componentes afectados, sus responsabilidades y límites.
3. Contrato de API relevante: entradas, respuestas exitosas, errores y ejemplos. Si no puede determinarse, explica qué información falta.
4. Trazabilidad de cada criterio de aceptación hacia el componente responsable y una forma verificable de comprobarlo.
5. Supuestos y preguntas pendientes.

Mantén el diseño acotado al cambio solicitado y usa nombres y convenciones coherentes con las interfaces existentes."""
agent = Agent(role='Arquitecto', goal="Analiza el Issue y define una propuesta verificable de componentes, límites del cambio y contrato de API, trazando cada criterio de aceptación y haciendo explícitos los supuestos y datos faltantes.",
              backstory="Líder técnico .NET", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Una historia de usuario.', agent=agent)
