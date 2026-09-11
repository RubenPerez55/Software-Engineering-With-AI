# ADA-04: Revisión de Especificaciones
**Ingeniería de Software Asistida por IA · UADY**  
**Estudiante:** Rubén Pérez  
**Fecha:** 11 de septiembre de 2026  
**Secuencia:** Detectar ambigüedad → Convertir requisitos en comportamiento verificable  

---

## 1. Introducción y Objetivo de la Práctica

El presente informe documenta el análisis crítico y formalización de una especificación de requerimientos de software deliberadamente ambigua para la funcionalidad de **Customer Search (Búsqueda de Clientes)**. 

Utilizando modelos de inteligencia artificial como herramientas de análisis asistido, se procedió a identificar ambigüedades, vacíos de información, riesgos de seguridad y limitaciones no funcionales. Como estudiante e ingeniero de software responsable, se dirigió y cuestionó activamente el análisis de la IA, contrastando sus propuestas y traduciendo el lenguaje subjetivo en especificaciones objetivas, medibles y verificables mediante pruebas automatizadas.

---

## 2. Especificación Original Deliberadamente Ambigua

> **FEATURE: Customer Search**  
> We need a customer search feature for the application.  
> The user should be able to search customers quickly by name or email.  
> The search should be easy to use and return relevant results.  
> It should support partial matches and work well with large numbers of customers.  
> Results should be displayed in a useful order, with the most relevant customers first.  
> If no customers are found, show an appropriate message.  
> The search should be secure and should not expose sensitive customer information.  
> It should be fast enough for normal use.  
> The feature should work on mobile and desktop.  

---

## 3. Paso 1 — Identificación de Ambigüedades y Términos No Verificables

Se identificaron **14 elementos** en la especificación que resultan ambiguos, incompletos, subjetivos o imposibles de verificar sin definiciones adicionales:

