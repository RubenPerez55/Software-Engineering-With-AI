# AI Usage Log — Registro de Uso de Inteligencia Artificial
**Asignatura:** Ingeniería de Software Asistida por IA · UADY  
**Actividad:** ADA-04 — Revisión de Especificaciones  
**Estudiante:** Rubén Pérez  
**Fecha:** 11 de septiembre de 2026  

---

## Propósito del AI Usage Log
Conforme a las directrices metodológicas de la práctica ADA-04 (secciones 10.1 y 12), este documento hace explícita la trazabilidad técnica de cómo el estudiante dirigió, evaluó, cuestionó y aprovechó herramientas de inteligencia artificial generativa en tareas de ingeniería de requerimientos. El modelo operó como un asistente analítico de alta velocidad bajo la continua supervisión y validación crítica del estudiante, quien ejerció la toma de decisiones, la delimitación de alcance y la responsabilidad sobre los requisitos formalizados.

---

### Entry 01 — Análisis Crítico Inicial y Detección de Ambigüedades
- **Etapa:** Requirements Analysis
- **Herramienta / Modelo:** Antigravity CLI / Gemini 3.8 Flash (High)
- **Fecha:** 2026-09-11
- **Prompt / Objetivo:**
  > *"Actúa como Senior Requirements Engineer. Ejecuta un análisis crítico exhaustivo de la siguiente especificación preliminar para 'Customer Search'. Identifica ambigüedades semánticas, vacíos de especificación, adjetivos no medibles, ausencia de criterios de aceptación verificables, preocupaciones de seguridad/privacidad (PII) y preguntas abiertas que deban escalarse al Product Owner. Separa de forma estricta las observaciones basadas en hechos de las recomendaciones técnicas de arquitectura:*  
  > *FEATURE: Customer Search*  
  > *We need a customer search feature for the application.*  
  > *The user should be able to search customers quickly by name or email.*  
  > *The search should be easy to use and return relevant results.*  
  > *It should support partial matches and work well with large numbers of customers.*  
  > *Results should be displayed in a useful order, with the most relevant customers first.*  
  > *If no customers are found, show an appropriate message.*  
  > *The search should be secure and should not expose sensitive customer information.*  
  > *It should be fast enough for normal use.*  
  > *The feature should work on mobile and desktop."*
- **Contribución de la IA:**
  La IA desglosó sistemáticamente la especificación identificando 14 términos ambiguos y no medibles (`quickly`, `by name`, `or email`, `easy to use`, `relevant results`, `partial matches`, `large numbers`, `useful order`, `appropriate message`, `secure`, `sensitive info`, `fast enough`, etc.). Evidenció la imposibilidad de automatizar pruebas con la redacción actual y presentó una categorización preliminar de riesgos operativos.
- **Decisión del estudiante:**
  Evalué y acepté las 14 observaciones técnicas. Determiné prioritario incorporar el análisis sobre la arquitectura de entrada (unificación de campo de búsqueda vs filtros independientes) y exigí especificar el tratamiento de acentos diacríticos y caracteres especiales en español (tildes y eñes), omisión frecuente en requerimientos redactados originalmente en inglés para mercados latinoamericanos.
- **Impacto:**
  Estructuración formal de la matriz del **Paso 1** (14 ambigüedades con descripción de problema, justificación de impacto técnico y pregunta de resolución) y establecimiento de las bases para las preguntas clave dirigidas al Product Owner.

---

### Entry 02 — Clasificación Taxonómica, Casos Límite y Atributos de Calidad (NFRs)
- **Etapa:** Specification & Quality Attributes (NFRs)
- **Herramienta / Modelo:** Antigravity CLI / Gemini 3.8 Flash (High)
- **Fecha:** 2026-09-11
- **Prompt / Objetivo:**
  > *"Procede con la ejecución y estructuración técnica del laboratorio ADA-04 conforme a las directrices de la UADY: clasifica los problemas detectados dentro de la taxonomía oficial de 9 categorías, delimita exhaustivamente los casos de borde operativos (incluyendo normalización diacrítica, mitigación de inyecciones y control de race conditions asíncronas en frontend), y formula los atributos de calidad (NFRs) cuantitativos requeridos. Asumo el rol de Lead Engineer para auditar y validar cada una de las definiciones."*
- **Contribución de la IA:**
  1. Clasificó los 15 hallazgos dentro de las 9 categorías oficiales de ingeniería de requerimientos de la UADY.
  2. Modeló 8 casos límite fundamentales: consultas vacías, sanitización de espacios con `trim()`, normalización de diacríticos (`unaccent`), neutralización de wildcards e inyecciones SQL/XSS, tratamiento de estados vacíos, paginación defensiva ante grandes volúmenes, race conditions en typeahead y resolución de homónimos.
  3. Propuso 4 requisitos no funcionales cuantitativos (latencia P95 < 200 ms bajo 150 QPS, mitigación estricta de inyecciones, rate limiting de 30 req/min y debounce de 300 ms en frontend).
- **Decisión del estudiante:**
  Audité los casos límite y los NFRs propuestos:
  - Ratifiqué el uso de `AbortController` en capa de transporte frontend para garantizar consistencia visual ante peticiones asíncronas concurrentes.
  - Aprobé fijar la longitud mínima de búsqueda en 3 caracteres netos para proteger el motor de persistencia contra escaneos de tabla completa (*full table scans*).
  - Rechacé que la IA asumiera decisiones de negocio arbitrarias sobre el contenido del estado vacío o el despliegue de historiales de búsqueda; clasifiqué dichos aspectos formalmente como **Preguntas Abiertas para el Product Owner**.
