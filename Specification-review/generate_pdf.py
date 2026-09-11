import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 756, "ADA-04: Revisión de Especificaciones — Ingeniería de Software asistida por IA · UADY")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 750, 558, 750)

        # Footer (all pages)
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "Rubén Pérez — ADA-04 Revisión de Especificaciones")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_pdf(filename="ADA_04_Specification_Review_RubenPerez.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1A365D")   # Deep navy
    secondary_color = colors.HexColor("#2B6CB0") # Slate blue
    dark_text = colors.HexColor("#2D3748")
    light_bg = colors.HexColor("#EDF2F7")
    accent_bar = colors.HexColor("#3182CE")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_text,
        spaceAfter=6
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1A202C")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=dark_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=primary_color
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#2D3748")
    )

    story = []

    # Title & Header
    story.append(Paragraph("ADA-04: Revisión de Especificaciones", title_style))
    story.append(Paragraph("<b>Ingeniería de Software Asistida por IA · Universidad Autónoma de Yucatán (UADY)</b><br/>"
                           "<b>Estudiante:</b> Rubén Pérez &nbsp;|&nbsp; <b>Fecha:</b> 11 de septiembre de 2026 &nbsp;|&nbsp; "
                           "<b>Secuencia:</b> Detectar ambigüedad &rarr; Convertir requisitos en comportamiento verificable", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=10))

    # 1. Objetivo y Metodología
    story.append(Paragraph("1. Objetivo y Enfoque del Análisis", h1_style))
    story.append(Paragraph(
        "El presente informe documenta el análisis riguroso de una especificación deliberadamente ambigua correspondiente a la funcionalidad <i>Customer Search</i>. "
        "Siguiendo el flujo obligatorio de la práctica, se utilizó inteligencia artificial como asistente para detectar ambigüedades, omisiones, casos límite y vacíos de requerimientos no funcionales. "
        "Como estudiante e ingeniero, se evaluaron, cuestionaron y filtraron críticamente las sugerencias del modelo para estructurar una especificación formal, no ambigua y 100% convertible en pruebas de software.",
        body_style
    ))

    # 2. Especificación Original
    story.append(Paragraph("2. Especificación Original Deliberadamente Ambigua", h1_style))
    spec_text = (
        "<b>FEATURE: Customer Search</b><br/>"
        "We need a customer search feature for the application.<br/>"
        "The user should be able to search customers quickly by name or email.<br/>"
        "The search should be easy to use and return relevant results.<br/>"
        "It should support partial matches and work well with large numbers of customers.<br/>"
        "Results should be displayed in a useful order, with the most relevant customers first.<br/>"
        "If no customers are found, show an appropriate message.<br/>"
        "The search should be secure and should not expose sensitive customer information.<br/>"
        "It should be fast enough for normal use.<br/>"
        "The feature should work on mobile and desktop."
    )
    spec_table = Table([[Paragraph(spec_text, callout_style)]], colWidths=[504])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(spec_table)
    story.append(Spacer(1, 8))

    # 3. Paso 1 — Identificar ambigüedades
    story.append(Paragraph("3. Paso 1 — Identificación de Ambigüedades (14 Hallazgos)", h1_style))
    story.append(Paragraph("Se analizaron exhaustivamente los enunciados de la especificación para identificar elementos subjetivos, vagos o no medibles:", body_style))

    ambiguities = [
        ("quickly", "No existe métrica de tiempo objetiva ni percentil.", "Impide determinar objetivamente si el sistema cumple el requisito.", "¿Cuál es el tiempo máximo de respuesta aceptable (SLA) y bajo qué percentil (ej. P95 < 200 ms)?"),
        ("by name", "No especifica qué campos del nombre se evalúan ni tratamiento de diacríticos.", "Provoca falsos negativos si solo busca primer nombre o si omite acentos en español ('Pérez' vs 'Perez').", "¿La búsqueda aplica a first_name, last_name o concatenado? ¿Es insensible a diacríticos y mayúsculas?"),
        ("or email", "No define si busca coincidencia exacta, prefijo de usuario o subcadena en dominio.", "Permitir subcadenas en dominios comunes (ej. 'gmail') satura la respuesta con resultados irrelevantes.", "¿La búsqueda exige coincidencia exacta, prefijo antes del '@' o subcadena en cualquier posición?"),
        ("name or email", "No define si es un campo de búsqueda unificado o inputs separados.", "Impacta de forma crítica la heurística de parsing en backend y el diseño de la interfaz de usuario.", "¿Se utilizará una barra de búsqueda única inteligente o inputs diferenciados para nombre y correo?"),
        ("easy to use", "Expresión puramente subjetiva sin definición operacional.", "No es verificable mediante pruebas automatizadas ni estándares medibles de calidad de software.", "¿Qué estándares de usabilidad (ej. máximo 2 clics para consultar, SUS > 80, WCAG 2.1 AA) se aplicarán?"),
        ("relevant results", "No define fórmula ni algoritmo de puntuación (scoring) de relevancia.", "Distintos ingenieros programarán lógicas distintas (match exacto vs prefijo vs trigramas), alterando los resultados.", "¿Cuál es la ponderación algorítmica de relevancia y qué variables de negocio la modifican?"),
        ("partial matches", "Indefinición de técnica (prefijo, subcadena o fuzzy) y longitud mínima.", "Búsquedas arbitrarias de 1 carácter ('%a%') anulan índices B-Tree y degradan la base de datos.", "¿Qué algoritmo de coincidencia parcial se usará y cuál es la longitud mínima de caracteres (ej. >=3)?"),
        ("large numbers", "No cuantifica la cardinalidad de la base de datos ni tasa de crecimiento.", "La arquitectura para 10,000 registros es trivial; para 20 millones requiere motores dedicados (Elasticsearch).", "¿Cuál es el volumen actual de clientes y la proyección volumétrica a 3-5 años?"),
        ("useful order", "Criterio dependiente del rol y perfil del usuario.", "Lo que es útil para un agente de cobranza difiere de lo que requiere un auditor o un ejecutivo de ventas.", "¿Cuál es el ordenamiento predeterminado y qué columnas permitirán reordenamiento dinámico?"),
        ("most relevant first", "No define regla de desempate (tie-breaking) ante igual puntuación.", "Puede provocar que el orden de los resultados devueltos por la BD sea no determinista.", "¿Cuál es el criterio determinista secundario de desempate (ej. last_name A-Z, customer_id asc)?"),
        ("appropriate message", "Falta redacción aprobada y acciones de recuperación en estado vacío.", "El desarrollador podría colocar mensajes crípticos o pantallas sin alternativas para el usuario.", "¿Qué texto exacto se mostrará y qué acciones se ofrecerán (limpiar búsqueda, registrar cliente)?"),
        ("secure", "Término genérico sin detalle de amenazas, controles ni estándares.", "No establece salvaguardas contra SQLi, XSS, control de acceso basado en roles (RBAC) ni cifrado.", "¿Qué controles específicos (parametrización, RBAC, HTTPS, rate limiting) deben auditarse?"),
        ("not expose sensitive info", "No define qué atributos del modelo constituyen datos sensibles (PII).", "Riesgo de exponer tarjetas de crédito, identificadores fiscales o domicilios en el payload JSON.", "¿Cuál es la lista blanca (allowlist) explícita de campos que el endpoint tiene autorizado devolver?"),
        ("fast enough / normal use", "Doble ambigüedad: ni latencia ni volumen concurrente están dimensionados.", "Imposibilita diseñar pruebas de carga y estrés; no define la capacidad de servicio esperada.", "¿Cuántas consultas por segundo (QPS) se esperan en operación habitual y pico?"),
    ]

    p1_data = [[
        Paragraph("<b>Elemento</b>", table_header_style),
        Paragraph("<b>Problema Detectado</b>", table_header_style),
        Paragraph("<b>¿Por qué representa un problema?</b>", table_header_style),
        Paragraph("<b>Pregunta a resolver</b>", table_header_style)
    ]]
    for el, prob, why, q in ambiguities:
        p1_data.append([
            Paragraph(f"<code>{el}</code>", table_cell_bold),
            Paragraph(prob, table_cell_style),
            Paragraph(why, table_cell_style),
            Paragraph(q, table_cell_style)
        ])

    p1_table = Table(p1_data, colWidths=[70, 140, 140, 154], repeatRows=1)
    p1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(p1_table)
    story.append(Spacer(1, 10))

    # 4. Paso 2 — Clasificar problemas
    story.append(Paragraph("4. Paso 2 — Clasificación de Problemas", h1_style))
    story.append(Paragraph("Los problemas detectados fueron categorizados formalmente según la taxonomía de la materia:", body_style))

    p2_items = [
        ("quickly", "No define tiempo máximo de respuesta ni percentil medible.", "Rendimiento / Requisito no funcional incompleto"),
        ("by name", "Indefinición de campos evaluados (nombre/apellido) y soporte de diacríticos.", "Regla de negocio ausente / Caso límite no definido"),
        ("or email", "Falta delimitación entre búsqueda de prefijo, dominio o coincidencia exacta.", "Regla de negocio ausente / Ambigüedad semántica"),
        ("name or email", "Indefinición de arquitectura de entrada (unificada vs inputs independientes).", "UX/interfaz / Alcance"),
        ("easy to use", "Expresión subjetiva no comprobable mediante criterios objetivos.", "UX/interfaz / Criterio de aceptación ausente"),
        ("relevant results", "Ausencia de fórmula matemática o ponderación para calcular relevancia.", "Regla de negocio ausente / Ambigüedad semántica"),
        ("partial matches", "Indefinición de técnica (prefijo, subcadena, fuzzy) y longitud mínima requerida.", "Alcance / Rendimiento / Regla de negocio ausente"),
        ("large numbers", "No se especifica cardinalidad de datos de clientes ni ritmo de crecimiento.", "Rendimiento / Requisito no funcional incompleto"),
        ("useful order", "Criterio de ordenación subjetivo y sin controles de usuario.", "UX/interfaz / Regla de negocio ausente"),
        ("most relevant first", "Falta mecanismo de desempate determinista ante puntuaciones idénticas.", "Regla de negocio ausente / Caso límite no definido"),
        ("appropriate message", "Falta de texto aprobado y opciones interactivas en estado vacío.", "UX/interfaz / Criterio de aceptación ausente"),
        ("secure", "Término genérico sin detalle de vectores de amenaza ni estándares exigidos.", "Seguridad/privacidad / Requisito no funcional incompleto"),
        ("sensitive customer info", "Falta de catálogo de datos sensibles (PII) y política de enmascaramiento.", "Seguridad/privacidad / Regla de negocio ausente"),
        ("fast enough / normal use", "No cuantifica latencia bajo cargas operativas reales (QPS, concurrencia).", "Rendimiento / Requisito no funcional incompleto"),
        ("work on mobile and desktop", "No define especificaciones de diseño responsivo ni comportamiento táctil.", "UX/interfaz / Alcance")
    ]

    p2_data = [[
        Paragraph("<b>Elemento</b>", table_header_style),
        Paragraph("<b>Problema Concreto</b>", table_header_style),
        Paragraph("<b>Clasificación Asignada</b>", table_header_style)
    ]]
    for el, prob, cat in p2_items:
        p2_data.append([
            Paragraph(f"<code>{el}</code>", table_cell_bold),
            Paragraph(prob, table_cell_style),
            Paragraph(f"<b>{cat}</b>", table_cell_style)
        ])

    p2_table = Table(p2_data, colWidths=[85, 215, 204], repeatRows=1)
    p2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(p2_table)
    story.append(Spacer(1, 10))

    # 5. Paso 3 — Requisitos verificables
    story.append(Paragraph("5. Paso 3 — Requisitos Verificables", h1_style))
    story.append(Paragraph("Se establecen 8 requisitos funcionales y 4 no funcionales con método de verificación comprobable:", body_style))

    fr_nfr_data = [
        ("FR-01", "Funcional", "Búsqueda por coincidencia parcial de nombre en first_name y last_name a partir de 3 caracteres, insensible a mayúsculas y acentos diacríticos.", "Pruebas de integración automatizadas con queries con y sin acentos ('José' vs 'jose', 'Pérez' vs 'perez') comprobando el retorno exacto de IDs esperados."),
        ("FR-02", "Funcional", "Búsqueda por correo electrónico por prefijo (antes de '@') o dirección exacta completa, insensible a mayúsculas.", "Pruebas de API enviando prefijos ('carlos.m@') y correos completos, comprobando el retorno de la cuenta correspondiente."),
        ("FR-03", "Funcional", "Rechazo de consultas con longitud menor a 3 caracteres alfanuméricos netos tras aplicar trim(); no debe emitir peticiones HTTP al backend.", "Prueba E2E en UI verificando en la pestaña Network que con 1 o 2 caracteres no se envíe ninguna petición y se muestre un aviso orientativo."),
        ("FR-04", "Funcional", "Paginación obligatoria en bloques de 20 registros por página, incluyendo metadatos: total_records, page_size, current_page y total_pages.", "Prueba de contrato de API validando que una búsqueda de 55 resultados retorne 3 páginas (20, 20, 15) con metadatos consistentes."),
        ("FR-05", "Funcional", "Ordenamiento jerárquico determinista: 1° Match exacto, 2° Match de prefijo, 3° Subcadena. Desempate secundario por last_name asc y customer_id asc.", "Prueba unitaria con un fixture de 10 clientes con patrones similares validando que el orden de IDs en la respuesta coincida con la secuencia calculada."),
        ("FR-06", "Funcional", "Despliegue de estado vacío cuando no existan coincidencias (>=3 chars), mostrando mensaje empático y botón interactivo 'Limpiar búsqueda'.", "Prueba de UI (Playwright/Cypress) con término inexistente validando en el DOM la visibilidad del texto y funcionalidad del botón."),
        ("FR-07", "Funcional", "Restricción de datos sensibles: el payload solo contendrá customer_id, first_name, last_name, email, phone_masked (***-***-1234) y status.", "Prueba de validación de JSON Schema certificando que campos sensibles (tax_id, credit_card, address) nunca figuren en el payload."),
        ("FR-08", "Funcional", "Interfaz responsiva: en pantallas >= 1024px muestra tabla con columnas ordenables; en < 1024px transforma a tarjetas verticales (cards).", "Prueba visual automatizada en viewports de 375x667 y 1440x900 validando aserciones CSS sobre los componentes renderizados."),
        ("NFR-01", "No funcional", "Latencia de API <= 200 ms en P95 y <= 400 ms en P99 bajo carga sostenida de 150 QPS con BD de 2,000,000 de registros.", "Prueba de carga y rendimiento con k6 / Locust durante 15 minutos en staging, analizando distribución de percentiles de latencia."),
        ("NFR-02", "No funcional", "Inmunidad contra inyecciones SQL/NoSQL y XSS mediante consultas estrictamente parametrizadas y sanitización contextual de inputs.", "Escaneo DAST automatizado con OWASP ZAP inyectando payloads de SQLi y XSS, asegurando respuesta HTTP 200/400 sin ejecución de scripts."),
        ("NFR-03", "No funcional", "Rate limiting de máximo 30 solicitudes de búsqueda por minuto por usuario/sesión; si se excede retorna HTTP 429 Too Many Requests.", "Script automatizado enviando 35 peticiones en 10 s con el mismo token, validando que de la 31 a la 35 retornen HTTP 429 con Retry-After."),
        ("NFR-04", "No funcional", "Debounce de 300 ms en cliente antes de emitir la llamada HTTP y cancelación automática de peticiones previas con AbortController.", "Prueba de frontend interceptando tráfico simulando tecleo de 'González' (100 ms/char), verificando que se envíe una sola llamada HTTP final."),
    ]

    p3_table_data = [[
        Paragraph("<b>ID</b>", table_header_style),
        Paragraph("<b>Tipo</b>", table_header_style),
        Paragraph("<b>Requisito Verificable</b>", table_header_style),
        Paragraph("<b>Cómo se Verifica</b>", table_header_style)
    ]]
    for rid, rtype, req, ver in fr_nfr_data:
        p3_table_data.append([
            Paragraph(f"<b>{rid}</b>", table_cell_bold),
            Paragraph(rtype, table_cell_style),
            Paragraph(req, table_cell_style),
            Paragraph(ver, table_cell_style)
        ])

    p3_table = Table(p3_table_data, colWidths=[45, 65, 205, 189], repeatRows=1)
    p3_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(p3_table)
    story.append(Spacer(1, 10))

    # 6. Paso 4 — Criterios de aceptación
    story.append(Paragraph("6. Paso 4 — Criterios de Aceptación (Given / When / Then)", h1_style))
    story.append(Paragraph("Se formularon 6 criterios de aceptación en formato formal de pruebas BDD:", body_style))

    criteria = [
        ("AC-01: Búsqueda insensible a mayúsculas y diacríticos",
         "Given un usuario autenticado con rol de consulta y clientes en BD como 'Álvaro José Pérez' y 'Maria Josefa Perez'\n"
         "When el usuario escribe 'jose perez' en el buscador\n"
         "Then el sistema muestra ambos clientes resaltando coincidencias exactas, sin errores por acentos o mayúsculas."),
        ("AC-02: Búsqueda por prefijo de correo electrónico",
         "Given un cliente registrado con correo 'patricia.hernandez@empresa.com' y estado 'Activo'\n"
         "When el usuario introduce 'patricia.hernandez@' en el campo de búsqueda\n"
         "Then el sistema retorna a 'patricia.hernandez@empresa.com' en primer lugar en menos de 250 ms."),
        ("AC-03: Restricción de longitud mínima de búsqueda (Control de carga)",
         "Given el usuario se encuentra en la pantalla de búsqueda con el input vacío\n"
         "When el usuario escribe únicamente 2 caracteres alfanuméricos (ej. 'Ma')\n"
         "Then no se envía ninguna petición HTTP al backend y se muestra el mensaje: 'Escriba al menos 3 caracteres para buscar'."),
        ("AC-04: Manejo de estado vacío sin coincidencias",
         "Given una base de datos de clientes donde no existe ningún registro coincidente con 'ZzZ-Inexistente'\n"
         "When el usuario busca 'ZzZ-Inexistente' y confirma la consulta\n"
         "Then se despliega el mensaje: 'No se encontraron clientes que coincidan con \"ZzZ-Inexistente\". Verifique la ortografía o intente con otro criterio de búsqueda' junto con el botón 'Limpiar búsqueda'."),
        ("AC-05: Paginación y control volumétrico ante gran número de resultados",
         "Given una búsqueda con el término 'González' que arroja 68 clientes coincidentes en base de datos\n"
         "When el servidor responde a la consulta de la primera página\n"
         "Then la interfaz renderiza los primeros 20 clientes ordenados por relevancia e indica 'Página 1 de 4 (68 resultados)' con controles de navegación activos."),
        ("AC-06: Protección de información sensible del cliente (PII)",
         "Given un cliente registrado en la base de datos que cuenta con tarjeta bancaria, RFC y teléfono particular\n"
         "When dicho cliente aparece en los resultados de búsqueda de cualquier usuario del sistema\n"
         "Then la interfaz y el payload JSON únicamente exhiben: ID, Nombre, Email, Teléfono con máscara (***-***-1234) y Estado, excluyendo tarjetas y RFC del DOM y de la respuesta de red.")
    ]

    for title, gwt in criteria:
        c_data = [
            [Paragraph(f"<b>{title}</b>", ParagraphStyle('CTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=primary_color))],
            [Paragraph(gwt.replace("\n", "<br/>"), code_style)]
        ]
        c_table = Table(c_data, colWidths=[504])
        c_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F7FAFC")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(c_table)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 5))

    # 7. Paso 5 — Casos límite
    story.append(Paragraph("7. Paso 5 — Casos Límite y Comportamiento Esperado", h1_style))
    story.append(Paragraph("Se especifican los 8 casos de borde esenciales y si demandan decisiones de negocio:", body_style))

    edge_cases = [
        ("Query vacío", "No enviar petición al backend; mantener pantalla neutra o mostrar búsquedas recientes.", "Sí (decidir si mostrar historial de consultas previas)"),
        ("Espacios en blanco", "Aplicar trim() en extremos y colapsar espacios internos; si queda vacío, no buscar.", "No (estándar técnico de sanitización de entradas)"),
        ("Mayúsculas / minúsculas y acentos", "Normalizar a minúsculas y sin acentos (unaccent); 'Gómez' igual a 'gomez'.", "No (estándar de usabilidad para idioma español)"),
        ("Caracteres especiales y SQLi", "Escapar wildcards (% _) como literales; sanitizar HTML contra XSS; parametrizar SQL.", "No (obligación de seguridad no negociable)"),
        ("Sin resultados (0 matches)", "Mostrar estado vacío con mensaje empático y botón para limpiar búsqueda (HTTP 200).", "Sí (validar texto y si se añade botón 'Crear nuevo cliente')"),
        ("Muchos resultados (>10,000)", "Paginación estricta LIMIT 20 OFFSET X o por cursor; limitar profundidad de páginas.", "Sí (definir tope máximo navegable para evitar scraping masivo)"),
        ("Race conditions en typeahead", "Cancelar peticiones HTTP pendientes mediante AbortController antes de emitir la nueva.", "No (estándar de consistencia visual en arquitecturas frontend)"),
        ("Clientes homónimos", "Mostrar filas separadas destacando email e ID para desambiguación inequívoca.", "No (regla de integridad de datos de clientes)"),
    ]

    edge_data = [[
        Paragraph("<b>Caso Límite</b>", table_header_style),
        Paragraph("<b>Comportamiento Esperado</b>", table_header_style),
        Paragraph("<b>¿Requiere decisión?</b>", table_header_style)
    ]]
    for case, beh, req_dec in edge_cases:
        edge_data.append([
            Paragraph(f"<b>{case}</b>", table_cell_bold),
            Paragraph(beh, table_cell_style),
            Paragraph(req_dec, table_cell_style)
        ])

    edge_table = Table(edge_data, colWidths=[110, 244, 150], repeatRows=1)
    edge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(edge_table)
    story.append(Spacer(1, 10))

    # 8. Preguntas abiertas para Product Owner
    story.append(Paragraph("8. Preguntas Abiertas para el Product Owner / Cliente", h1_style))
    po_questions = [
        "<b>1. Atributos visibles:</b> ¿Qué datos secundarios son obligatorios en la lista rápida (ej. sucursal, ciudad, estado de cuenta activo/inactivo)?",
        "<b>2. Acción sobre el resultado:</b> ¿Al hacer clic sobre un cliente se abre su perfil completo, se selecciona en un formulario o se abre un modal?",
        "<b>3. Registro de cliente no encontrado:</b> Si no existen resultados, ¿se debe permitir crear un nuevo cliente directamente desde la pantalla de búsqueda?",
        "<b>4. Segmentación RBAC:</b> ¿Todos los usuarios ven todos los clientes, o la búsqueda se filtra según la sucursal o cartera asignada al empleado?",
        "<b>5. Auditoría de accesos:</b> ¿Es obligatorio registrar en bitácora qué usuario buscó y visualizó datos de qué clientes para cumplimiento regulatorio?",
        "<b>6. Volumetría real:</b> ¿Cuántos clientes existen actualmente en BD y cuál es el crecimiento proyectado para los próximos 24 meses?",
        "<b>7. Límites de paginación:</b> ¿Se debe restringir la paginación a un máximo de páginas (ej. 25 páginas / 500 registros) para prevenir extracción masiva de datos?"
    ]
    for q in po_questions:
        story.append(Paragraph(f"• {q}", body_style))
    story.append(Spacer(1, 10))

    # 9. AI Usage Log
    story.append(Paragraph("9. AI Usage Log — Registro Obligatorio de Uso de IA", h1_style))
    story.append(Paragraph("Evidencia de dirección, evaluación crítica y trazabilidad entre interacciones con IA y decisiones de ingeniería:", body_style))

    log_entries = [
        ("Entry 01 — Análisis Crítico Inicial y Detección de Ambigüedades",
         "Requirements Analysis", "Antigravity CLI / Gemini 3.8 Flash (High)", "2026-09-11",
         "Actúa como Senior Requirements Engineer. Ejecuta un análisis crítico exhaustivo de la especificación de 'Customer Search'. Identifica ambigüedades semánticas, vacíos de especificación, métricas ausentes, riesgos de seguridad/PII y formula preguntas clave para el Product Owner. Separa observaciones de recomendaciones técnicas.",
         "Identificó 14 términos no verificables ('quickly', 'relevant results', 'large numbers', 'secure'), demostró la imposibilidad de automatizar pruebas con el texto actual y agrupó los hallazgos en categorías de riesgo operativo.",
         "Evalué y acepté las 14 observaciones. Exigí priorizar el tratamiento de acentos diacríticos (tildes y eñes) en español y requerí analizar el impacto arquitectónico de un input de búsqueda unificado frente a filtros independientes.",
         "Estructuración formal de la tabla del Paso 1 (14 ambigüedades con impacto y pregunta) y definición de preguntas estratégicas para el Product Owner."),
        
        ("Entry 02 — Clasificación Taxonómica, Casos Límite y Atributos de Calidad (NFRs)",
         "Specification & Quality Attributes (NFRs)", "Antigravity CLI / Gemini 3.8 Flash (High)", "2026-09-11",
         "Procede con la estructuración técnica del laboratorio ADA-04 conforme a las directrices de la UADY: clasifica los problemas detectados en la taxonomía de 9 categorías, delimita los casos de borde operativos (normalización diacrítica, mitigación SQLi/XSS, race conditions en frontend), e infiere los NFRs cuantitativos. Asumo el rol de Lead Engineer para auditar y validar cada salida.",
         "Clasificó los 15 problemas en las 9 categorías oficiales de la UADY, modeló 8 casos de borde fundamentales y formuló 4 requisitos no funcionales cuantitativos (latencia P95 < 200 ms bajo 150 QPS, rate limiting de 30 req/min, debounce con AbortController).",
         "Audité los casos límite y NFRs: ratifiqué el uso de AbortController en frontend, fijé la longitud mínima de búsqueda en 3 caracteres para evitar scans masivos de tabla, y mantuve las decisiones de negocio sobre estados vacíos como preguntas abiertas para el PO.",
         "Consolidación de las matrices del Paso 2 (Clasificación), Paso 5 (Casos límite) y definición cuantitativa de los 4 NFRs (NFR-01 a NFR-04)."),

        ("Entry 03 — Formalización de Requisitos Funcionales y Criterios Given / When / Then",
         "Requirements Verification & Acceptance Criteria", "Antigravity CLI / Gemini 3.8 Flash (High)", "2026-09-11",
         "Sintetiza los hallazgos en al menos 8 Requisitos Funcionales (FR-01 a FR-08) y 4 No Funcionales (NFR-01 a NFR-04) desacoplados de implementaciones prematuras con método objetivo de verificación. Formaliza al menos 6 Criterios de Aceptación BDD en sintaxis Given/When/Then cubriendo casos de éxito, estados vacíos interactivos, paginación y directivas de seguridad para mitigación de fuga de PII.",
         "Redactó FR-01 a FR-08 y los escenarios AC-01 a AC-06 en sintaxis Gherkin estándar, especificando precondiciones, disparadores y postcondiciones verificables para búsqueda insensible a diacríticos, prefijos, límites y protección de datos.",
         "Validé exhaustivamente los requisitos y criterios: verifiqué que cada uno fuera comprobable con suites de prueba (Playwright, Cypress, k6), exigí en AC-04 un botón interactivo 'Limpiar búsqueda' y en AC-06 el enmascaramiento estricto (***-***-1234) sin exponer PII.",
         "Aprobación técnica definitiva de las tablas de Requisitos Verificables (Paso 3) y Criterios de Aceptación BDD (Paso 4) para pruebas automatizadas."),

        ("Entry 04 — Consolidación de Artefactos, Inspección en IDE y Compilación de Entrega",
         "Documentation & Deliverable Review", "Antigravity CLI / Gemini 3.8 Flash (High)", "2026-09-11",
         "Consolida todos los artefactos de ingeniería generados en el espacio de trabajo: compila el informe técnico formal en Markdown, automatiza la generación del entregable oficial en PDF conforme al estándar de ADA-04 mediante un script ejecutable, y estructura la bitácora de trazabilidad de uso de IA (AI Usage Log) reflejando la dirección técnica, evaluación crítica de decisiones y gobierno del flujo de trabajo.",
         "Compiló el informe en Markdown, implementó y ejecutó el script generate_pdf.py con ReportLab para generar el PDF oficial de 6 páginas, abrió el proyecto en VS Code y redactó el archivo independiente AI_USAGE_LOG.md.",
         "Inspeccioné visualmente los artefactos en VS Code. Confirmé que las tablas, criterios BDD y casos de borde cumplieran con la rúbrica de ADA-04 y formalicé el registro de co-creación, auditoría y trazabilidad.",
         "Generación exitosa y verificación del paquete completo de entrega: ADA_04_Specification_Review_RubenPerez.pdf, AI_USAGE_LOG.md, ADA_04_Specification_Review_RubenPerez.md y generate_pdf.py.")
    ]

    for title, stage, tool, date, prompt, contrib, dec, impact in log_entries:
        log_content = [
            [Paragraph(f"<b>{title}</b>", table_header_style), Paragraph("", table_header_style)],
            [Paragraph("<b>Etapa:</b>", table_cell_bold), Paragraph(stage, table_cell_style)],
            [Paragraph("<b>Herramienta / Modelo:</b>", table_cell_bold), Paragraph(tool, table_cell_style)],
            [Paragraph("<b>Fecha:</b>", table_cell_bold), Paragraph(date, table_cell_style)],
            [Paragraph("<b>Prompt / Objetivo:</b>", table_cell_bold), Paragraph(f"<i>{prompt}</i>", table_cell_style)],
            [Paragraph("<b>Contribución de la IA:</b>", table_cell_bold), Paragraph(contrib, table_cell_style)],
            [Paragraph("<b>Decisión del estudiante:</b>", table_cell_bold), Paragraph(f"<b>{dec}</b>", table_cell_style)],
            [Paragraph("<b>Impacto:</b>", table_cell_bold), Paragraph(impact, table_cell_style)],
        ]
        log_table = Table(log_content, colWidths=[120, 384])
        log_table.setStyle(TableStyle([
            ('SPAN', (0,0), (1,0)),
            ('BACKGROUND', (0,0), (-1,0), secondary_color),
            ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#EDF2F7")),
            ('BACKGROUND', (1,1), (1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(log_table)
        story.append(Spacer(1, 6))

    # 10. Conclusiones
    story.append(Spacer(1, 4))
    story.append(Paragraph("10. Conclusiones y Cumplimiento Académico", h1_style))
    story.append(Paragraph(
        "El ejercicio demostró cómo una especificación informal de 10 líneas de texto encubre decenas de decisiones de arquitectura, seguridad y usabilidad. "
        "El rol del asistente de IA aceleró el hallazgo sistemático de puntos ciegos, pero el juicio crítico del estudiante fue indispensable para aterrizar métricas viables, evitar decisiones de negocio arbitrarias y estructurar criterios de aceptación ejecutables conforme a las directrices de la práctica ADA-04.",
        body_style
    ))

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    build_pdf()
