# Context Engineering Experiment
**Curso:** Ingeniería de Software Asistida por IA — UADY  
**Práctica:** ADA-03 — Context Engineering Experiment  
**Elaborado por:** Rubén Alejandro Pérez Zumárraga  
**Herramienta:** Agy
**Fecha:** 8 de septiembre de 2026  

---

## Hypothesis

Al estructurar y proporcionar contexto explícito (especificación formal de requisitos en `SPEC.md` y reglas de proceso y calidad en `AGENTS.md`), un *coding agent* mejorará su eficiencia operativa (menor número de iteraciones y tiempo de resolución), reducirá la incertidumbre o conductas erráticas (como intentar descifrar archivos binarios o depender de inferencias basadas solo en aserciones de pruebas), y producirá una implementación de mayor calidad de software (validaciones más robustas, respeto a la persistencia y arquitecturas de dominio).

---

## Experimental Setup

- **Plataforma / Agente:** Antigravity CLI (agy) / Gemini 3.8 Flash (High)
- **Editor / Entorno:** macOS / VS Code / Python 3.14 con entorno virtual (`.venv`)
- **Herramienta de pruebas:** `pytest 9.1.1`
- **Control de versiones:** Git
- **Base experimental inicial (Commit `a210be2` - "Initial experimental baseline"):**
  - `README.md` (documentación de Customer API)
  - `src/customer.py` (dataclass `Customer` y stub `update_customer_email`)
  - `src/repository.py` (clase `CustomerRepository` con métodos `add`, `get`, `save`, `update_email`)
  - `tests/test_customer.py` (2 pruebas: preservación de ID/auditoría y rechazo de email inválido)
  - `tests/test_repository.py` (2 pruebas: cliente inexistente y preservación de ID en repositorio)
- **Línea base previa a la ejecución:** 2 pruebas aprobadas, 2 pruebas fallidas (esperado por falta de validación de email y minúsculas).
- **Aislamiento experimental:** Tres copias idénticas e independientes generadas a partir de la línea base en `experiments/A-minimal/`, `experiments/B-repository/` y `experiments/C-engineered/`.

---

## A — Minimal Context

### Prompt:
```text
Implement the customer email update functionality.
Inspect the repository first. Implement the necessary changes and run the tests.
```

### Results:
- **Tests iniciales:** 2 fallidos, 2 aprobados.
- **Tests finales:** 4 aprobados (100%).
- **Archivos modificados:** `src/customer.py`, `src/repository.py`.
- **Iteraciones / Tool calls:** 44 llamadas a herramientas.
- **Tiempo de ejecución:** 138 segundos (~2 min 18 s).

### Human intervention:
- 0 intervenciones humanas.

### Score:
- **Score:** 97 / 100 (9.7 / 10)
  - *Correctness:* 30/30 (pasan todas las pruebas).
  - *Requirements:* 20/20 (cumple los 7 requisitos funcionales).
  - *Minimal Change:* 15/15 (modificó solo los archivos necesarios).
  - *Maintainability:* 14/15 (código limpio pero faltó persistencia formal con `self.save()`).
  - *Security/Safety:* 9/10 (regex funcional pero básica).
  - *Verification:* 9/10 (verificó pruebas pero sin proceso metódico antes/después documentado).

### Observations:
El agente carecía por completo de especificaciones o restricciones. Al inspeccionar el entorno de trabajo, notó un archivo PDF de la práctica en el directorio superior (`ADA-03_Context_Engineering_Autocontenido.pdf`) e invirtió más de 16 llamadas a herramientas ejecutando scripts en Python con `zlib` y `regex` para descompilar streams binarios e intentar leer los requerimientos exactos. Aunque finalmente resolvió la tarea modificando los dos archivos, incurrió en un costo cognitivo y de latencia muy elevado debido al contexto insuficiente.

---

## B — Repository Context

### Prompt:
```text
Implement the customer email update functionality.
Before making changes:
1. Inspect the repository.
2. Read README.md.
3. Inspect all relevant source files.
4. Inspect the tests.
5. Infer expected behavior from the code and tests.
6. Run tests before changing code.
7. Make the smallest necessary implementation.
8. Run tests again.
9. Explain which repository information influenced the implementation.
```