| # | Elemento | Problema detectado | ¿Por qué representa un problema? | Pregunta a resolver |
|:---:|:---|:---|:---|:---|
| **1** | `quickly` | No existe una métrica de tiempo cuantitativa ni percentil de medición. | No permite determinar objetivamente si el sistema cumple el requisito; una respuesta de 2 segundos puede ser rápida para un proceso batch pero inaceptable para una búsqueda interactiva. | ¿Cuál es el tiempo máximo de respuesta aceptable (SLA/latencia) y bajo qué percentil (ej. P95 < 250 ms)? |
| **2** | `by name` | No define qué componentes del nombre se buscan ni el tratamiento de diacríticos o nombres compuestos. | El desarrollador puede buscar solo en `first_name` ignorando `last_name`, o no soportar acentos ("Pérez" vs "Perez") provocando falsos negativos. | ¿La búsqueda evalúa `first_name`, `last_name` o nombre completo concatenado? ¿Es insensible a acentos diacríticos? |
| **3** | `or email` | No define si busca coincidencia exacta, prefijo de usuario o cualquier subcadena en el dominio. | Permitir subcadenas en dominios comunes (ej. "gmail") retornará miles de coincidencias espurias y degradará la base de datos. | ¿La búsqueda por email debe exigir coincidencia exacta, prefijo de cuenta (`usuario@`) o subcadena completa? |
| **4** | `name or email` | No define si la búsqueda ocurre en un campo de texto unificado o en campos independientes. | Impacta la arquitectura de interfaz (UI) y la lógica de backend (unificación con heurísticas de parsing vs filtros específicos). | ¿Se proporcionará una barra de búsqueda única inteligente o filtros separados para nombre y email? |
| **5** | `easy to use` | Expresión subjetiva e indemostrable sin una métrica de usabilidad estandarizada. | No puede formularse como prueba automatizada ni criterio de aceptación verificable; queda sujeta a la percepción de cada individuo. | ¿Qué estándar de usabilidad o métricas de UX (ej. máximo de 2 clics para consultar, SUS > 80, cumplimiento WCAG 2.1 AA) se aplicarán? |
| **6** | `relevant results` | No define el algoritmo ni los criterios matemáticos de relevancia (*scoring*). | Dos ingenieros implementarán algoritmos distintos (coincidencia exacta vs prefijo vs distancia Levenshtein/trigramas), alterando los resultados. | ¿Cuál es la ponderación algorítmica de relevancia (coincidencia exacta > prefijo > subcadena) y qué variables de negocio la modifican? |
| **7** | `partial matches` | No delimita si es coincidencia por prefijo, infijo (subcadena interna) o tolerancia a fallas tipográficas (*fuzzy search*). | Búsquedas por subcadena arbitraria (`%termino%`) impiden el uso óptimo de índices B-Tree en bases de datos relacionales, causando escaneos de tabla completa. | ¿Qué tipo específico de coincidencia parcial se requiere y cuál es la longitud mínima de caracteres para activarla? |
| **8** | `large numbers of customers` | No cuantifica el volumen de datos de clientes ni la tasa de crecimiento anual. | La solución arquitectónica para 10,000 registros es elemental; para 20 millones de clientes exige motores de búsqueda indexada (Elasticsearch) y particionamiento. | ¿Cuál es la cardinalidad actual de clientes en base de datos y cuál es el volumen proyectado a 3 años? |
| **9** | `useful order` | Adjetivo ambiguo y dependiente del perfil o rol de quien realiza la búsqueda. | El orden "útil" para un agente de soporte telefónico difiere del de un auditor financiero o un ejecutivo comercial. | ¿Cuál es el ordenamiento predeterminado (relevancia, alfabético, actividad reciente) y qué opciones de ordenamiento dinámico tendrá el usuario? |
| **10** | `most relevant customers first` | No define regla de desempate (*tie-breaking*) cuando múltiples registros poseen idéntica relevancia. | Puede ocasionar que el orden devuelto por la base de datos no sea determinista entre consultas idénticas consecutivas. | ¿Qué criterio secundario y determinista se aplicará para desempatar (ej. ID de cliente descendente o apellido alfabético)? |
| **11** | `appropriate message` | No especifica el texto exacto, tono ni acciones secundarias en estado vacío (*empty state*). | Puede resultar en mensajes crípticos del sistema ("0 registros encontrados"), pantallas en blanco o mensajes de error desconcertantes. | ¿Cuál es el texto exacto a desplegar y qué opciones de recuperación se facilitan (limpiar búsqueda, crear cliente, sugerencias)? |
| **12** | `secure` | Declaración abstracta sin vectores de amenaza, mecanismos de cifrado ni controles de acceso. | No especifica salvaguardas contra inyección SQL/NoSQL, control de acceso basado en roles (RBAC) o ataques de fuerza bruta. | ¿Qué controles de seguridad normativos y técnicos (parametrización, RBAC, HTTPS, rate limiting) deben implementarse y auditarse? |
| **13** | `not expose sensitive customer information` | No delimita qué campos del esquema de datos son considerados confidenciales o PII (*Personally Identifiable Information*). | Existe el riesgo de que el backend exponga tarjetas de crédito, identificadores fiscales (RFC/CURP/SSN) o domicilios en el JSON de respuesta. | ¿Cuál es la lista blanca (*allowlist*) explícita de campos autorizados para retorno en el payload de la API de búsqueda? |
| **14** | `fast enough for normal use` | Doble ambigüedad: ni "fast enough" tiene un valor medible, ni "normal use" dimensiona la concurrencia. | Imposibilita la formulación de pruebas de rendimiento y estrés; no define la capacidad de carga del sistema. | ¿Cuántas consultas simultáneas por segundo (QPS) se esperan en operación habitual y pico, y cuál es el tiempo de respuesta tolerado? |
| **15** | `work on mobile and desktop` | No aclara si es una aplicación web responsiva (RWD) o aplicaciones móviles nativas; no define adaptabilidad de layout. | Una tabla con múltiples columnas en desktop resulta inusable en una pantalla móvil sin diseño responsivo específico. | ¿Es interfaz web responsive o app nativa? ¿Cómo se transforma la presentación de datos en pantallas pequeñas (cards vs tabla)? |

---

## 4. Paso 2 — Clasificación de los Problemas

A continuación, se clasifican los problemas detectados utilizando la taxonomía oficial de ingeniería de requerimientos:

