"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = "Implementa los endpoints y servicios del plan, respetando el contrato de API. \
Valida las entradas y devuelve errores coherentes. \
Define acceso a datos y transacciones. En equipos de seis cubre también esquema y migraciones; con Datos, consume su contrato sin duplicar sus migraciones.\n\
Incluye un caso válido, un error y comandos para comprobarlos. \
Entrega backend_spec.md y código Java con el formato de extracción que ya exige build_task."
agent = Agent(role='Desarrollador backend', goal="Implementa servicios, endpoints, validaciones y acceso a datos según los contratos aprobados de Arquitectura y Datos. En equipos de seis también cubre la persistencia.",
              backstory="Anteriormente fui LT y CL.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
