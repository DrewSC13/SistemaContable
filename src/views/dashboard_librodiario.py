import os
import sys
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QHeaderView, QDateEdit, QFrame,
                               QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, QDate

# Agregar el directorio raíz al path para imports absolutos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    PANDAS_AVAILABLE = True
except ImportError as e:
    print(f"❌ Pandas/Matplotlib no disponibles: {e}")
    PANDAS_AVAILABLE = False

try:
    from services.journal_service import JournalService
    from models import get_session
except ImportError as e:
    print(f"❌ Error importando servicios: {e}")
    # Fallback para cuando los servicios no estén disponibles
    class JournalService:
        def __init__(self):
            pass
        
        def obtener_asientos(self, session, fecha_inicio=None, fecha_fin=None):
            return []
        
        def obtener_estadisticas_generales(self, session, fecha_inicio=None, fecha_fin=None):
            return {
                'total_asientos': 0,
                'total_debe': 0,
                'total_haber': 0,
                'balance': 0,
                'periodo': 'Sin datos'
            }

class DashboardLibroDiario(QWidget):
    def __init__(self, usuario=None):
        super().__init__()
        self.usuario = usuario
        self.journal_service = JournalService()
        try:
            self.session = get_session()
        except:
            self.session = None
            
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Configura la interfaz de usuario del dashboard del libro diario"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)
        
        # Stats cards
        stats_layout = self.create_stats_cards()
        main_layout.addLayout(stats_layout)
        
        # Controls section
        controls_layout = self.create_controls()
        main_layout.addLayout(controls_layout)
        
        # Table section
        table_section = self.create_table_section()
        main_layout.addWidget(table_section)
        
        # Charts section (solo si pandas está disponible)
        if PANDAS_AVAILABLE:
            charts_layout = self.create_charts_section()
            main_layout.addLayout(charts_layout)
        else:
            warning_label = QLabel("⚠️ Para gráficos avanzados, instale: pandas, matplotlib, seaborn")
            warning_label.setStyleSheet("color: #FF6B6B; font-size: 12px; padding: 10px;")
            warning_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(warning_label)
        
        self.setLayout(main_layout)
        self.apply_styles()
        
    def create_header(self):
        """Crea el encabezado del dashboard"""
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("📊 DASHBOARD - LIBRO DIARIO")
        title_label.setObjectName("dashboard_title")
        
        # Date info
        date_label = QLabel(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        date_label.setObjectName("date_label")
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(date_label)
        
        return header_layout
        
    def create_stats_cards(self):
        """Crea las tarjetas de estadísticas"""
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        # Total transactions card
        self.total_transactions_card = self.create_stat_card(
            "📈 Total Asientos", "0", "#2E86AB")
        
        # Total debit card
        self.total_debit_card = self.create_stat_card(
            "💰 Total Débito (Bs)", "0.00", "#A23B72")
        
        # Total credit card
        self.total_credit_card = self.create_stat_card(
            "💳 Total Crédito (Bs)", "0.00", "#F18F01")
        
        # Balance card
        self.balance_card = self.create_stat_card(
            "⚖️ Balance (Bs)", "0.00", "#2E8B57")
        
        stats_layout.addWidget(self.total_transactions_card)
        stats_layout.addWidget(self.total_debit_card)
        stats_layout.addWidget(self.total_credit_card)
        stats_layout.addWidget(self.balance_card)
        
        return stats_layout
        
    def create_stat_card(self, title, value, color):
        """Crea una tarjeta de estadística individual"""
        card = QFrame()
        card.setObjectName("stat_card")
        card.setMinimumHeight(100)
        card.setMaximumHeight(120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setObjectName("stat_title")
        
        value_label = QLabel(value)
        value_label.setObjectName("stat_value")
        
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        
        # Aplicar estilo dinámico
        card_style = f"""
            #stat_card {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                         stop:0 {color}, stop:1 #1a1a2e);
                border-radius: 12px;
                border: 1px solid #2d3748;
            }}
            #stat_title {{
                color: #e2e8f0;
                font-size: 12px;
                font-weight: bold;
            }}
            #stat_value {{
                color: white;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Courier New';
            }}
        """
        card.setStyleSheet(card_style)
        
        return card
        
    def create_controls(self):
        """Crea los controles de filtro y exportación"""
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Date filters
        date_label = QLabel("📅 Filtrar por fecha:")
        date_label.setStyleSheet("color: #94a3b8; font-weight: bold;")
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        # Filter button
        filter_btn = QPushButton("🔍 Aplicar Filtro")
        filter_btn.setObjectName("filter_btn")
        filter_btn.clicked.connect(self.apply_filters)
        
        # Export buttons
        export_csv_btn = QPushButton("📊 Exportar CSV")
        export_csv_btn.setObjectName("export_btn")
        export_csv_btn.clicked.connect(self.export_csv)
        
        export_excel_btn = QPushButton("📈 Exportar Excel")
        export_excel_btn.setObjectName("export_btn")
        export_excel_btn.clicked.connect(self.export_excel)
        
        controls_layout.addWidget(date_label)
        controls_layout.addWidget(self.start_date)
        controls_layout.addWidget(QLabel("a"))
        controls_layout.addWidget(self.end_date)
        controls_layout.addWidget(filter_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(export_csv_btn)
        controls_layout.addWidget(export_excel_btn)
        
        return controls_layout
        
    def create_table_section(self):
        """Crea la sección de la tabla de asientos"""
        table_section = QFrame()
        table_section.setObjectName("table_section")
        
        layout = QVBoxLayout()
        
        # Table title
        table_title = QLabel("📋 ASIENTOS CONTABLES - LIBRO DIARIO")
        table_title.setObjectName("table_title")
        
        # Table
        self.asientos_table = QTableWidget()
        self.asientos_table.setObjectName("asientos_table")
        self.asientos_table.setAlternatingRowColors(True)
        self.asientos_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(table_title)
        layout.addWidget(self.asientos_table)
        
        table_section.setLayout(layout)
        return table_section
        
    def create_charts_section(self):
        """Crea la sección de gráficos"""
        charts_layout = QHBoxLayout()
        
        # Canvas para gráficos
        self.chart_canvas = FigureCanvas(plt.Figure(figsize=(10, 4)))
        
        charts_layout.addWidget(self.chart_canvas)
        
        return charts_layout
        
    def apply_styles(self):
        """Aplica estilos al dashboard"""
        style = """
            QWidget {
                background-color: #0f172a;
                color: #e2e8f0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            #dashboard_title {
                color: #00E5FF;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
            
            #date_label {
                color: #94a3b8;
                font-size: 12px;
                font-weight: bold;
            }
            
            QPushButton#filter_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #3b82f6, stop:1 #1d4ed8);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            
            QPushButton#filter_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #60a5fa, stop:1 #2563eb);
            }
            
            QPushButton#export_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            
            QPushButton#export_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #34d399, stop:1 #10b981);
            }
            
            #table_section {
                background-color: #1e293b;
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #334155;
            }
            
            #table_title {
                color: #00E5FF;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            
            #asientos_table {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 6px;
                gridline-color: #334155;
            }
            
            #asientos_table::item {
                padding: 8px;
                border-bottom: 1px solid #334155;
            }
            
            #asientos_table::item:selected {
                background-color: #3b82f6;
            }
            
            QHeaderView::section {
                background-color: #334155;
                color: #e2e8f0;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            
            QDateEdit {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 1px solid #475569;
                border-radius: 4px;
                padding: 6px;
            }
        """
        self.setStyleSheet(style)
        
    def load_data(self):
        """Carga los datos iniciales"""
        try:
            # Obtener datos del servicio
            asientos = self.journal_service.obtener_asientos(self.session)
            self.update_stats(asientos)
            self.update_table(asientos)
            
            if PANDAS_AVAILABLE:
                self.update_charts(asientos)
            
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            QMessageBox.warning(self, "Error", f"Error al cargar datos: {str(e)}")
            
    def update_stats(self, asientos):
        """Actualiza las estadísticas"""
        total_asientos = len(asientos)
        total_debe = sum(sum(linea['debe'] for linea in asiento['lineas']) for asiento in asientos)
        total_haber = sum(sum(linea['haber'] for linea in asiento['lineas']) for asiento in asientos)
        balance = total_debe - total_haber
        
        # Actualizar tarjetas
        self.total_transactions_card.findChild(QLabel, "stat_value").setText(str(total_asientos))
        self.total_debit_card.findChild(QLabel, "stat_value").setText(f"{total_debe:,.2f} Bs")
        self.total_credit_card.findChild(QLabel, "stat_value").setText(f"{total_haber:,.2f} Bs")
        self.balance_card.findChild(QLabel, "stat_value").setText(f"{balance:,.2f} Bs")
        
    def update_table(self, asientos):
        """Actualiza la tabla de asientos"""
        headers = ["Número", "Fecha", "Descripción", "Total Débito (Bs)", "Total Crédito (Bs)", "Líneas"]
        self.asientos_table.setColumnCount(len(headers))
        self.asientos_table.setHorizontalHeaderLabels(headers)
        self.asientos_table.setRowCount(len(asientos))
        
        for row, asiento in enumerate(asientos):
            total_debe = sum(linea['debe'] for linea in asiento['lineas'])
            total_haber = sum(linea['haber'] for linea in asiento['lineas'])
            
            self.asientos_table.setItem(row, 0, QTableWidgetItem(asiento['numero']))
            self.asientos_table.setItem(row, 1, QTableWidgetItem(
                asiento['fecha'].strftime('%d/%m/%Y') if hasattr(asiento['fecha'], 'strftime') else str(asiento['fecha'])))
            self.asientos_table.setItem(row, 2, QTableWidgetItem(asiento['descripcion']))
            self.asientos_table.setItem(row, 3, QTableWidgetItem(f"{total_debe:,.2f}"))
            self.asientos_table.setItem(row, 4, QTableWidgetItem(f"{total_haber:,.2f}"))
            self.asientos_table.setItem(row, 5, QTableWidgetItem(str(len(asiento['lineas']))))
                
    def update_charts(self, asientos):
        """Actualiza los gráficos"""
        if not asientos or not PANDAS_AVAILABLE:
            return
            
        try:
            # Crear DataFrame con los datos
            data = []
            for asiento in asientos:
                fecha = asiento['fecha']
                if isinstance(fecha, str):
                    fecha = datetime.strptime(fecha, '%Y-%m-%d')
                
                total_debe = sum(linea['debe'] for linea in asiento['lineas'])
                total_haber = sum(linea['haber'] for linea in asiento['lineas'])
                
                data.append({
                    'fecha': fecha,
                    'debe': total_debe,
                    'haber': total_haber
                })
            
            df = pd.DataFrame(data)
            df['fecha'] = pd.to_datetime(df['fecha'])
            df = df.sort_values('fecha')
            
            # Agrupar por fecha
            daily_totals = df.groupby(df['fecha'].dt.date).agg({
                'debe': 'sum',
                'haber': 'sum'
            }).reset_index()
            
            # Limpiar el gráfico anterior
            self.chart_canvas.figure.clear()
            ax = self.chart_canvas.figure.add_subplot(111)
            
            # Configurar estilo del gráfico
            plt.style.use('dark_background')
            ax.set_facecolor('#1e293b')
            self.chart_canvas.figure.patch.set_facecolor('#0f172a')
            
            # Crear gráfico
            if len(daily_totals) > 0:
                ax.plot(daily_totals['fecha'], daily_totals['debe'], 
                        label='Débito', color='#A23B72', linewidth=2, marker='o')
                ax.plot(daily_totals['fecha'], daily_totals['haber'], 
                        label='Crédito', color='#F18F01', linewidth=2, marker='s')
                
                ax.set_xlabel('Fecha', color='white')
                ax.set_ylabel('Monto (Bs)', color='white')
                ax.set_title('Tendencia de Movimientos Diarios', color='white', pad=20)
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                # Rotar etiquetas de fecha
                plt.setp(ax.get_xticklabels(), rotation=45)
            
            self.chart_canvas.draw()
            
        except Exception as e:
            print(f"❌ Error actualizando gráficos: {e}")
        
    def apply_filters(self):
        """Aplica los filtros de fecha"""
        try:
            start_date = self.start_date.date().toPython()
            end_date = self.end_date.date().toPython()
            
            # Obtener asientos filtrados
            asientos = self.journal_service.obtener_asientos(
                self.session, fecha_inicio=start_date, fecha_fin=end_date)
                
            self.update_stats(asientos)
            self.update_table(asientos)
            
            if PANDAS_AVAILABLE:
                self.update_charts(asientos)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al aplicar filtros: {str(e)}")
            
    def export_csv(self):
        """Exporta los datos a CSV"""
        try:
            if not PANDAS_AVAILABLE:
                QMessageBox.warning(self, "Error", "Pandas no está disponible para exportación CSV")
                return
                
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar CSV", "libro_diario.csv", "CSV Files (*.csv)")
                
            if file_path:
                asientos = self.journal_service.obtener_asientos(self.session)
                
                # Preparar datos para exportación
                data = []
                for asiento in asientos:
                    for linea in asiento['lineas']:
                        data.append({
                            'numero_asiento': asiento['numero'],
                            'fecha': asiento['fecha'],
                            'descripcion_asiento': asiento['descripcion'],
                            'cuenta_codigo': linea['cuenta_codigo'],
                            'cuenta_nombre': linea['cuenta_nombre'],
                            'debe': linea['debe'],
                            'haber': linea['haber'],
                            'descripcion_linea': linea['descripcion']
                        })
                
                df = pd.DataFrame(data)
                df.to_csv(file_path, index=False, encoding='utf-8')
                QMessageBox.information(self, "Éxito", "Datos exportados a CSV correctamente")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al exportar CSV: {str(e)}")
            
    def export_excel(self):
        """Exporta los datos a Excel"""
        try:
            if not PANDAS_AVAILABLE:
                QMessageBox.warning(self, "Error", "Pandas no está disponible para exportación Excel")
                return
                
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Exportar Excel", "libro_diario.xlsx", "Excel Files (*.xlsx)")
                
            if file_path:
                asientos = self.journal_service.obtener_asientos(self.session)
                
                # Preparar datos para exportación
                data = []
                for asiento in asientos:
                    for linea in asiento['lineas']:
                        data.append({
                            'Número Asiento': asiento['numero'],
                            'Fecha': asiento['fecha'],
                            'Descripción Asiento': asiento['descripcion'],
                            'Código Cuenta': linea['cuenta_codigo'],
                            'Nombre Cuenta': linea['cuenta_nombre'],
                            'Débito (Bs)': linea['debe'],
                            'Crédito (Bs)': linea['haber'],
                            'Descripción Línea': linea['descripcion']
                        })
                
                df = pd.DataFrame(data)
                df.to_excel(file_path, index=False, engine='openpyxl')
                QMessageBox.information(self, "Éxito", "Datos exportados a Excel correctamente")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al exportar Excel: {str(e)}")