| Elemento | Problema Concreto | Clasificación Asignada |
|:---|:---|:---|
| `quickly` | Ausencia de límite máximo de tiempo de respuesta cuantificable. | **Rendimiento** / **Requisito no funcional incompleto** |
| `by name` | Indefinición de campos evaluados (nombre/apellido) y soporte de tildes. | **Regla de negocio ausente** / **Caso límite no definido** |
| `or email` | Falta de delimitación entre búsqueda de prefijo, dominio o coincidencia exacta. | **Regla de negocio ausente** / **Ambigüedad semántica** |
| `name or email` | Indefinición de arquitectura de entrada (unificada vs múltiple). | **UX/interfaz** / **Alcance** |
| `easy to use` | Expresión subjetiva no comprobable mediante criterios objetivos. | **UX/interfaz** / **Criterio de aceptación ausente** |
| `relevant results` | Ausencia de fórmula matemática o ponderación para calcular la relevancia. | **Regla de negocio ausente** / **Ambigüedad semántica** |
| `partial matches` | Indefinición de técnica de coincidencia (prefijo, subcadena, fuzzy) y longitud mínima. | **Alcance** / **Rendimiento** / **Regla de negocio ausente** |
| `large numbers of customers` | No se especifica el volumen volumétrico de datos ni la cardinalidad esperada. | **Rendimiento** / **Requisito no funcional incompleto** |
| `useful order` | Criterio de ordenación subjetivo y sin controles para el usuario. | **UX/interfaz** / **Regla de negocio ausente** |
| `most relevant customers first` | Falta de mecanismo de desempate determinista entre resultados con mismo score. | **Regla de negocio ausente** / **Caso límite no definido** |
| `appropriate message` | Falta de texto aprobado y acciones de recuperación en estado vacío. | **UX/interfaz** / **Criterio de aceptación ausente** |
| `secure` | Término genérico sin detalle de amenazas, controles de acceso ni estándares. | **Seguridad/privacidad** / **Requisito no funcional incompleto** |
| `not expose sensitive customer info`| Falta de catálogo de datos sensibles (PII) y política de enmascaramiento. | **Seguridad/privacidad** / **Regla de negocio ausente** |
| `fast enough for normal use` | No se cuantifica el rendimiento bajo cargas operativas reales (QPS, concurrencia). | **Rendimiento** / **Requisito no funcional incompleto** |
| `work on mobile and desktop` | No define estándares de adaptabilidad responsiva ni comportamiento táctil. | **UX/interfaz** / **Alcance** |

---

## 5. Paso 3 — Requisitos Verificables

Se formulan **8 Requisitos Funcionales (FR)** y **4 Requisitos No Funcionales (NFR)**, redactados en términos concretos y con su respectivo método objetivo de verificación:

### 5.1. Requisitos Funcionales

