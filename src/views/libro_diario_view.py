import os
import sys
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QHeaderView, QDateEdit, QFrame, QMessageBox,
                               QFileDialog, QTextEdit, QComboBox, QLineEdit,
                               QSpinBox, QGroupBox, QFormLayout, QSplitter,
                               QTabWidget, QApplication, QScrollArea)
from PySide6.QtCore import Qt, QDate, QTimer
from PySide6.QtGui import QFont, QPalette, QColor, QLinearGradient

# Agregar el directorio raíz al path para imports absolutos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import pandas as pd
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    PANDAS_AVAILABLE = True
    REPORTLAB_AVAILABLE = True
except ImportError as e:
    print(f"❌ Librerías no disponibles: {e}")
    PANDAS_AVAILABLE = False
    REPORTLAB_AVAILABLE = False

try:
    from services.journal_service import JournalService
    from models import get_session, init_db
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Servicios no disponibles: {e}")
    SERVICES_AVAILABLE = False

class LibroDiarioView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.empresa_nombre = "MISKY CHOCLOS S.A."
        self.pagina_actual = 1
        self.asientos_por_pagina = 20
        self.setup_ui()
        self.setup_connections()
        self.cargar_datos_iniciales()
        
    def setup_ui(self):
        """Configura la interfaz completa del libro diario"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)
        
        # Header principal con efecto futurista
        self.setup_header(main_layout)
        
        # Controles de periodo y paginación
        self.setup_controls(main_layout)
        
        # Splitter para área principal
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)
        
        # Sección de asientos contables
        self.setup_asientos_section(splitter)
        
        # Sección de resumen y totales
        self.setup_resumen_section(splitter)
        
        # Configurar proporciones del splitter
        splitter.setSizes([400, 150])
        main_layout.addWidget(splitter)
        
        # Barra de herramientas inferior
        self.setup_toolbar(main_layout)
        
        self.apply_futurist_styles()
        
    def setup_header(self, parent_layout):
        """Configura el encabezado futurista"""
        header_frame = QFrame()
        header_frame.setObjectName("header_frame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(8)
        
        # Nombre de la empresa con efecto neón
        empresa_label = QLabel(self.empresa_nombre)
        empresa_label.setObjectName("empresa_label")
        empresa_label.setAlignment(Qt.AlignCenter)
        
        # Título del libro con efecto glitch
        libro_label = QLabel("📊 LIBRO DIARIO CONTABLE")
        libro_label.setObjectName("libro_label")
        libro_label.setAlignment(Qt.AlignCenter)
        
        # Información del periodo
        info_layout = QHBoxLayout()
        
        periodo_label = QLabel(f"PERIODO: {datetime.now().strftime('%B/%Y').upper()}")
        periodo_label.setObjectName("info_label")
        
        pagina_label = QLabel(f"PÁGINA: {self.pagina_actual}")
        pagina_label.setObjectName("info_label")
        
        usuario_label = QLabel(f"USUARIO: {self.usuario.username.upper()}")
        usuario_label.setObjectName("info_label")
        
        info_layout.addWidget(periodo_label)
        info_layout.addStretch()
        info_layout.addWidget(pagina_label)
        info_layout.addStretch()
        info_layout.addWidget(usuario_label)
        
        header_layout.addWidget(empresa_label)
        header_layout.addWidget(libro_label)
        header_layout.addLayout(info_layout)
        
        parent_layout.addWidget(header_frame)
        
    def setup_controls(self, parent_layout):
        """Configura controles de filtro y paginación"""
        controls_frame = QFrame()
        controls_frame.setObjectName("controls_frame")
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(15)
        
        # Filtros de fecha
        filtros_group = QGroupBox("🕐 FILTRAR POR FECHA")
        filtros_group.setObjectName("filtros_group")
        filtros_layout = QHBoxLayout(filtros_group)
        
        filtros_layout.addWidget(QLabel("Desde:"))
        self.date_desde = QDateEdit()
        self.date_desde.setDate(QDate.currentDate().addMonths(-1))
        self.date_desde.setCalendarPopup(True)
        filtros_layout.addWidget(self.date_desde)
        
        filtros_layout.addWidget(QLabel("Hasta:"))
        self.date_hasta = QDateEdit()
        self.date_hasta.setDate(QDate.currentDate())
        self.date_hasta.setCalendarPopup(True)
        filtros_layout.addWidget(self.date_hasta)
        
        self.btn_filtrar = QPushButton("🔍 APLICAR FILTRO")
        self.btn_filtrar.setObjectName("primary_btn")
        filtros_layout.addWidget(self.btn_filtrar)
        
        # Paginación
        paginacion_group = QGroupBox("📄 PAGINACIÓN")
        paginacion_group.setObjectName("paginacion_group")
        paginacion_layout = QHBoxLayout(paginacion_group)
        
        self.spin_pagina = QSpinBox()
        self.spin_pagina.setMinimum(1)
        self.spin_pagina.setMaximum(100)
        self.spin_pagina.setValue(1)
        
        paginacion_layout.addWidget(QLabel("Página:"))
        paginacion_layout.addWidget(self.spin_pagina)
        paginacion_layout.addWidget(QLabel("de"))
        self.lbl_total_paginas = QLabel("1")
        paginacion_layout.addWidget(self.lbl_total_paginas)
        
        self.btn_anterior = QPushButton("◀ ANTERIOR")
        self.btn_siguiente = QPushButton("SIGUIENTE ▶")
        self.btn_anterior.setObjectName("secondary_btn")
        self.btn_siguiente.setObjectName("secondary_btn")
        
        paginacion_layout.addWidget(self.btn_anterior)
        paginacion_layout.addWidget(self.btn_siguiente)
        
        controls_layout.addWidget(filtros_group)
        controls_layout.addWidget(paginacion_group)
        
        parent_layout.addWidget(controls_frame)
        
    def setup_asientos_section(self, parent_splitter):
        """Configura la sección de asientos contables"""
        asientos_frame = QFrame()
        asientos_frame.setObjectName("asientos_frame")
        asientos_layout = QVBoxLayout(asientos_frame)
        
        # Tabla de asientos contables
        self.tabla_asientos = QTableWidget()
        self.tabla_asientos.setColumnCount(8)
        headers = ["FECHA", "N° ASIENTO", "CÓDIGO CUENTA", "NOMBRE CUENTA", 
                  "DETALLE/GLOBA", "DEBE (Bs)", "HABER (Bs)", "SALDO (Bs)"]
        self.tabla_asientos.setHorizontalHeaderLabels(headers)
        
        # Configurar header
        header = self.tabla_asientos.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Fecha
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # N° Asiento
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Código
        header.setSectionResizeMode(3, QHeaderView.Stretch)          # Nombre
        header.setSectionResizeMode(4, QHeaderView.Stretch)          # Detalle
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Debe
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents) # Haber
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents) # Saldo
        
        self.tabla_asientos.setAlternatingRowColors(True)
        self.tabla_asientos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_asientos.setEditTriggers(QTableWidget.NoEditTriggers)
        
        asientos_layout.addWidget(self.tabla_asientos)
        
        parent_splitter.addWidget(asientos_frame)
        
    def setup_resumen_section(self, parent_splitter):
        """Configura la sección de resumen y totales"""
        resumen_frame = QFrame()
        resumen_frame.setObjectName("resumen_frame")
        resumen_layout = QVBoxLayout(resumen_frame)
        
        # Título del resumen
        resumen_title = QLabel("📈 RESUMEN Y TOTALES")
        resumen_title.setObjectName("resumen_title")
        resumen_layout.addWidget(resumen_title)
        
        # Estadísticas en tiempo real
        stats_layout = QHBoxLayout()
        
        self.lbl_total_asientos = QLabel("Total Asientos: 0")
        self.lbl_total_debe = QLabel("Total Débito: Bs 0.00")
        self.lbl_total_haber = QLabel("Total Crédito: Bs 0.00")
        self.lbl_diferencia = QLabel("Diferencia: Bs 0.00")
        self.lbl_estado = QLabel("Estado: ✅ CUADRADO")
        
        for lbl in [self.lbl_total_asientos, self.lbl_total_debe, 
                   self.lbl_total_haber, self.lbl_diferencia, self.lbl_estado]:
            lbl.setObjectName("stat_label")
            stats_layout.addWidget(lbl)
            
        resumen_layout.addLayout(stats_layout)
        
        # Totales por página
        pagina_layout = QHBoxLayout()
        
        self.lbl_total_pagina_debe = QLabel("Total Página Débito: Bs 0.00")
        self.lbl_total_pagina_haber = QLabel("Total Página Crédito: Bs 0.00")
        self.lbl_acumulado_debe = QLabel("Acumulado Débito: Bs 0.00")
        self.lbl_acumulado_haber = QLabel("Acumulado Crédito: Bs 0.00")
        
        for lbl in [self.lbl_total_pagina_debe, self.lbl_total_pagina_haber,
                   self.lbl_acumulado_debe, self.lbl_acumulado_haber]:
            lbl.setObjectName("total_label")
            pagina_layout.addWidget(lbl)
            
        resumen_layout.addLayout(pagina_layout)
        
        parent_splitter.addWidget(resumen_frame)
        
    def setup_toolbar(self, parent_layout):
        """Configura la barra de herramientas"""
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("toolbar_frame")
        toolbar_layout = QHBoxLayout(toolbar_frame)
        
        # Botones de acción
        acciones = [
            ("🔄 ACTUALIZAR", self.actualizar_datos),
            ("📊 EXPORTAR EXCEL", self.exportar_excel),
            ("📄 EXPORTAR PDF", self.exportar_pdf),
            ("🎯 IR A REGISTRO", self.ir_a_registro),
            ("🖨️ IMPRIMIR", self.imprimir_reporte)
        ]
        
        for texto, slot in acciones:
            btn = QPushButton(texto)
            btn.setObjectName("toolbar_btn")
            btn.clicked.connect(slot)
            toolbar_layout.addWidget(btn)
            
        toolbar_layout.addStretch()
        
        # Contador en tiempo real
        self.lbl_contador = QLabel("🕐 Actualizado: --:--:--")
        self.lbl_contador.setObjectName("contador_label")
        toolbar_layout.addWidget(self.lbl_contador)
        
        parent_layout.addWidget(toolbar_frame)
        
    def setup_connections(self):
        """Configura las conexiones de señales"""
        self.btn_filtrar.clicked.connect(self.aplicar_filtros)
        self.btn_anterior.clicked.connect(self.pagina_anterior)
        self.btn_siguiente.clicked.connect(self.pagina_siguiente)
        self.spin_pagina.valueChanged.connect(self.cambiar_pagina)
        
        # Timer para actualización automática
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_contador)
        self.timer.start(1000)  # Actualizar cada segundo
        
    def cargar_datos_iniciales(self):
        """Carga los datos iniciales del libro diario"""
        if not SERVICES_AVAILABLE:
            self.mostrar_error_servicios()
            return
            
        try:
            self.actualizar_datos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando datos iniciales: {str(e)}")
            
    def actualizar_datos(self):
        """Actualiza todos los datos del libro diario"""
        if not SERVICES_AVAILABLE:
            return
            
        try:
            engine = init_db()
            session = get_session(engine)
            
            journal_service = JournalService()
            
            fecha_desde = self.date_desde.date().toPython()
            fecha_hasta = self.date_hasta.date().toPython()
            
            # Obtener asientos del periodo
            self.asientos = journal_service.obtener_asientos(session, fecha_desde, fecha_hasta)
            
            # Calcular total de páginas
            total_asientos = len(self.asientos)
            self.total_paginas = max(1, (total_asientos + self.asientos_por_pagina - 1) // self.asientos_por_pagina)
            self.lbl_total_paginas.setText(str(self.total_paginas))
            self.spin_pagina.setMaximum(self.total_paginas)
            
            # Mostrar página actual
            self.mostrar_pagina_actual()
            
            # Actualizar estadísticas
            self.actualizar_estadisticas()
            
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error actualizando datos: {str(e)}")
            
    def mostrar_pagina_actual(self):
        """Muestra los asientos de la página actual"""
        if not hasattr(self, 'asientos'):
            return
            
        inicio = (self.pagina_actual - 1) * self.asientos_por_pagina
        fin = min(inicio + self.asientos_por_pagina, len(self.asientos))
        
        asientos_pagina = self.asientos[inicio:fin]
        
        # Limpiar tabla
        self.tabla_asientos.setRowCount(0)
        
        # Llenar tabla con asientos de la página
        fila_global = 0
        total_pagina_debe = 0
        total_pagina_haber = 0
        
        for asiento in asientos_pagina:
            # Agregar fila para cada línea del asiento
            for linea in asiento['lineas']:
                self.tabla_asientos.insertRow(fila_global)
                
                # Fecha
                fecha = asiento['fecha'].strftime('%d/%m/%Y') if hasattr(asiento['fecha'], 'strftime') else asiento['fecha']
                self.tabla_asientos.setItem(fila_global, 0, QTableWidgetItem(fecha))
                
                # Número de asiento
                self.tabla_asientos.setItem(fila_global, 1, QTableWidgetItem(asiento['numero']))
                
                # Código de cuenta
                self.tabla_asientos.setItem(fila_global, 2, QTableWidgetItem(linea['cuenta_codigo']))
                
                # Nombre de cuenta
                self.tabla_asientos.setItem(fila_global, 3, QTableWidgetItem(linea['cuenta_nombre']))
                
                # Detalle/Glosa
                detalle = f"{asiento['descripcion']} - {linea['descripcion']}" if linea['descripcion'] else asiento['descripcion']
                self.tabla_asientos.setItem(fila_global, 4, QTableWidgetItem(detalle))
                
                # Debe
                debe = linea['debe']
                self.tabla_asientos.setItem(fila_global, 5, QTableWidgetItem(f"{debe:,.2f}"))
                total_pagina_debe += debe
                
                # Haber
                haber = linea['haber']
                self.tabla_asientos.setItem(fila_global, 6, QTableWidgetItem(f"{haber:,.2f}"))
                total_pagina_haber += haber
                
                # Saldo (acumulado)
                saldo = debe - haber
                self.tabla_asientos.setItem(fila_global, 7, QTableWidgetItem(f"{saldo:,.2f}"))
                
                # Aplicar estilos según el tipo de movimiento
                self.aplicar_estilo_fila(fila_global, debe, haber)
                
                fila_global += 1
                
            # Agregar línea separadora entre asientos
            if asiento != asientos_pagina[-1]:
                self.tabla_asientos.insertRow(fila_global)
                for col in range(8):
                    item = QTableWidgetItem("─" * 5 if col == 4 else "")
                    item.setFlags(Qt.NoItemFlags)
                    self.tabla_asientos.setItem(fila_global, col, item)
                fila_global += 1
        
        # Actualizar totales de página
        self.lbl_total_pagina_debe.setText(f"Total Página Débito: Bs {total_pagina_debe:,.2f}")
        self.lbl_total_pagina_haber.setText(f"Total Página Crédito: Bs {total_pagina_haber:,.2f}")
        
    def aplicar_estilo_fila(self, fila, debe, haber):
        """Aplica estilos visuales a las filas según el tipo de movimiento"""
        if debe > 0:
            # Movimiento de débito - color azul
            for col in range(8):
                item = self.tabla_asientos.item(fila, col)
                if item:
                    item.setBackground(QColor(30, 58, 138, 50))  # Azul oscuro translúcido
        elif haber > 0:
            # Movimiento de crédito - color rosa
            for col in range(8):
                item = self.tabla_asientos.item(fila, col)
                if item:
                    item.setBackground(QColor(136, 19, 55, 50))  # Rosa oscuro translúcido
                    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas y totales generales"""
        if not hasattr(self, 'asientos'):
            return
            
        total_asientos = len(self.asientos)
        total_debe = 0
        total_haber = 0
        
        # Calcular totales generales
        for asiento in self.asientos:
            for linea in asiento['lineas']:
                total_debe += linea['debe']
                total_haber += linea['haber']
                
        diferencia = total_debe - total_haber
        estado = "✅ CUADRADO" if abs(diferencia) < 0.01 else "❌ DESCUADRADO"
        
        # Actualizar labels
        self.lbl_total_asientos.setText(f"Total Asientos: {total_asientos}")
        self.lbl_total_debe.setText(f"Total Débito: Bs {total_debe:,.2f}")
        self.lbl_total_haber.setText(f"Total Crédito: Bs {total_haber:,.2f}")
        self.lbl_diferencia.setText(f"Diferencia: Bs {diferencia:,.2f}")
        self.lbl_estado.setText(f"Estado: {estado}")
        
        # Calcular acumulados
        inicio = (self.pagina_actual - 1) * self.asientos_por_pagina
        acumulado_debe = 0
        acumulado_haber = 0
        
        for i in range(inicio):
            if i < len(self.asientos):
                for linea in self.asientos[i]['lineas']:
                    acumulado_debe += linea['debe']
                    acumulado_haber += linea['haber']
                    
        self.lbl_acumulado_debe.setText(f"Acumulado Débito: Bs {acumulado_debe:,.2f}")
        self.lbl_acumulado_haber.setText(f"Acumulado Crédito: Bs {acumulado_haber:,.2f}")
        
        # Resaltar estado
        if abs(diferencia) > 0.01:
            self.lbl_estado.setStyleSheet("color: #FF4444; font-weight: bold;")
        else:
            self.lbl_estado.setStyleSheet("color: #00FF88; font-weight: bold;")
            
    def aplicar_filtros(self):
        """Aplica los filtros de fecha"""
        self.pagina_actual = 1
        self.spin_pagina.setValue(1)
        self.actualizar_datos()
        
    def cambiar_pagina(self, pagina):
        """Cambia a la página especificada"""
        self.pagina_actual = pagina
        self.mostrar_pagina_actual()
        self.actualizar_estadisticas()
        
    def pagina_anterior(self):
        """Va a la página anterior"""
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.spin_pagina.setValue(self.pagina_actual)
            
    def pagina_siguiente(self):
        """Va a la página siguiente"""
        if self.pagina_actual < self.total_paginas:
            self.pagina_actual += 1
            self.spin_pagina.setValue(self.pagina_actual)
            
    def actualizar_contador(self):
        """Actualiza el contador de tiempo"""
        hora_actual = datetime.now().strftime("%H:%M:%S")
        self.lbl_contador.setText(f"🕐 Actualizado: {hora_actual}")
        
    def exportar_excel(self):
        """Exporta el libro diario a Excel"""
        if not PANDAS_AVAILABLE:
            QMessageBox.warning(self, "Error", "Pandas no está disponible para exportación Excel")
            return
            
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Libro Diario", "libro_diario.xlsx", "Excel Files (*.xlsx)")
                
            if file_path:
                # Preparar datos para exportación
                data = []
                for asiento in self.asientos:
                    for linea in asiento['lineas']:
                        data.append({
                            'Fecha': asiento['fecha'].strftime('%d/%m/%Y') if hasattr(asiento['fecha'], 'strftime') else asiento['fecha'],
                            'Número Asiento': asiento['numero'],
                            'Código Cuenta': linea['cuenta_codigo'],
                            'Nombre Cuenta': linea['cuenta_nombre'],
                            'Detalle/Glosa': f"{asiento['descripcion']} - {linea['descripcion']}",
                            'Débito (Bs)': linea['debe'],
                            'Crédito (Bs)': linea['haber'],
                            'Saldo (Bs)': linea['debe'] - linea['haber']
                        })
                
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False, engine='openpyxl')
                QMessageBox.information(self, "Éxito", "Libro diario exportado a Excel correctamente")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exportando a Excel: {str(e)}")
            
    def exportar_pdf(self):
        """Exporta el libro diario a PDF"""
        if not REPORTLAB_AVAILABLE:
            QMessageBox.warning(self, "Error", "ReportLab no está disponible para exportación PDF")
            return
            
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Libro Diario", "libro_diario.pdf", "PDF Files (*.pdf)")
                
            if file_path:
                self.generar_pdf(file_path)
                QMessageBox.information(self, "Éxito", "Libro diario exportado a PDF correctamente")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exportando a PDF: {str(e)}")
            
    def generar_pdf(self, file_path):
        """Genera el archivo PDF del libro diario"""
        doc = SimpleDocTemplate(file_path, pagesize=A4, topMargin=0.5*inch)
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para el título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#00E5FF'),
            alignment=1,  # Centrado
            spaceAfter=20
        )
        
        # Encabezado
        elements.append(Paragraph(self.empresa_nombre, title_style))
        elements.append(Paragraph("LIBRO DIARIO CONTABLE", styles['Heading2']))
        elements.append(Paragraph(f"Período: {self.date_desde.date().toString('dd/MM/yyyy')} - {self.date_hasta.date().toString('dd/MM/yyyy')}", styles['Normal']))
        elements.append(Paragraph(f"Página: {self.pagina_actual} de {self.total_paginas}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Preparar datos para la tabla
        table_data = [['Fecha', 'Asiento', 'Código', 'Cuenta', 'Detalle', 'Débito', 'Crédito']]
        
        for asiento in self.asientos:
            for linea in asiento['lineas']:
                fecha = asiento['fecha'].strftime('%d/%m/%Y') if hasattr(asiento['fecha'], 'strftime') else asiento['fecha']
                table_data.append([
                    fecha,
                    asiento['numero'],
                    linea['cuenta_codigo'],
                    linea['cuenta_nombre'],
                    f"{asiento['descripcion']} - {linea['descripcion']}",
                    f"{linea['debe']:,.2f}",
                    f"{linea['haber']:,.2f}"
                ])
        
        # Crear tabla
        table = Table(table_data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 1.5*inch, 2*inch, 0.8*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#00E5FF')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#334155'))
        ]))
        
        elements.append(table)
        doc.build(elements)
        
    def ir_a_registro(self):
        """Navega al módulo de registro de asientos"""
        # Esta función puede ser conectada al sistema de navegación principal
        QMessageBox.information(self, "Navegación", "Redirigiendo al módulo de registro de asientos...")
        
    def imprimir_reporte(self):
        """Prepara el reporte para impresión"""
        QMessageBox.information(self, "Imprimir", "Preparando reporte para impresión...")
        
    def mostrar_error_servicios(self):
        """Muestra error cuando los servicios no están disponibles"""
        QMessageBox.critical(self, "Error", 
                           "Los servicios contables no están disponibles.\n"
                           "Verifique la conexión a la base de datos y la configuración.")
                           
    def apply_futurist_styles(self):
        """Aplica estilos futuristas a toda la interfaz"""
        futurist_style = """
            /* Estilos generales */
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0A0E17, stop:0.5 #13182B, stop:1 #0A0E17);
                color: #E6EEF3;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }

            /* Encabezado principal */
            #header_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 229, 255, 0.1),
                    stop:0.5 rgba(179, 0, 158, 0.1),
                    stop:1 rgba(0, 229, 255, 0.1));
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 12px;
                padding: 15px;
                margin: 5px;
            }

            #empresa_label {
                color: #00E5FF;
                font-size: 18px;
                font-weight: 800;
                letter-spacing: 1px;
                text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
            }

            #libro_label {
                color: #B3009E;
                font-size: 24px;
                font-weight: 900;
                letter-spacing: 2px;
                text-shadow: 0 0 15px rgba(179, 0, 158, 0.6);
            }

            #info_label {
                color: #94A3B8;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }

            /* Controles */
            #controls_frame {
                background: rgba(30, 41, 59, 0.7);
                border: 1px solid rgba(255, 0, 128, 0.2);
                border-radius: 8px;
                padding: 10px;
            }

            QGroupBox {
                color: #00E5FF;
                font-weight: bold;
                font-size: 12px;
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #00E5FF;
            }

            /* Botones principales */
            #primary_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #B3009E);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
                min-height: 25px;
            }

            #primary_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00F7FF, stop:1 #FF0080);
                border: 1px solid rgba(0, 229, 255, 0.6);
            }

            #secondary_btn {
                background: rgba(30, 41, 59, 0.8);
                color: #00E5FF;
                border: 1px solid rgba(0, 229, 255, 0.4);
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 10px;
            }

            #secondary_btn:hover {
                background: rgba(0, 229, 255, 0.1);
                border: 1px solid rgba(0, 229, 255, 0.8);
            }

            /* Tabla de asientos */
            #asientos_frame {
                background: rgba(15, 23, 42, 0.9);
                border: 1px solid rgba(0, 229, 255, 0.2);
                border-radius: 8px;
            }

            QTableWidget {
                background: rgba(26, 29, 33, 0.8);
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 6px;
                gridline-color: rgba(0, 229, 255, 0.2);
                font-size: 10px;
            }

            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid rgba(0, 229, 255, 0.1);
            }

            QTableWidget::item:selected {
                background: rgba(0, 229, 255, 0.3);
            }

            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #B3009E);
                color: white;
                font-weight: bold;
                padding: 6px;
                border: none;
                font-size: 9px;
            }

            /* Resumen y totales */
            #resumen_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 229, 255, 0.05),
                    stop:1 rgba(255, 0, 128, 0.05));
                border: 1px solid rgba(0, 229, 255, 0.2);
                border-radius: 8px;
                padding: 10px;
            }

            #resumen_title {
                color: #00E5FF;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 8px;
            }

            #stat_label, #total_label {
                font-size: 11px;
                font-weight: 600;
                padding: 4px 8px;
                border-radius: 4px;
                background: rgba(30, 41, 59, 0.5);
            }

            #stat_label {
                color: #E6EEF3;
            }

            #total_label {
                color: #00E5FF;
            }

            /* Barra de herramientas */
            #toolbar_frame {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(255, 0, 128, 0.2);
                border-radius: 8px;
                padding: 8px;
            }

            #toolbar_btn {
                background: rgba(0, 229, 255, 0.1);
                color: #00E5FF;
                border: 1px solid rgba(0, 229, 255, 0.4);
                border-radius: 5px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 10px;
                min-height: 25px;
            }

            #toolbar_btn:hover {
                background: rgba(0, 229, 255, 0.2);
                border: 1px solid rgba(0, 229, 255, 0.8);
            }

            #contador_label {
                color: #B3009E;
                font-size: 10px;
                font-weight: bold;
                font-family: 'Courier New';
            }

            /* Controles de formulario */
            QDateEdit, QSpinBox {
                background: rgba(26, 29, 33, 0.8);
                border: 1px solid rgba(0, 229, 255, 0.4);
                border-radius: 4px;
                padding: 4px;
                color: #E6EEF3;
                font-size: 10px;
            }

            QDateEdit::drop-down, QSpinBox::up-button, QSpinBox::down-button {
                background: rgba(0, 229, 255, 0.2);
                border: none;
            }
        """
        self.setStyleSheet(futurist_style)