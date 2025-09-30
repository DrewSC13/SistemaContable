import os
import sys
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QTableWidget, QTableWidgetItem,
                             QPushButton, QLineEdit, QDateEdit, QComboBox,
                             QTextEdit, QHeaderView, QMessageBox, QTabWidget,
                             QSplitter, QFormLayout, QDoubleSpinBox, QToolBar,
                             QAbstractItemView, QSizePolicy)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QAction

# Agregar el directorio raíz al path para imports absolutos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Importación absoluta corregida
try:
    from services.journal_service import JournalService
    from models import get_session, init_db
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Servicios no disponibles: {e}")
    SERVICES_AVAILABLE = False

class JournalView(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.lineas_asiento = []
        self.setup_ui()
        self.conectar_señales()
        
    def setup_ui(self):
        # Layout principal con tamaño flexible
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        
        # Título responsivo
        title = QLabel("📖 LIBRO DIARIO")
        title.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 20px;
            font-weight: bold;
            color: #00E5FF;
            padding: 12px;
            background: rgba(26, 29, 33, 0.8);
            border-radius: 8px;
            border: 1px solid #2B2F36;
        """)
        title.setAlignment(Qt.AlignCenter)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(title)
        
        # Toolbar responsiva
        toolbar = self.create_toolbar()
        main_layout.addWidget(toolbar)
        
        # Contenedor principal con scroll implícito
        self.setup_main_content(main_layout)
    
    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setStyleSheet("""
            QToolBar {
                background: rgba(26, 29, 33, 0.8);
                border: 1px solid #2B2F36;
                border-radius: 6px;
                padding: 6px;
                spacing: 8px;
            }
        """)
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Botones de acción responsivos
        self.btn_nuevo = QAction("🆕 NUEVO", self)
        self.btn_guardar = QAction("💾 GUARDAR", self)
        self.btn_cancelar = QAction("❌ CANCELAR", self)
        self.btn_eliminar = QAction("🗑️ ELIMINAR", self)
        
        toolbar.addAction(self.btn_nuevo)
        toolbar.addAction(self.btn_guardar)
        toolbar.addAction(self.btn_cancelar)
        toolbar.addSeparator()
        toolbar.addAction(self.btn_eliminar)
        
        return toolbar
    
    def setup_main_content(self, parent_layout):
        # Contenedor principal con layout flexible
        main_container = QFrame()
        main_container.setStyleSheet("""
            QFrame {
                background: rgba(26, 29, 33, 0.6);
                border: 1px solid #2B2F36;
                border-radius: 8px;
            }
        """)
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # Sección de información del asiento
        self.setup_asiento_section(main_layout)
        
        # Sección de líneas del asiento
        self.setup_lineas_section(main_layout)
        
        # Sección de asientos existentes
        self.setup_historial_section(main_layout)
        
        parent_layout.addWidget(main_container)
    
    def setup_asiento_section(self, parent_layout):
        info_frame = QFrame()
        info_frame.setObjectName("card")
        info_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        info_layout = QFormLayout(info_frame)
        info_layout.setHorizontalSpacing(15)
        info_layout.setVerticalSpacing(8)
        
        # Fila 1: Número y Fecha (layout horizontal responsivo)
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(10)
        
        # Número de asiento
        num_layout = QVBoxLayout()
        num_layout.addWidget(QLabel("N° ASIENTO:"))
        self.txt_numero = QLineEdit()
        self.txt_numero.setPlaceholderText("Generado automáticamente...")
        self.txt_numero.setReadOnly(True)
        self.txt_numero.setStyleSheet("""
            QLineEdit {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #00E5FF;
                font-weight: bold;
                min-width: 150px;
            }
        """)
        num_layout.addWidget(self.txt_numero)
        row1_layout.addLayout(num_layout)
        
        # Fecha
        fecha_layout = QVBoxLayout()
        fecha_layout.addWidget(QLabel("FECHA:"))
        self.date_fecha = QDateEdit()
        self.date_fecha.setDate(QDate.currentDate())
        self.date_fecha.setCalendarPopup(True)
        self.date_fecha.setStyleSheet("""
            QDateEdit {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #E6EEF3;
                min-width: 120px;
            }
        """)
        fecha_layout.addWidget(self.date_fecha)
        row1_layout.addLayout(fecha_layout)
        
        row1_layout.addStretch()
        info_layout.addRow(row1_layout)
        
        # Descripción
        info_layout.addRow("DESCRIPCIÓN:", self.create_descripcion_widget())
        
        parent_layout.addWidget(info_frame)
    
    def setup_lineas_section(self, parent_layout):
        lines_frame = QFrame()
        lines_frame.setObjectName("card")
        lines_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        lines_layout = QVBoxLayout(lines_frame)
        lines_layout.setSpacing(8)
        
        # Título
        lines_title = QLabel("📋 LÍNEAS DEL ASIENTO")
        lines_title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #00E5FF;
            padding: 8px;
            border-bottom: 1px solid #2B2F36;
        """)
        lines_layout.addWidget(lines_title)
        
        # Controles para agregar líneas (layout responsivo)
        line_controls = QHBoxLayout()
        line_controls.setSpacing(8)
        
        # Cuenta contable - simplificada
        cuenta_layout = QVBoxLayout()
        cuenta_layout.addWidget(QLabel("CUENTA:"))
        self.combo_cuenta = QComboBox()
        self.combo_cuenta.setStyleSheet("""
            QComboBox {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #E6EEF3;
                min-width: 200px;
            }
        """)
        cuenta_layout.addWidget(self.combo_cuenta)
        line_controls.addLayout(cuenta_layout)
        
        # Descripción de línea
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("DESCRIPCIÓN:"))
        self.txt_linea_desc = QLineEdit()
        self.txt_linea_desc.setPlaceholderText("Descripción...")
        self.txt_linea_desc.setStyleSheet("""
            QLineEdit {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #E6EEF3;
            }
        """)
        desc_layout.addWidget(self.txt_linea_desc)
        line_controls.addLayout(desc_layout)
        
        # Montos (Debe y Haber en layout horizontal)
        montos_layout = QHBoxLayout()
        montos_layout.setSpacing(6)
        
        # Debe
        debe_layout = QVBoxLayout()
        debe_layout.addWidget(QLabel("DEBE:"))
        self.spin_debe = QDoubleSpinBox()
        self.spin_debe.setMaximum(9999999.99)
        self.spin_debe.setPrefix("Bs ")
        self.spin_debe.setStyleSheet("""
            QDoubleSpinBox {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #E6EEF3;
                min-width: 100px;
            }
        """)
        debe_layout.addWidget(self.spin_debe)
        montos_layout.addLayout(debe_layout)
        
        # Haber
        haber_layout = QVBoxLayout()
        haber_layout.addWidget(QLabel("HABER:"))
        self.spin_haber = QDoubleSpinBox()
        self.spin_haber.setMaximum(9999999.99)
        self.spin_haber.setPrefix("Bs ")
        self.spin_haber.setStyleSheet("""
            QDoubleSpinBox {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #E6EEF3;
                min-width: 100px;
            }
        """)
        haber_layout.addWidget(self.spin_haber)
        montos_layout.addLayout(haber_layout)
        
        line_controls.addLayout(montos_layout)
        
        # Botón agregar
        self.btn_agregar_linea = QPushButton("➕ AGREGAR")
        self.btn_agregar_linea.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #B3009E);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00F7FF, stop:1 #FF0080);
            }
            QPushButton:disabled {
                background: #2B2F36;
                color: #6B7280;
            }
        """)
        self.btn_agregar_linea.setFixedWidth(100)
        line_controls.addWidget(self.btn_agregar_linea)
        
        lines_layout.addLayout(line_controls)
        
        # Tabla de líneas
        self.tabla_lineas = QTableWidget()
        self.tabla_lineas.setColumnCount(5)
        self.tabla_lineas.setHorizontalHeaderLabels(["CUENTA", "DESCRIPCIÓN", "DEBE", "HABER", "ACCIÓN"])
        self.tabla_lineas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_lineas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_lineas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_lineas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.tabla_lineas.setStyleSheet("""
            QTableWidget {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                gridline-color: #2B2F36;
                min-height: 150px;
            }
            QHeaderView::section {
                background: #101315;
                color: #00E5FF;
                font-weight: bold;
                padding: 6px;
                border: none;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #2B2F36;
                font-size: 11px;
            }
            QTableWidget::item:selected {
                background: rgba(0, 229, 255, 0.2);
            }
        """)
        
        lines_layout.addWidget(self.tabla_lineas)
        
        # Totales
        self.setup_totales_section(lines_layout)
        
        parent_layout.addWidget(lines_frame)
    
    def setup_totales_section(self, parent_layout):
        totals_layout = QHBoxLayout()
        totals_layout.setSpacing(15)
        
        self.lbl_total_debe = QLabel("TOTAL DEBE: Bs 0.00")
        self.lbl_total_debe.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #00E5FF;
            padding: 8px;
            background: rgba(0, 229, 255, 0.1);
            border-radius: 4px;
        """)
        
        self.lbl_total_haber = QLabel("TOTAL HABER: Bs 0.00")
        self.lbl_total_haber.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #00E5FF;
            padding: 8px;
            background: rgba(0, 229, 255, 0.1);
            border-radius: 4px;
        """)
        
        self.lbl_diferencia = QLabel("DIFERENCIA: Bs 0.00")
        self.lbl_diferencia.setStyleSheet("""
            font-size: 12px;
            font-weight: bold;
            color: #00FF88;
            padding: 8px;
            background: rgba(0, 255, 136, 0.1);
            border-radius: 4px;
        """)
        
        totals_layout.addWidget(self.lbl_total_debe)
        totals_layout.addWidget(self.lbl_total_haber)
        totals_layout.addWidget(self.lbl_diferencia)
        totals_layout.addStretch()
        
        parent_layout.addLayout(totals_layout)
    
    def setup_historial_section(self, parent_layout):
        history_frame = QFrame()
        history_frame.setObjectName("card")
        history_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        history_layout = QVBoxLayout(history_frame)
        history_layout.setSpacing(8)
        
        history_title = QLabel("📜 ASIENTOS REGISTRADOS")
        history_title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #00E5FF;
            padding: 8px;
            border-bottom: 1px solid #2B2F36;
        """)
        history_layout.addWidget(history_title)
        
        # Filtros responsivos
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(8)
        
        # Fecha desde
        desde_layout = QVBoxLayout()
        desde_layout.addWidget(QLabel("DESDE:"))
        self.date_desde = QDateEdit()
        self.date_desde.setDate(QDate.currentDate().addDays(-30))
        self.date_desde.setCalendarPopup(True)
        self.date_desde.setStyleSheet("""
            QDateEdit {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #E6EEF3;
                min-width: 120px;
            }
        """)
        desde_layout.addWidget(self.date_desde)
        filter_layout.addLayout(desde_layout)
        
        # Fecha hasta
        hasta_layout = QVBoxLayout()
        hasta_layout.addWidget(QLabel("HASTA:"))
        self.date_hasta = QDateEdit()
        self.date_hasta.setDate(QDate.currentDate())
        self.date_hasta.setCalendarPopup(True)
        self.date_hasta.setStyleSheet("""
            QDateEdit {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #E6EEF3;
                min-width: 120px;
            }
        """)
        hasta_layout.addWidget(self.date_hasta)
        filter_layout.addLayout(hasta_layout)
        
        self.btn_filtrar = QPushButton("🔍 FILTRAR")
        self.btn_filtrar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #B3009E);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00F7FF, stop:1 #FF0080);
            }
        """)
        self.btn_filtrar.setFixedWidth(100)
        filter_layout.addWidget(self.btn_filtrar)
        
        filter_layout.addStretch()
        history_layout.addLayout(filter_layout)
        
        # Tabla de asientos
        self.tabla_asientos = QTableWidget()
        self.tabla_asientos.setColumnCount(5)
        self.tabla_asientos.setHorizontalHeaderLabels(["N° ASIENTO", "FECHA", "DESCRIPCIÓN", "TOTAL", "ESTADO"])
        self.tabla_asientos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_asientos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_asientos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_asientos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.tabla_asientos.setStyleSheet("""
            QTableWidget {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                gridline-color: #2B2F36;
                min-height: 200px;
            }
            QHeaderView::section {
                background: #101315;
                color: #00E5FF;
                font-weight: bold;
                padding: 6px;
                border: none;
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #2B2F36;
                font-size: 11px;
            }
            QTableWidget::item:selected {
                background: rgba(0, 229, 255, 0.2);
            }
        """)
        
        history_layout.addWidget(self.tabla_asientos)
        parent_layout.addWidget(history_frame)
    
    def create_descripcion_widget(self):
        self.txt_descripcion = QTextEdit()
        self.txt_descripcion.setMaximumHeight(50)
        self.txt_descripcion.setPlaceholderText("Descripción del asiento contable...")
        self.txt_descripcion.setStyleSheet("""
            QTextEdit {
                background: #1A1D21;
                border: 1px solid #2B2F36;
                border-radius: 4px;
                padding: 6px;
                color: #E6EEF3;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
            }
        """)
        return self.txt_descripcion
    
    def conectar_señales(self):
        self.btn_nuevo.triggered.connect(self.nuevo_asiento)
        self.btn_guardar.triggered.connect(self.guardar_asiento)
        self.btn_cancelar.triggered.connect(self.cancelar_edicion)
        self.btn_eliminar.triggered.connect(self.eliminar_asiento)
        self.btn_agregar_linea.clicked.connect(self.agregar_linea)
        self.btn_filtrar.clicked.connect(self.filtrar_asientos)
        
        self.spin_debe.valueChanged.connect(self.calcular_totales)
        self.spin_haber.valueChanged.connect(self.calcular_totales)
    
    def cargar_datos_iniciales(self):
        self.nuevo_asiento()
        self.filtrar_asientos()
    
    def nuevo_asiento(self):
        if not SERVICES_AVAILABLE:
            QMessageBox.critical(self, "Error", "Servicios no disponibles. Verifique la configuración.")
            return
            
        try:
            engine = init_db()
            session = get_session(engine)
            
            journal_service = JournalService()
            numero_asiento = journal_service.generar_numero_asiento(session)
            self.txt_numero.setText(numero_asiento)
            
            # Cargar cuentas contables básicas
            cuentas = journal_service.obtener_cuentas_contables(session)
            self.combo_cuenta.clear()
            for cuenta in cuentas:
                self.combo_cuenta.addItem(f"{cuenta['codigo']} - {cuenta['nombre']}", cuenta['id'])
            
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error cargando datos: {str(e)}")
            # Generar número de asiento básico si hay error
            fecha_actual = datetime.now()
            self.txt_numero.setText(f"AS-{fecha_actual.strftime('%Y%m%d')}-001")
        
        # Limpiar formulario
        self.date_fecha.setDate(QDate.currentDate())
        self.txt_descripcion.clear()
        self.tabla_lineas.setRowCount(0)
        self.lineas_asiento = []
        self.calcular_totales()
    
    def agregar_linea(self):
        if self.combo_cuenta.currentIndex() == -1:
            QMessageBox.warning(self, "Advertencia", "❌ Selecciona una cuenta contable")
            return
        
        if self.spin_debe.value() == 0 and self.spin_haber.value() == 0:
            QMessageBox.warning(self, "Advertencia", "❌ Ingresa un valor en Debe o Haber")
            return
        
        cuenta_text = self.combo_cuenta.currentText()
        cuenta_id = self.combo_cuenta.currentData()
        descripcion = self.txt_linea_desc.text()
        debe = self.spin_debe.value()
        haber = self.spin_haber.value()
        
        # Agregar a la lista temporal
        self.lineas_asiento.append({
            'cuenta_id': cuenta_id,
            'cuenta_text': cuenta_text,
            'descripcion': descripcion,
            'debe': debe,
            'haber': haber
        })
        
        # Actualizar tabla
        self.actualizar_tabla_lineas()
        
        # Limpiar controles
        self.txt_linea_desc.clear()
        self.spin_debe.setValue(0)
        self.spin_haber.setValue(0)
        
        # Calcular totales
        self.calcular_totales()
    
    def actualizar_tabla_lineas(self):
        self.tabla_lineas.setRowCount(len(self.lineas_asiento))
        
        for row, linea in enumerate(self.lineas_asiento):
            self.tabla_lineas.setItem(row, 0, QTableWidgetItem(linea['cuenta_text']))
            self.tabla_lineas.setItem(row, 1, QTableWidgetItem(linea['descripcion']))
            self.tabla_lineas.setItem(row, 2, QTableWidgetItem(f"Bs {linea['debe']:,.2f}"))
            self.tabla_lineas.setItem(row, 3, QTableWidgetItem(f"Bs {linea['haber']:,.2f}"))
            
            # Botón eliminar
            btn_eliminar = QPushButton("🗑️")
            btn_eliminar.setStyleSheet("""
                QPushButton {
                    background: #E53E3E;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 4px;
                    font-weight: bold;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background: #C53030;
                }
            """)
            btn_eliminar.clicked.connect(lambda checked, r=row: self.eliminar_linea(r))
            self.tabla_lineas.setCellWidget(row, 4, btn_eliminar)
    
    def eliminar_linea(self, row):
        if 0 <= row < len(self.lineas_asiento):
            self.lineas_asiento.pop(row)
            self.actualizar_tabla_lineas()
            self.calcular_totales()
    
    def calcular_totales(self):
        total_debe = sum(linea['debe'] for linea in self.lineas_asiento)
        total_haber = sum(linea['haber'] for linea in self.lineas_asiento)
        diferencia = total_debe - total_haber
        
        self.lbl_total_debe.setText(f"TOTAL DEBE: Bs {total_debe:,.2f}")
        self.lbl_total_haber.setText(f"TOTAL HABER: Bs {total_haber:,.2f}")
        self.lbl_diferencia.setText(f"DIFERENCIA: Bs {diferencia:,.2f}")
        
        # Resaltar si no está cuadrado
        if abs(diferencia) > 0.01:
            self.lbl_diferencia.setStyleSheet("""
                font-size: 12px;
                font-weight: bold;
                color: #FF4444;
                padding: 8px;
                background: rgba(255, 68, 68, 0.1);
                border-radius: 4px;
            """)
        else:
            self.lbl_diferencia.setStyleSheet("""
                font-size: 12px;
                font-weight: bold;
                color: #00FF88;
                padding: 8px;
                background: rgba(0, 255, 136, 0.1);
                border-radius: 4px;
            """)
    
    def guardar_asiento(self):
        if not SERVICES_AVAILABLE:
            QMessageBox.critical(self, "Error", "Servicios no disponibles. Verifique la configuración.")
            return

        # Validaciones básicas
        if not self.txt_numero.text().strip():
            QMessageBox.warning(self, "Advertencia", "❌ El número de asiento es requerido")
            return
        
        if len(self.lineas_asiento) == 0:
            QMessageBox.warning(self, "Advertencia", "❌ Debe agregar al menos una línea al asiento")
            return
        
        # Verificar que esté cuadrado
        total_debe = sum(linea['debe'] for linea in self.lineas_asiento)
        total_haber = sum(linea['haber'] for linea in self.lineas_asiento)
        
        if abs(total_debe - total_haber) > 0.01:
            QMessageBox.warning(self, "Advertencia", 
                              f"❌ El asiento no está cuadrado!\n"
                              f"Debe: Bs {total_debe:,.2f}\n"
                              f"Haber: Bs {total_haber:,.2f}\n"
                              f"Diferencia: Bs {total_debe - total_haber:,.2f}")
            return
        
        try:
            engine = init_db()
            session = get_session(engine)
            
            journal_service = JournalService()
            
            # Preparar líneas para el servicio
            lineas_servicio = []
            for linea in self.lineas_asiento:
                lineas_servicio.append({
                    'cuenta_id': linea['cuenta_id'],
                    'debe': linea['debe'],
                    'haber': linea['haber'],
                    'descripcion': linea['descripcion']
                })
            
            # Obtener descripción
            descripcion = self.txt_descripcion.toPlainText()
            
            # Crear asiento
            fecha = self.date_fecha.date().toPython()
            success, mensaje = journal_service.crear_asiento(
                session=session,
                numero=self.txt_numero.text(),
                fecha=fecha,
                descripcion=descripcion,
                lineas=lineas_servicio,
                usuario_id=self.usuario.id
            )
            
            if success:
                QMessageBox.information(self, "✅ Éxito", mensaje)
                self.nuevo_asiento()
                self.filtrar_asientos()
            else:
                QMessageBox.critical(self, "❌ Error", mensaje)
            
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"Error guardando asiento: {str(e)}")
    
    def eliminar_asiento(self):
        current_row = self.tabla_asientos.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "Advertencia", "❌ Selecciona un asiento para eliminar")
            return
        
        numero_asiento = self.tabla_asientos.item(current_row, 0).text()
        
        reply = QMessageBox.question(self, "Confirmar Eliminación", 
                                   f"¿Estás seguro de eliminar el asiento {numero_asiento}?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if not SERVICES_AVAILABLE:
                QMessageBox.critical(self, "Error", "Servicios no disponibles. Verifique la configuración.")
                return
                
            try:
                engine = init_db()
                session = get_session(engine)
                
                journal_service = JournalService()
                
                # Buscar el asiento por número
                asientos = journal_service.obtener_asientos(session)
                asiento_id = None
                for asiento in asientos:
                    if asiento['numero'] == numero_asiento:
                        asiento_id = asiento['id']
                        break
                
                if asiento_id:
                    success, mensaje = journal_service.eliminar_asiento(
                        session=session, 
                        asiento_id=asiento_id, 
                        usuario_id=self.usuario.id
                    )
                    
                    if success:
                        QMessageBox.information(self, "✅ Éxito", mensaje)
                        self.filtrar_asientos()
                    else:
                        QMessageBox.critical(self, "❌ Error", mensaje)
                else:
                    QMessageBox.warning(self, "Advertencia", "Asiento no encontrado")
                
                session.close()
                
            except Exception as e:
                QMessageBox.critical(self, "❌ Error", f"Error eliminando asiento: {str(e)}")
    
    def filtrar_asientos(self):
        if not SERVICES_AVAILABLE:
            QMessageBox.critical(self, "Error", "Servicios no disponibles. Verifique la configuración.")
            return
            
        try:
            engine = init_db()
            session = get_session(engine)
            
            journal_service = JournalService()
            
            fecha_desde = self.date_desde.date().toPython()
            fecha_hasta = self.date_hasta.date().toPython()
            
            asientos = journal_service.obtener_asientos(session, fecha_desde, fecha_hasta)
            
            self.tabla_asientos.setRowCount(len(asientos))
            
            for row, asiento in enumerate(asientos):
                self.tabla_asientos.setItem(row, 0, QTableWidgetItem(asiento['numero']))
                self.tabla_asientos.setItem(row, 1, QTableWidgetItem(asiento['fecha'].strftime('%d/%m/%Y')))
                self.tabla_asientos.setItem(row, 2, QTableWidgetItem(asiento['descripcion']))
                
                total = sum(linea['debe'] for linea in asiento['lineas'])
                self.tabla_asientos.setItem(row, 3, QTableWidgetItem(f"Bs {total:,.2f}"))
                self.tabla_asientos.setItem(row, 4, QTableWidgetItem("✅ ACTIVO"))
            
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Error", f"Error cargando asientos: {str(e)}")
    
    def cancelar_edicion(self):
        reply = QMessageBox.question(self, "Confirmar Cancelación",
                                   "¿Estás seguro de cancelar la edición?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.nuevo_asiento()

    # Asegurar que las señales se conecten después de inicializar
    def showEvent(self, event):
        super().showEvent(event)
        self.cargar_datos_iniciales()