| ID | Tipo | Requisito Verificable | Cómo se Verifica |
|:---:|:---:|:---|:---|
| **FR-01** | Funcional | El sistema debe permitir la búsqueda de clientes mediante coincidencia parcial de texto sobre los campos de primer nombre, apellido paterno y apellido materno, siendo completamente insensible a mayúsculas, minúsculas y caracteres diacríticos (tildes, diéresis, eñes). | Pruebas de integración automatizadas que envían términos como "jose", "José", "JOSÉ", "perez", "Pérez" y validan que el conjunto de identificadores devuelto coincida exactamente con el dataset esperado. |
| **FR-02** | Funcional | El sistema debe permitir la búsqueda de clientes por correo electrónico mediante coincidencia de prefijo (antes del carácter `@`) o coincidencia exacta de la dirección completa, siendo insensible a mayúsculas y minúsculas. | Pruebas automatizadas de API enviando payloads de consulta con prefijos válidos ("carlos.mendoza@") y correos completos ("carlos.mendoza@empresa.com"), comprobando el retorno exclusivo de la cuenta correspondiente. |
| **FR-03** | Funcional | El sistema debe rechazar la ejecución de búsquedas y no disparar consultas al backend si el término ingresado por el usuario posee menos de 3 caracteres alfanuméricos netos (tras aplicar eliminación de espacios en blanco en extremos con `trim`). | Prueba E2E en interfaz de usuario introduciendo 1 y 2 caracteres, validando en la consola de red (*Network Tab*) que no se emita ninguna petición HTTP y se renderice un mensaje orientativo al usuario. |
| **FR-04** | Funcional | El sistema debe devolver los resultados de búsqueda paginados en bloques predeterminados de exactamente 20 registros por página, incluyendo en la cabecera de la respuesta los metadatos: `total_records`, `page_size`, `current_page` y `total_pages`. | Prueba de contrato de API validando que una consulta que genera 55 coincidencias retorne 20 elementos en página 1, 20 en página 2, 15 en página 3, con `total_pages: 3` y `total_records: 55`. |
| **FR-05** | Funcional | Los resultados de búsqueda deben ordenarse de forma determinista mediante el siguiente algoritmo de relevancia jerárquico: 1° Coincidencia exacta completa en email o nombre; 2° Coincidencia de prefijo en nombre o apellido; 3° Coincidencia de subcadena interna. Ante empate en puntuación de relevancia, el desempate se realizará alfabéticamente por `last_name` ascendente y luego por `customer_id` ascendente. | Prueba unitaria de la lógica de ordenamiento con un fixture de 10 clientes con patrones de nombres similares, comprobando que el orden de IDs devuelto coincida en un 100% con la secuencia calculada por el modelo de pruebas. |
| **FR-06** | Funcional | Cuando una búsqueda válida (>= 3 caracteres) no arroje ninguna coincidencia en la base de datos, el sistema debe presentar en pantalla un estado vacío (*empty state*) con el mensaje: *"No se encontraron clientes que coincidan con '[término]'. Verifique la ortografía o intente con otro criterio de búsqueda."*, acompañado de un botón interactivo con el texto *"Limpiar búsqueda"*. | Prueba automatizada de UI (Playwright/Cypress) buscando un término inexistente ("ZZZ_VALOR_NULO_99"), comprobando la presencia del elemento DOM con el mensaje exacto y la interactividad del botón de limpieza. |
| **FR-07** | Funcional | El payload de respuesta de la búsqueda y la interfaz visual únicamente deben incluir los campos: `customer_id`, `first_name`, `last_name`, `primary_email`, `phone_masked` (formato: `***-***-1234`) y `account_status`. Queda estrictamente prohibida la inclusión de campos sensibles como `tax_id`, `ssn`, `credit_card_data`, `billing_address` o `password_hash`. | Prueba de seguridad y validación de esquema JSON (*JSON Schema Validation*) sobre la respuesta HTTP, garantizando que ninguna llave no autorizada en la lista blanca forme parte del objeto JSON. |
| **FR-08** | Funcional | En pantallas con ancho de visualización >= 1024px (desktop), el sistema debe desplegar los resultados en una tabla tabular con cabeceras ordenables; en pantallas con ancho < 1024px (mobile/tablet), el sistema debe transformar la vista automáticamente en tarjetas verticales (*cards*) con botones de acción táctiles de tamaño mínimo 44x44px. | Pruebas visuales de regresión en múltiples viewports (Mobile: 375x667px, Desktop: 1440x900px), verificando mediante aserciones CSS la visibilidad del componente `table` en desktop y del componente `card-list` en mobile. |

### 5.2. Requisitos No Funcionales

| ID | Tipo | Requisito Verificable | Cómo se Verifica |
|:---:|:---:|:---|:---|
| **NFR-01** | No Funcional (Rendimiento) | El tiempo de respuesta de extremo a extremo de la API de búsqueda (latencia de red excluida) debe ser menor o igual a 200 milisegundos en el percentil 95 (P95) y menor a 400 milisegundos en el percentil 99 (P99), operando bajo una carga concurrente sostenida de 150 peticiones por segundo (RPS) contra una base de datos con al menos 2,000,000 de registros de clientes. | Prueba de carga y rendimiento ejecutada con k6 / Locust durante 15 minutos en ambiente de pruebas homologado, analizando la distribución estadística de los tiempos de respuesta del endpoint. |
| **NFR-02** | No Funcional (Seguridad) | El endpoint de búsqueda debe neutralizar cualquier intento de inyección de código (SQL Injection, NoSQL Injection y Cross-Site Scripting) mediante consultas estrictamente parametrizadas en capa de persistencia y sanitización contextual de entrada en capa de transporte. | Escaneo automatizado de vulnerabilidades dinámicas (DAST con OWASP ZAP) inyectando vectores de ataque (`' OR '1'='1`, `UNION SELECT`, `<script>alert(1)</script>`), certificando que el servidor responda con HTTP 200/400 seguro sin alterar la consulta ni ejecutar scripts. |
| **NFR-03** | No Funcional (Seguridad / Disponibilidad) | El servicio debe limitar la tasa de peticiones (*rate limiting*) a un máximo de 30 consultas de búsqueda por minuto por cada usuario autenticado. Al excederse este límite, el sistema debe bloquear peticiones subsecuentes retornando el código de estado `HTTP 429 Too Many Requests` junto con la cabecera `Retry-After`. | Script de pruebas automatizado que envía ráfagas de 35 peticiones en un lapso de 10 segundos utilizando el mismo token de autenticación, validando que las peticiones 1 a 30 retornen HTTP 200 y las peticiones 31 a 35 reciban código HTTP 429. |
| **NFR-04** | No Funcional (UX / Red) | El componente de entrada de búsqueda en la interfaz gráfica debe implementar un retardo de amortiguación (*debounce*) de exactamente 300 milisegundos antes de disparar la llamada HTTP al backend, y debe cancelar automáticamente mediante `AbortController` cualquier petición HTTP que se encuentre pendiente de respuesta si el usuario continúa introduciendo texto. | Prueba de frontend automatizada interceptando el tráfico de red, simulando un usuario escribiendo la palabra "González" letra por letra con intervalos de 100 ms, verificando que se envíe una sola petición HTTP al término del debounce y ninguna llamada redundante previa quede abierta. |