### Results:
- **Tests iniciales:** 2 fallidos, 2 aprobados.
- **Tests finales:** 4 aprobados (100%).
- **Archivos modificados:** `src/customer.py`, `src/repository.py`.
- **Iteraciones / Tool calls:** 21 llamadas a herramientas (reducción de más del 52% respecto a A).
- **Tiempo de ejecución:** 51 segundos (reducción de más del 63% respecto a A).

### Human intervention:
- 0 intervenciones humanas.

### Score:
- **Score:** 98 / 100 (9.8 / 10)
  - *Correctness:* 30/30.
  - *Requirements:* 20/20.
  - *Minimal Change:* 15/15.
  - *Maintainability:* 14/15.
  - *Security/Safety:* 9/10.
  - *Verification:* 10/10 (ejecución estricta de pruebas antes y después).

### Observations:
Proporcionar un flujo estructurado de pasos en el prompt (Chain-of-Thought guiado al repositorio) eliminó por completo la deriva errática. El agente no intentó buscar archivos externos, sino que inspeccionó metódicamente `README.md`, el código fuente y las aserciones de `tests/`, infiriendo correctamente el contrato de excepciones (`ValueError("invalid-email")`), la normalización a minúsculas y la separación de responsabilidades entre dominio y repositorio.

---

## C — Engineered Context

### Contexto Diseñado Incluido:
1. **`SPEC.md`**: Especificación formal de objetivos, requisitos funcionales (validación de email, lowercasing, inmutabilidad de ID y `created_by`, actualización de `updated_by`) y criterios de aceptación específicos.
2. **`AGENTS.md`**: Directrices de comportamiento (mantener cambios mínimos, no alterar tests, correr `pytest` antes y después, reportar hallazgos y respetar puertas de calidad).

### Prompt:
```text
Implement the customer email update functionality.
Follow SPEC.md and AGENTS.md.
Inspect the repository first, run tests before and after changes, and explain your verification.
```

### Results:
- **Tests iniciales:** 2 fallidos, 2 aprobados.
- **Tests finales:** 4 aprobados (100%).
- **Archivos modificados:** `src/customer.py`, `src/repository.py`.
- **Iteraciones / Tool calls:** 25 llamadas a herramientas.
- **Tiempo de ejecución:** 72 segundos.

### Human intervention:
- 0 intervenciones humanas.

### Score:
- **Score:** 100 / 100 (10.0 / 10)
  - *Correctness:* 30/30 (100% pruebas superadas).
  - *Requirements:* 20/20 (los 7 requisitos cumplidos rigurosamente).
  - *Minimal Change:* 15/15 (modificación precisa y focalizada).
  - *Maintainability:* 15/15 (arquitectura ejemplar: llamó a `self.save(updated_customer)` y verificó `None` defensivamente en la entidad).
  - *Security/Safety:* 10/10 (expresión regular robusta `r"^[^@\s]+@[^@\s\.]+(\.[^@\s\.]+)+$"`, previniendo inyecciones y dominios malformados con puntos consecutivos).
  - *Verification:* 10/10 (verificación antes, después y cobertura adicional de casos borde de la especificación).

### Observations:
Fue la ejecución con mayor nivel de madurez en ingeniería de software. Al contar con `SPEC.md`, el agente no tuvo que adivinar qué validaciones de email aplicar ni qué excepciones lanzar ante clientes inexistentes. Cumplió con todas las reglas de `AGENTS.md`: ejecutó pruebas iniciales de diagnóstico, aplicó el cambio mínimo seguro, persistió explícitamente en el repositorio (`self.save`) y ejecutó validaciones adicionales sobre casos de borde descritos en la especificación.

---

## Comparative Results

### Tabla de Métricas (Sección 16)

