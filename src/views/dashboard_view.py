from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QGridLayout, QScrollArea,
                             QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QFont
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
import math
from models import Usuario

class PieChartWidget(QWidget):
    def __init__(self, title, data, colors, parent=None):
        super().__init__(parent)
        self.title = title
        self.data = data
        self.colors = colors
        self.setMinimumSize(300, 250)
        self.setup_chart()
    
    def setup_chart(self):
        # Crear serie de torta
        series = QPieSeries()
        
        # Agregar datos a la serie
        for i, (label, value) in enumerate(self.data):
            slice = series.append(label, value)
            slice.setColor(QColor(self.colors[i % len(self.colors)]))
            slice.setLabelVisible(True)
            slice.setLabel(f"{label}: Bs {value:,.0f}")
        
        # Configurar el chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(self.title)
        chart.setTitleFont(QFont("Segoe UI", 12, QFont.Bold))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.setBackgroundBrush(QColor(0, 0, 0, 0))  # Fondo transparente
        
        # Chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet("""
            QChartView {
                background: transparent;
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(chart_view)

class BarChartWidget(QWidget):
    def __init__(self, title, data, colors, parent=None):
        super().__init__(parent)
        self.title = title
        self.data = data
        self.colors = colors
        self.setMinimumSize(400, 250)
        self.setup_chart()
    
    def setup_chart(self):
        # Crear series de barras
        series = QBarSeries()
        
        # Crear sets de datos
        for i, (category, values) in enumerate(self.data):
            bar_set = QBarSet(category)
            for value in values:
                bar_set.append(value)
            bar_set.setColor(QColor(self.colors[i % len(self.colors)]))
            series.append(bar_set)
        
        # Configurar el chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(self.title)
        chart.setTitleFont(QFont("Segoe UI", 12, QFont.Bold))
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Configurar ejes
        categories = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText("Bs")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chart.setBackgroundBrush(QColor(0, 0, 0, 0))  # Fondo transparente
        
        # Chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet("""
            QChartView {
                background: transparent;
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(chart_view)

class FuturisticDashboardView(QWidget):
    def __init__(self, usuario: Usuario):
        super().__init__()
        self.usuario = usuario
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        # Layout principal futurista
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)
        
        # Título principal minimalista
        title = QLabel("PANEL PRINCIPAL - MISKY CHOCLOS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 24px;
            font-weight: 300;
            color: #00E5FF;
            padding: 15px;
            margin-bottom: 10px;
            letter-spacing: 2px;
        """)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(title)
        
        # Línea decorativa
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 transparent,
                stop:0.3 #00E5FF,
                stop:0.7 #FF0080,
                stop:1 transparent);
            height: 1px;
            margin: 0 50px;
        """)
        line.setFixedHeight(1)
        main_layout.addWidget(line)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(43, 47, 54, 0.3);
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #FF0080);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00F7FF, stop:1 #FF1A99);
            }
        """)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 20, 10, 20)
        scroll_layout.setSpacing(25)
        
        # Grid principal para todas las métricas
        self.setup_metrics_grid(scroll_layout)
        
        # Sección de gráficos
        self.setup_charts_section(scroll_layout)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def setup_metrics_grid(self, parent_layout):
        """Configurar grid con todas las métricas del sistema"""
        
        # Grid principal 4x3 para métricas
        main_grid = QGridLayout()
        main_grid.setSpacing(15)
        main_grid.setContentsMargins(0, 0, 0, 0)
        
        # Definir todas las métricas del sistema con estilo Windows 8 futurista
        metrics = [
            # Fila 1 - Métricas Financieras Principales
            {
                "title": "INGRESOS TOTALES", 
                "value": "Bs 125,430", 
                "color": "#00E5FF",
                "icon": "💰",
                "description": "Ingresos acumulados del mes"
            },
            {
                "title": "EGRESOS TOTALES", 
                "value": "Bs 89,210", 
                "color": "#FF4444",
                "icon": "📊",
                "description": "Egresos acumulados del mes"
            },
            {
                "title": "UTILIDAD NETA", 
                "value": "Bs 36,220", 
                "color": "#00FF88",
                "icon": "⚡",
                "description": "Utilidad del período"
            },
            {
                "title": "FLUJO DE CAJA", 
                "value": "Bs 42,150", 
                "color": "#0078D7",
                "icon": "💳",
                "description": "Disponibilidad actual"
            },
            
            # Fila 2 - Métricas de Operaciones
            {
                "title": "VENTAS DEL MES", 
                "value": "Bs 98,750", 
                "color": "#B3009E",
                "icon": "🛒",
                "description": "Total ventas mensuales"
            },
            {
                "title": "COMPRAS DEL MES", 
                "value": "Bs 45,680", 
                "color": "#FFAA00",
                "icon": "📦",
                "description": "Total compras mensuales"
            },
            {
                "title": "MARGEN BRUTO", 
                "value": "42%", 
                "color": "#AA00FF",
                "icon": "📈",
                "description": "Margen de utilidad bruta"
            },
            {
                "title": "ROTACIÓN INVENTARIO", 
                "value": "2.8x", 
                "color": "#FF0080",
                "icon": "🔄",
                "description": "Veces rotación mensual"
            },
            
            # Fila 3 - Métricas de Clientes y Deudas
            {
                "title": "CLIENTES ACTIVOS", 
                "value": "156", 
                "color": "#00BCF2",
                "icon": "👥",
                "description": "Clientes con movimiento"
            },
            {
                "title": "CUENTAS POR COBRAR", 
                "value": "Bs 23,450", 
                "color": "#FF6B6B",
                "icon": "📋",
                "description": "Total por cobrar"
            },
            {
                "title": "CUENTAS POR PAGAR", 
                "value": "Bs 18,790", 
                "color": "#FF8C00",
                "icon": "🏢",
                "description": "Total por pagar"
            },
            {
                "title": "PROVEEDORES ACTIVOS", 
                "value": "28", 
                "color": "#8E44AD",
                "icon": "🤝",
                "description": "Proveedores con movimiento"
            }
        ]
        
        # Crear y colocar las métricas en el grid 4x3
        for i, metric in enumerate(metrics):
            card = self.create_windows8_metric_card(
                metric["title"], 
                metric["value"], 
                metric["color"],
                metric["icon"],
                metric["description"]
            )
            row = i // 4  # 4 columnas por fila
            col = i % 4   # 4 columnas
            main_grid.addWidget(card, row, col)
        
        parent_layout.addLayout(main_grid)
    
    def setup_charts_section(self, parent_layout):
        """Configurar sección de gráficos"""
        
        # Título de la sección de gráficos
        charts_title = QLabel("ANÁLISIS VISUAL - DATOS FINANCIEROS")
        charts_title.setStyleSheet("""
            font-size: 18px; 
            color: #00E5FF; 
            font-weight: 600; 
            font-family: 'Segoe UI';
            margin-top: 30px;
            margin-bottom: 15px;
            letter-spacing: 1px;
        """)
        charts_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        parent_layout.addWidget(charts_title)
        
        # Contenedor principal para gráficos
        charts_container = QFrame()
        charts_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 229, 255, 0.05),
                    stop:1 rgba(255, 0, 128, 0.05));
                border: 1px solid rgba(0, 229, 255, 0.2);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        charts_layout = QVBoxLayout(charts_container)
        charts_layout.setSpacing(20)
        
        # Fila 1: Gráficos de torta
        pie_charts_layout = QHBoxLayout()
        pie_charts_layout.setSpacing(20)
        
        # Gráfico de torta 1 - Distribución de Ingresos
        income_data = [
            ("Ventas", 65000),
            ("Servicios", 32000),
            ("Inversiones", 15430),
            ("Otros", 13000)
        ]
        income_colors = ["#00E5FF", "#B3009E", "#00FF88", "#FFAA00"]
        pie_chart1 = PieChartWidget("DISTRIBUCIÓN DE INGRESOS", income_data, income_colors)
        pie_charts_layout.addWidget(pie_chart1)
        
        # Gráfico de torta 2 - Distribución de Egresos
        expenses_data = [
            ("Compras", 35680),
            ("Gastos Operativos", 21890),
            ("Sueldos", 18750),
            ("Impuestos", 12890)
        ]
        expenses_colors = ["#FF4444", "#FF8C00", "#FF0080", "#AA00FF"]
        pie_chart2 = PieChartWidget("DISTRIBUCIÓN DE EGRESOS", expenses_data, expenses_colors)
        pie_charts_layout.addWidget(pie_chart2)
        
        charts_layout.addLayout(pie_charts_layout)
        
        # Fila 2: Gráficos de barras
        bar_charts_layout = QHBoxLayout()
        bar_charts_layout.setSpacing(20)
        
        # Gráfico de barras 1 - Ventas vs Compras (6 meses)
        sales_vs_purchases_data = [
            ("Ventas", [45000, 52000, 48000, 61000, 58750, 65750]),
            ("Compras", [32000, 38000, 29500, 42800, 38680, 45680])
        ]
        bar_colors1 = ["#00E5FF", "#B3009E"]
        bar_chart1 = BarChartWidget("VENTAS VS COMPRAS - ÚLTIMOS 6 MESES", sales_vs_purchases_data, bar_colors1)
        bar_charts_layout.addWidget(bar_chart1)
        
        # Gráfico de barras 2 - Flujo de Caja Mensual
        cash_flow_data = [
            ("Ingresos", [42000, 48000, 52000, 45000, 55430, 65430]),
            ("Egresos", [38000, 42000, 45000, 39210, 48210, 58210]),
            ("Utilidad", [4000, 6000, 7000, 5790, 7220, 7220])
        ]
        bar_colors2 = ["#00FF88", "#FF4444", "#0078D7"]
        bar_chart2 = BarChartWidget("FLUJO DE CAJA MENSUAL", cash_flow_data, bar_colors2)
        bar_charts_layout.addWidget(bar_chart2)
        
        charts_layout.addLayout(bar_charts_layout)
        
        parent_layout.addWidget(charts_container)
        parent_layout.addStretch()
    
    def create_windows8_metric_card(self, title, value, color, icon, description):
        """Crear tarjeta de métrica estilo Windows 8 futurista"""
        card = QFrame()
        card.setObjectName("metric-card")
        card.setMinimumSize(220, 120)
        card.setMaximumSize(280, 140)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Estilo Windows 8 con toque futurista
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color},
                    stop:0.7 {self.darken_color(color, 20)},
                    stop:1 {color});
                border-radius: 8px;
                border: 2px solid {self.lighten_color(color, 30)};
            }}
            QFrame:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.lighten_color(color, 10)},
                    stop:0.7 {color},
                    stop:1 {self.lighten_color(color, 10)});
                border: 2px solid {self.lighten_color(color, 50)};
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)
        
        # Header con icono y título
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            font-size: 20px;
            background: transparent;
            color: white;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 12px;
            font-weight: 600;
            color: white;
            background: transparent;
            font-family: 'Segoe UI';
        """)
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Línea divisoria
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("""
            background: rgba(255, 255, 255, 0.5);
            border-radius: 0.5px;
        """)
        
        # Valor principal (más destacado)
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: white;
            background: transparent;
            font-family: 'Segoe UI';
        """)
        value_label.setAlignment(Qt.AlignCenter)
        
        # Descripción pequeña
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            font-size: 9px;
            color: rgba(255, 255, 255, 0.8);
            background: transparent;
            font-family: 'Segoe UI';
        """)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        
        layout.addLayout(header_layout)
        layout.addWidget(line)
        layout.addWidget(value_label)
        layout.addWidget(desc_label)
        
        return card
    
    def darken_color(self, hex_color, percent):
        """Oscurecer un color hex"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = max(0, min(255, r - (r * percent // 100)))
        g = max(0, min(255, g - (g * percent // 100)))
        b = max(0, min(255, b - (b * percent // 100)))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def lighten_color(self, hex_color, percent):
        """Aclarar un color hex"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = min(255, r + (255 - r) * percent // 100)
        g = min(255, g + (255 - g) * percent // 100)
        b = min(255, b + (255 - b) * percent // 100)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def setup_animations(self):
        """Configurar animaciones sutiles"""
        # Timer para efectos de actualización en tiempo real
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.simulate_data_update)
        self.update_timer.start(5000)  # Actualizar cada 5 segundos
    
    def simulate_data_update(self):
        """Simular actualización de datos en tiempo real"""
        # En una implementación real, aquí se conectaría con la base de datos
        # Por ahora es solo una simulación visual
        pass

# Para mantener compatibilidad
DashboardView = FuturisticDashboardView