---

## 6. Paso 4 — Criterios de Aceptación (Formato Given / When / Then)

Se redactan **6 criterios de aceptación** formales y ejecutables derivados directamente de los requerimientos:

```gherkin
AC-01: Búsqueda exitosa insensible a mayúsculas y acentos diacríticos
Given un usuario autenticado con rol de "Representante de Soporte"
  And existen clientes registrados con nombres "Álvaro José Pérez" y "Maria Josefa Perez"
When el usuario escribe "jose perez" en el campo de búsqueda
Then el sistema muestra ambos clientes en la lista de resultados
  And el cliente "Álvaro José Pérez" se resalta indicando coincidencia exacta en ambos términos
  And no se produce ningún error por diferencias de tildes o mayúsculas.
```

```gherkin
AC-02: Búsqueda por prefijo de correo electrónico
Given un cliente registrado con correo "patricia.hernandez@empresa.com" y estado "Activo"
When el usuario introduce "patricia.hernandez@" en el buscador
Then el sistema retorna como primer resultado a "patricia.hernandez@empresa.com"
  And muestra su identificador, nombre completo y estado en el listado
  And el tiempo de renderizado es inferior a 250 ms.
```

```gherkin
AC-03: Restricción de longitud mínima de búsqueda (Control de carga)
Given el usuario se encuentra en la pantalla de búsqueda con el input en blanco
When el usuario escribe únicamente 2 caracteres alfanuméricos (ejemplo: "Ma")
Then el sistema no realiza ninguna petición de red al servidor backend
  And la vista no muestra indicadores de carga ni resultados vacíos
  And se despliega una leyenda en color grisáceo debajo del input indicando: "Escriba al menos 3 caracteres para buscar".
```

```gherkin
AC-04: Manejo de estado vacío cuando no existen coincidencias
Given una base de datos de clientes donde no existe ningún registro que contenga "ZzZ-Inexistente"
When el usuario busca "ZzZ-Inexistente" y presiona la tecla Enter
Then el sistema despliega un panel de estado vacío con el mensaje:
     "No se encontraron clientes que coincidan con 'ZzZ-Inexistente'. Verifique la ortografía o intente con otro criterio de búsqueda."
  And se visualiza un botón primario con la leyenda "Limpiar búsqueda"
  And al presionar dicho botón, el input de texto se vacía y se restaura el estado inicial.
```

```gherkin
AC-05: Paginación y control volumétrico ante gran número de resultados
Given una búsqueda con el término "González" que arroja 68 clientes coincidentes en la base de datos
When el servidor responde a la consulta de la primera página
Then la interfaz renderiza exactamente los primeros 20 clientes ordenados por relevancia jerárquica
  And el paginador indica claramente "Página 1 de 4 (68 resultados encontrados)"
  And los controles "Página Siguiente" y botones numéricos de página están habilitados y permiten la navegación fluida.
```