| Métrica | A (Minimal Context) | B (Repository Context) | C (Engineered Context) |
|:---|:---:|:---:|:---:|
| **Tests passing** | 4 / 4 | 4 / 4 | 4 / 4 |
| **Tests failing** | 0 | 0 | 0 |
| **Requisitos cumplidos (de 7)** | 7 / 7 | 7 / 7 | 7 / 7 |
| **Archivos modificados** | 2 (`src/customer.py`, `src/repository.py`) | 2 (`src/customer.py`, `src/repository.py`) | 2 (`src/customer.py`, `src/repository.py`) |
| **Cambios innecesarios** | 0 | 0 | 0 |
| **Iteraciones (Tool Calls)** | 44 | 21 | 25 |
| **Intervenciones humanas** | 0 | 0 | 0 |
| **Problemas introducidos** | 0 | 0 | 0 |
| **Tiempo de resolución** | 138 s (~2m 18s) | 51 s (~0m 51s) | 72 s (~1m 12s) |
| **Context Engineering Score (/10)** | **9.7** | **9.8** | **10.0** |

### Desglose de Puntuación (Sección 17)

| Criterio | Puntos Máx. | A (Minimal) | B (Repository) | C (Engineered) |
|:---|:---:|:---:|:---:|:---:|
| **Correctness** | 30 | 30 | 30 | 30 |
| **Requirements** | 20 | 20 | 20 | 20 |
| **Minimal Change** | 15 | 15 | 15 | 15 |
| **Maintainability** | 15 | 14 | 14 | 15 |
| **Security/Safety** | 10 | 9 | 9 | 10 |
| **Verification** | 10 | 9 | 10 | 10 |
| **Total (/100)** | **100** | **97** | **98** | **100** |

---

## Error Analysis

1. **Ambigüedad y exploración dispersa en A:**
   Al no proveer especificación ni instrucciones sobre cómo validar, el agente en A invirtió cerca del 40% de sus operaciones en tratar de extraer información de un PDF fuera de su alcance, provocando retrasos y desperdicio computacional innecesario.
2. **Omisión de persistencia explícita en A y B:**
   En A y B, el método `CustomerRepository.update_email` simplemente retornó la mutación en memoria del objeto `Customer`, omitiendo llamar a `self.save(customer)`. En un repositorio real (con base de datos o almacenamiento persistente), este cambio no se habría guardado. Solo en C, gracias a las reglas explícitas y buenas prácticas, se implementó `self.save()`.
3. **Calidad de validación sintáctica:**
   La expresión regular de A y B (`r"^[^@\s]+@[^@\s]+\.[^@\s]+$"`) aceptaba dobles puntos en el dominio (ej. `user@domain..com`). En C, la especificación explícita llevó al agente a aplicar una regex más estricta (`r"^[^@\s]+@[^@\s\.]+(\.[^@\s\.]+)+$"`).

---

## Context Quality Analysis

- **Mínimo vs. Guiado vs. Diseñado:** 
  - El contexto mínimo obliga al modelo a compensar la falta de información asumiendo o buscando pistas en el entorno (alto riesgo de alucinación o sobre-ingeniería).
  - El contexto de repositorio guía el razonamiento (*process engineering*), lo que hace la ejecución rápida y concisa, pero depende exclusivamente de qué tan bien esté escrito el código existente.
  - El contexto diseñado (`SPEC.md` + `AGENTS.md`) define el contrato formal y las reglas de negocio antes de tocar código, alineando perfectamente el resultado con los estándares del equipo.

---

## Preguntas de Análisis (Sección 19)

### 1. ¿Cuál fue tu hipótesis?
Que diseñar y entregar un contexto explícito y estructurado (`SPEC.md` y `AGENTS.md`) reduce drásticamente las iteraciones erráticas del agente, disminuye el tiempo de desarrollo y eleva la calidad técnica y de seguridad de la solución implementada.

### 2. ¿Cuál experimento produjo el mejor resultado y por qué?
El **Experimento C (Engineered Context)**. Produjo la solución más robusta y segura: validó exhaustivamente los formatos de email, verificó defensivamente la existencia del cliente, respetó el contrato de persistencia con `self.save()` y validó casos límite descritos en la especificación.

### 3. ¿Qué errores aparecieron en A y no en C?
En A el agente sufrió desorientación sobre el alcance de la validación sintáctica requerida y desvió tiempo valioso intentando desensamblar un archivo PDF binario para averiguar qué esperaba el evaluador. En C, el agente fue directo al código guiado por `SPEC.md`.

### 4. ¿Qué información del repositorio fue más útil?
Los archivos de pruebas en `tests/`. Revelaron de inmediato los nombres exactos de las excepciones esperadas (`ValueError("invalid-email")` y `ValueError("customer-not-found")`), así como el requisito de normalización a minúsculas (`NEW@example.com` -> `new@example.com`).