- **Impacto:**
  Consolidación de las matrices del **Paso 2 (Clasificación de problemas)**, **Paso 5 (Casos límite)** y definición cuantitativa de los 4 Requisitos No Funcionales (NFR-01 a NFR-04).

---

### Entry 03 — Formalización de Requisitos Funcionales y Criterios Given / When / Then
- **Etapa:** Requirements Verification & Acceptance Criteria
- **Herramienta / Modelo:** Antigravity CLI / Gemini 3.8 Flash (High)
- **Fecha:** 2026-09-11
- **Prompt / Objetivo:**
  > *"Sintetiza los hallazgos en al menos 8 Requisitos Funcionales (FR-01 a FR-08) y 4 No Funcionales (NFR-01 a NFR-04) completamente desacoplados de implementaciones prematuras, acompañados de su método objetivo de verificación. Asimismo, formaliza al menos 6 Criterios de Aceptación ejecutables bajo el estándar BDD en sintaxis Given / When / Then, asegurando cobertura sobre casos de éxito, estados vacíos interactivos, control volumétrico de paginación y directivas de seguridad por diseño para mitigación de fuga de PII."*
- **Contribución de la IA:**
  Redactó los 8 requisitos funcionales y formuló los 6 criterios de aceptación en sintaxis Gherkin estándar, detallando precondiciones, disparadores y postcondiciones verificables para coincidencia insensible a diacríticos, prefijos de correo, throttling de entrada, paginación con metadatos y listas blancas de datos autorizados.
- **Decisión del estudiante:**
  Validé y afiné la redacción de los requisitos y criterios de aceptación:
  - Exigí que cada requisito funcional y no funcional incorporara un método de comprobación comprobable mediante suites de testing reales (Playwright, Cypress, k6, analizadores de schema JSON).
  - En el criterio AC-04, obligué a que el estado vacío contara con un componente de acción interactivo ("Limpiar búsqueda") para evitar puntos muertos en el flujo del usuario.
  - En el criterio AC-06, reforcé la política de privacidad por diseño especificando el formato exacto de enmascaramiento telefónico (`***-***-1234`) y prohibiendo expresamente la presencia de identificadores fiscales o bancarios en el DOM y payload de respuesta.
- **Impacto:**
  Aprobación técnica definitiva de las tablas de **Requisitos Verificables (Paso 3)** y **Criterios de Aceptación BDD (Paso 4)** en el informe de ingeniería.

---

### Entry 04 — Consolidación de Artefactos, Inspección en IDE y Compilación de Entrega
- **Etapa:** Documentation & Deliverable Review
- **Herramienta / Modelo:** Antigravity CLI / Gemini 3.8 Flash (High)
- **Fecha:** 2026-09-11
- **Prompt / Objetivo:**
  > *"Consolida todos los artefactos de ingeniería generados en el espacio de trabajo: compila el informe técnico formal en Markdown, automatiza la generación del entregable oficial en PDF conforme al estándar de entrega de ADA-04 mediante un script ejecutable, y estructura la bitácora de trazabilidad de uso de IA (AI Usage Log) reflejando la dirección técnica, evaluación crítica de decisiones y el gobierno del flujo de trabajo."*
- **Contribución de la IA:**
  1. Estructuró el documento maestro `ADA_04_Specification_Review_RubenPerez.md`.
  2. Diseñó e implementó el script `generate_pdf.py` con ReportLab para compilar el documento oficial `ADA_04_Specification_Review_RubenPerez.pdf` con maquetación académica, encabezados dinámicos y numeración automatizada.
  3. Ejecutó el comando de entorno para abrir el proyecto en Visual Studio Code e implementó esta bitácora independiente `AI_USAGE_LOG.md`.
- **Decisión del estudiante:**
  Realicé una inspección visual y técnica de los artefactos directamente en VS Code. Verifiqué la coherencia entre las tablas de requerimientos, la ausencia de supuestos no justificados, la integridad visual del PDF compilado y la fidelidad del AI Usage Log respecto al proceso de ingeniería ejecutado.
- **Impacto:**
  Generación, verificación y disponibilidad del paquete completo de entrega del laboratorio: `ADA_04_Specification_Review_RubenPerez.pdf`, `ADA_04_Specification_Review_RubenPerez.md`, `AI_USAGE_LOG.md` y `generate_pdf.py`.

---

## Síntesis de Trazabilidad y Aprendizaje de Ingeniería
1. **Gobierno del Flujo por el Ingeniero:** La inteligencia artificial proporcionó aceleración analítica en la detección exhaustiva de ambigüedades, pero la delimitación de soluciones, la definición de umbrales cuantitativos y la separación entre arquitectura y reglas de negocio dependieron enteramente de la dirección crítica humana.
2. **Robustez y Verificabilidad:** La transformación de enunciados vagos en criterios BDD y métricas no funcionales tangibles (latencia percentilada, pruebas de carga con k6 y mitigación DAST) demuestra la transición efectiva desde una especificación informal hacia requerimientos comprobables de nivel de producción.
3. **Evidencia Académica:** Este registro cumple rigurosamente con los estándares éticos, metodológicos y formativos estipulados en las secciones 10.1 y 12 del programa ADA-04 de la Universidad Autónoma de Yucatán.
