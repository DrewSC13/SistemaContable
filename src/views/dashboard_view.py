from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QGridLayout, QScrollArea)
from PySide6.QtCore import Qt
from models import Usuario

class DashboardView(QWidget):
    def __init__(self, usuario: Usuario):
        super().__init__()
        self.usuario = usuario
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)
        
        # Título principal
        title = QLabel("DASHBOARD PRINCIPAL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 22px;
            font-weight: 300;
            color: #00E5FF;
            padding: 15px;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Línea decorativa
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background: #00E5FF; height: 1px;")
        line.setFixedHeight(1)
        layout.addWidget(line)
        
        # Scroll area para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(15, 20, 15, 20)
        scroll_layout.setSpacing(20)
        
        # Grid de tarjetas KPI
        kpi_label = QLabel("INDICADORES PRINCIPALES")
        kpi_label.setStyleSheet("font-size: 16px; color: #E6EEF3; font-weight: 600; font-family: 'Segoe UI';")
        scroll_layout.addWidget(kpi_label)
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        # Tarjetas KPI profesionales - TODOS EN 0
        kpis = [
            ("INGRESOS MENSUALES", "Q 0.00", "#00E5FF"),
            ("EGRESOS MENSUALES", "Q 0.00", "#B3009E"), 
            ("SALDO GENERAL", "Q 0.00", "#00FF88"),
            ("CLIENTES ACTIVOS", "0", "#FFAA00"),
            ("PRODUCTOS EN STOCK", "0", "#AA00FF"),
            ("FACTURAS PENDIENTES", "0", "#FF4444")
        ]
        
        for i, (titulo, valor, color) in enumerate(kpis):
            card = self.create_kpi_card(titulo, valor, color)
            row = i // 3
            col = i % 3
            grid_layout.addWidget(card, row, col)
        
        scroll_layout.addLayout(grid_layout)
        
        # Sección de accesos rápidos
        scroll_layout.addSpacing(15)
        quick_access_label = QLabel("ACCESOS RÁPIDOS")
        quick_access_label.setStyleSheet("font-size: 16px; color: #E6EEF3; font-weight: 600; font-family: 'Segoe UI'; margin-top: 15px;")
        scroll_layout.addWidget(quick_access_label)
        
        quick_grid = QGridLayout()
        quick_grid.setSpacing(12)
        quick_actions = [
            ("NUEVO ASIENTO CONTABLE", "Libro Diario General"),
            ("REGISTRAR FACTURA VENTA", "Modulo de Ventas"),
            ("GENERAR REPORTES", "Sistema de Reportes"),
            ("GESTIONAR INVENTARIO", "Control de Stock")
        ]
        
        for i, (accion, desc) in enumerate(quick_actions):
            btn_card = self.create_quick_action_card(accion, desc)
            row = i // 2
            col = i % 2
            quick_grid.addWidget(btn_card, row, col)
        
        scroll_layout.addLayout(quick_grid)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
    
    def create_kpi_card(self, title, value, color):
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(120)
        card.setMinimumWidth(180)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 11px; color: {color}; font-weight: 600; font-family: 'Segoe UI';")
        title_label.setAlignment(Qt.AlignLeft)
        
        # Valor - Todos en 0
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E6EEF3; font-family: 'Segoe UI';")
        value_label.setAlignment(Qt.AlignRight)
        
        # Línea divisoria
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background: {color}; height: 1px;")
        
        layout.addWidget(title_label)
        layout.addWidget(line)
        layout.addWidget(value_label)
        
        return card
    
    def create_quick_action_card(self, action, description):
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(80)
        card.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(6)
        
        action_label = QLabel(action)
        action_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #E6EEF3; font-family: 'Segoe UI';")
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 10px; color: #98A0A6; font-family: 'Segoe UI';")
        
        layout.addWidget(action_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        return card