### 5. ¿Qué aportó SPEC.md?
Definió los requisitos funcionales completos y criterios de aceptación no ambivalentes: validación sintáctica estricta, conversión a minúsculas, invariabilidad de identificadores y manejo de ausencias sin depender de la intuición del modelo.

### 6. ¿Qué función tuvo AGENTS.md?
Estableció las reglas de operación (*governance* y *quality gates*): instruyó correr `pytest` antes y después, prohibió modificar pruebas preexistentes para forzar aprobaciones espurias, y obligó a mantener la modificación mínima necesaria.

### 7. ¿Más contexto significa necesariamente mejor contexto?
No. Más contexto no estructurado o ruidoso (como arrojar documentación irrelevante, archivos binarios o prompts sobrecargados) satura la ventana de atención y puede confundir al modelo. El contexto de calidad es sintético, modular, específico y ubicado donde el agente opera.

### 8. ¿Qué información fue redundante?
En las pruebas y en el código de ejemplo existía información duplicada sobre cómo instanciar `Customer`. Además, la presencia del PDF en el directorio superior actuó como un distractor ruidoso para el agente en el Experimento A.

### 9. ¿Qué intervención humana fue necesaria?
Cero intervenciones durante las ejecuciones de los tres agentes. Toda la interacción se limitó a preparar los entornos limpios iniciales y suministrar los prompts y archivos de contexto correspondientes.

### 10. ¿Qué cambiarías en SPEC.md y AGENTS.md?
- En `SPEC.md`: Especificar explícitamente el estándar regex RFC 5322 o una regla clara para dominios (ej. rechazar dominios sin TLD de al menos 2 letras).
- En `AGENTS.md`: Añadir una directriz explícita para generar pruebas unitarias adicionales que cubran los nuevos criterios de aceptación sin alterar los tests originales.

### 11. ¿Qué aprendiste sobre la responsabilidad del desarrollador al usar agentes?
El desarrollador deja de ser un mero escritor de sintaxis para convertirse en un arquitecto de contexto y auditor de calidad. Si nosotros como desarrolladores no definimos con rigor los límites, contratos y compuertas de validación, el agente puede generar código superficial que pase los tests presentes pero falle en producción o degrade la arquitectura del sistema.

---

## Pregunta Final (Sección 21)

> **En máximo 200 palabras: ¿por qué un desarrollador que utiliza agentes de código necesita aprender Context Engineering y no solamente mejores prompts?**

Los prompts son instrucciones efímeras dirigidas a un único turno de conversación; no escalan a lo largo de un proyecto ni definen la arquitectura subyacente. En cambio, **Context Engineering** diseña sistemáticamente el ecosistema de información que alimenta al agente: especificaciones funcionales (`SPEC.md`), directrices de calidad y gobernanza (`AGENTS.md`), límites arquitectónicos y suites de verificación automatizada.

Un buen prompt puede sugerirle al modelo qué hacer en un momento dado, pero un contexto diseñado garantiza que cualquier agente comprenda las restricciones de dominio, respete los contratos existentes, reduzca la exploración errática y valide su propia solución de forma determinista y reproducible. Desarrollar con agentes sin Context Engineering es delegar a ciegas; con Context Engineering, el desarrollador conserva el control de la calidad, mantenibilidad y seguridad del software.

---

## Conclusions

1. **Contexto Diseñado frente a Contexto Mínimo:** La ingeniería de contexto disminuyó a la mitad el número de llamadas a herramientas y evitó conductas exploratorias no deseadas, mejorando la seguridad del código generado.
2. **Autonomía Confiable:** Separar las directrices de proceso (`AGENTS.md`) de los requisitos funcionales (`SPEC.md`) permite reutilizar reglas de calidad en múltiples tareas sin reescribir prompts desde cero.

---

## What I Would Change

Para futuras iteraciones del experimento:
1. Incluir un linter o formateador (`ruff` o `flake8`) como compuerta de calidad adicional en `AGENTS.md`.
2. Probar tareas de mayor complejidad arquitectónica (persistencia en base de datos real o APIs asíncronas) para evaluar cómo escala la degradación del agente en ausencia de contexto diseñado.