```gherkin
AC-06: Protección estricta de información sensible del cliente (PII)
Given un cliente registrado en la base de datos que cuenta con número de tarjeta bancaria, RFC, y teléfono particular
When dicho cliente aparece en los resultados de búsqueda de cualquier usuario del sistema
Then el cuerpo de la respuesta HTTP y la interfaz del usuario únicamente exhiben: ID, Nombre, Apellido, Email, Teléfono con máscara (***-***-5678) y Estado
  And las propiedades de tarjeta de crédito, RFC y dirección física no se encuentran presentes en ninguna parte del DOM ni en el payload JSON.
```

---

## 7. Paso 5 — Casos Límite y de Borde

Se analizan y definen los comportamientos del sistema ante condiciones de borde:

| Caso Límite | Comportamiento Esperado | ¿Requiere Decisión de Negocio? | Justificación / Impacto Técnico |
|:---|:---|:---:|:---|
| **Query vacío** | Si el input de búsqueda está vacío, no se envía ninguna solicitud al backend. La pantalla debe mostrar el estado inicial neutro o una lista de "Clientes consultados recientemente" (si negocio lo aprueba). | **Sí** | Requiere que el Product Owner decida si la pantalla inicial debe permanecer en blanco con instrucciones o si debe desplegar el historial de búsquedas recientes del usuario. |
| **Espacios en blanco exclusivamente o en extremos** | El sistema aplica automáticamente la función `trim()` eliminando espacios iniciales, finales y colapsando espacios múltiples interiores en un único espacio antes de evaluar la longitud del término. Si el término resultante queda vacío, se trata como *Query vacío*. | **No** | Es un estándar técnico universal de sanitización de entradas para evitar escaneos de base de datos accidentales e ineficientes. |
| **Mayúsculas, minúsculas y acentos diacríticos** | El motor de búsqueda normaliza tanto la consulta como los campos indexados a minúsculas y caracteres base sin acentos (mediante extensiones como `unaccent` en PostgreSQL o analizadores ASCII folding en motores NoSQL). "Gómez", "gomez", "GÓMEZ" deben producir exactamente el mismo resultado. | **No** | Corresponde a una buena práctica indiscutible de usabilidad y robustez técnica en sistemas en idioma español e internacional. |
| **Caracteres especiales y wildcards (`%`, `_`, `'`, `"`, `<`, `>`, `&`)** | Los caracteres comodín propios de SQL (`%`, `_`) se escapan como literales para que no actúen como operadores comodín en la consulta. Los caracteres HTML se sanitizan para impedir inyecciones XSS. Los caracteres de comillas se parametrizan en la consulta SQL. | **No** | Obligación técnica de seguridad estricta para evitar inyección SQL, bypass de filtros o ejecución de secuencias de comandos en el cliente. |
| **Sin resultados (0 coincidencias)** | Se presenta el estado vacío estandarizado (*empty state*) con mensaje empático y botón de "Limpiar búsqueda", sin registrar un código de error HTTP (responde HTTP 200 con arreglo vacío `[]`). | **Sí** | El Product Owner y diseño de UX deben validar el texto exacto del mensaje y si se ofrece o no un botón directo de "Crear nuevo cliente" en caso de que el cliente no exista. |
| **Gran volumen de resultados (> 10,000 coincidencias)** | El servidor nunca realiza un vuelco masivo de datos; restringe la consulta con `LIMIT 20 OFFSET X` (o paginación basada en cursor `WHERE id > last_seen_id LIMIT 20`) y reporta el conteo total máximo sin degradar la memoria del servidor ni saturar el DOM del navegador. | **Sí** | Negocio debe definir si se permite navegar hasta el final del catálogo o si se impone un tope máximo de resultados navegables (ej. máximo 500 resultados o 25 páginas) para prevenir *scraping*. |
| **Búsqueda rápida en tiempo real (Race Conditions en Typeahead)** | Cuando el usuario teclea rápidamente ("R", "Ro", "Rob", "Robe", "Robert"), el cliente cancela la petición HTTP previa que esté pendiente de resolución mediante la API nativa `AbortController` antes de lanzar la nueva, evitando que una respuesta lenta previa sobreescriba los datos más recientes. | **No** | Es un estándar técnico de arquitectura frontend para garantizar la consistencia visual y evitar condiciones de carrera en peticiones asíncronas. |
| **Clientes homónimos (mismo nombre y apellido)** | El sistema no agrupa ni colapsa clientes con el mismo nombre; los muestra como filas independientes destacando el correo electrónico y el identificador de cliente para su fácil diferenciación. | **No** | Regla de integridad de datos elemental para evitar confusiones de identidad en operaciones críticas de soporte o facturación. |

