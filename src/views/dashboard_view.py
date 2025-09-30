from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QGridLayout, QScrollArea,
                             QSizePolicy, QPushButton)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QFont
from datetime import datetime

class FuturisticDashboardView(QWidget):
    def __init__(self, usuario):
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
        title = QLabel("🏠 PANEL PRINCIPAL - MISKY CHOCLOS")
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
        
        # Sección de bienvenida
        self.setup_welcome_section(scroll_layout)
        
        # Grid principal para todas las métricas
        self.setup_metrics_grid(scroll_layout)
        
        # Sección de acciones rápidas
        self.setup_quick_actions(scroll_layout)
        
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
    
    def setup_welcome_section(self, parent_layout):
        """Configurar sección de bienvenida"""
        welcome_frame = QFrame()
        welcome_frame.setObjectName("welcome_frame")
        welcome_layout = QVBoxLayout(welcome_frame)
        
        welcome_label = QLabel(f"👋 ¡Bienvenido, {self.usuario.username}!")
        welcome_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00E5FF;
            background: transparent;
            margin-bottom: 10px;
        """)
        
        subtitle_label = QLabel("Sistema Contable Misky Choclos - Panel de Control Principal")
        subtitle_label.setStyleSheet("""
            font-size: 16px;
            color: #94A3B8;
            background: transparent;
        """)
        
        date_label = QLabel(f"📅 {datetime.now().strftime('%A, %d de %B de %Y - %H:%M')}")
        date_label.setStyleSheet("""
            font-size: 14px;
            color: #B3009E;
            background: transparent;
            margin-top: 10px;
        """)
        
        welcome_layout.addWidget(welcome_label)
        welcome_layout.addWidget(subtitle_label)
        welcome_layout.addWidget(date_label)
        
        welcome_frame.setStyleSheet("""
            #welcome_frame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 229, 255, 0.1),
                    stop:1 rgba(255, 0, 128, 0.1));
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        parent_layout.addWidget(welcome_frame)
    
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
    
    def setup_quick_actions(self, parent_layout):
        """Configurar sección de acciones rápidas"""
        actions_frame = QFrame()
        actions_frame.setObjectName("actions_frame")
        actions_layout = QVBoxLayout(actions_frame)
        
        title = QLabel("🚀 ACCIONES RÁPIDAS")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00E5FF;
            margin-bottom: 15px;
        """)
        actions_layout.addWidget(title)
        
        # Grid de botones de acción
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Crear los botones sin conectar aún (se conectarán desde main_window)
        self.btn_libro_diario = QPushButton("📖 LIBRO DIARIO")
        self.btn_libro_diario.setToolTip("Ver libro diario completo")
        self.btn_libro_diario.setObjectName("action_btn")
        self.btn_libro_diario.setMinimumHeight(70)
        
        self.btn_nuevo_asiento = QPushButton("➕ NUEVO ASIENTO")
        self.btn_nuevo_asiento.setToolTip("Crear nuevo asiento contable")
        self.btn_nuevo_asiento.setObjectName("action_btn")
        self.btn_nuevo_asiento.setMinimumHeight(70)
        
        # Agregar más botones según necesites...
        
        actions_grid.addWidget(self.btn_libro_diario, 0, 0)
        actions_grid.addWidget(self.btn_nuevo_asiento, 0, 1)
        # ... agregar más botones al grid
        
        actions_layout.addLayout(actions_grid)
        
        actions_frame.setStyleSheet("""
            #actions_frame {
                background: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(0, 229, 255, 0.2);
                border-radius: 12px;
                padding: 20px;
            }
            
            QPushButton#action_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #1d4ed8);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            
            QPushButton#action_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #60a5fa, stop:1 #2563eb);
                border: 1px solid rgba(0, 229, 255, 0.6);
            }
        """)
        
        parent_layout.addWidget(actions_frame)
    
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
    
    # Métodos de navegación (conectados a los botones)
    def ir_libro_diario(self):
        """Navegar al libro diario"""
        # Esta función se conectará con el sistema de navegación principal
        print("🔗 Navegando a Libro Diario...")
    
    def ir_registro_asientos(self):
        """Navegar al registro de asientos"""
        print("🔗 Navegando a Registro de Asientos...")
    
    def ir_reportes(self):
        """Navegar a reportes"""
        print("🔗 Navegando a Reportes...")
    
    def ir_clientes(self):
        """Navegar a clientes"""
        print("🔗 Navegando a Clientes...")
    
    def ir_proveedores(self):
        """Navegar a proveedores"""
        print("🔗 Navegando a Proveedores...")
    
    def ir_configuracion(self):
        """Navegar a configuración"""
        print("🔗 Navegando a Configuración...")

# Para mantener compatibilidad
DashboardView = FuturisticDashboardView