---

## 8. Preguntas Abiertas para el Product Owner y Stakeholders

Antes de proceder a la fase de diseño arquitectónico e implementación, el equipo de ingeniería requiere la resolución formal de las siguientes preguntas clave de negocio:

### 8.1. Reglas de Negocio y Operación
1. **Atributos visibles obligatorios:** Además de nombre y email, ¿qué datos secundarios son esenciales para que los empleados identifiquen inequívocamente al cliente en la lista rápida (ej. ciudad de residencia, empresa, estado de cuenta activo/inactivo)?
2. **Acción al seleccionar un resultado:** ¿Qué acción exacta debe dispararse cuando el usuario hace clic sobre un cliente de la lista (abrir ficha completa en nueva pestaña, abrir modal de resumen o cargar al cliente en el contexto de un pedido en curso)?
3. **Flujo de cliente no encontrado:** Si la búsqueda no arroja coincidencias, ¿el usuario debe tener acceso a un botón de "Registrar nuevo cliente" directamente desde esa pantalla, o el flujo de alta es independiente?

### 8.2. Control de Acceso y Privacidad
4. **Roles y Alcance de Datos (RBAC):** ¿Todos los empleados ven la totalidad de la base de clientes nacional, o la búsqueda debe segmentarse automáticamente según la sucursal, región o cartera asignada al empleado que consulta?
5. **Registro de Auditoría:** ¿Es requerido registrar en bitácora de auditoría (*audit trail*) qué empleado consultó qué clientes y en qué momento para fines de cumplimiento normativo y privacidad?

### 8.3. Dimensionamiento y Capacidad
6. **Volumetría y Proyecciones:** ¿Cuál es la cantidad exacta de clientes activos e inactivos registrada actualmente en la base de datos y cuál es el crecimiento proyectado para los próximos 24 meses?
7. **Picos de Demanda:** ¿En qué momentos del día o del mes se concentran las mayores consultas de clientes (ej. cierre de quincena, campañas de promociones) para planificar la autoescala de infraestructura?

---

## 9. AI Usage Log — Registro Obligatorio de Uso de IA

El siguiente registro documenta las interacciones con el modelo de IA a lo largo del proceso de análisis, demostrando cómo se dirigió, criticó, ajustó y validó cada hallazgo de ingeniería.

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
  3. Ejecutó el comando de entorno para abrir el proyecto en Visual Studio Code e implementó la bitácora independiente `AI_USAGE_LOG.md`.
- **Decisión del estudiante:**
  Realicé una inspección visual y técnica de los artefactos directamente en VS Code. Verifiqué la coherencia entre las tablas de requerimientos, la ausencia de supuestos no justificados, la integridad visual del PDF compilado y la fidelidad del AI Usage Log respecto al proceso de ingeniería ejecutado.
- **Impacto:**
  Generación, verificación y disponibilidad del paquete completo de entrega del laboratorio: `ADA_04_Specification_Review_RubenPerez.pdf`, `ADA_04_Specification_Review_RubenPerez.md`, `AI_USAGE_LOG.md` y `generate_pdf.py`.

---

## 10. Conclusiones y Reflexión de Ingeniería

1. **El valor de la formalización:** Una especificación que a primera vista parece "clara" y "concisa" para un usuario de negocio oculta decenas de trampas técnicas cuando se analiza con mentalidad de ingeniería de pruebas. Convertir adjetivos como "rápido" o "fácil" en SLAs (P95 < 200 ms) y heurísticas verificables es la diferencia entre un software predecible y una fuente constante de deuda técnica y bugs.
2. **Rol activo ante la IA:** El uso de herramientas de IA no sustituye la responsabilidad ni el criterio del ingeniero. La IA acelera la identificación sistemática de patrones y posibles vectores de falla, pero requiere una dirección precisa, cuestionamiento continuo de sus sesgos o suposiciones, y un proceso de filtrado que garantice que las decisiones de negocio no sean inventadas arbitrariamente por el modelo, sino identificadas como preguntas abiertas para el cliente o Product Owner.
