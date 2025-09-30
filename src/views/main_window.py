from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QStackedWidget,
                             QFrame, QToolBar, QStatusBar, QMessageBox, QSizePolicy,
                             QScrollArea, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PySide6.QtGui import QFontDatabase, QIcon, QPainter, QLinearGradient, QColor, QPalette, QFont
import os

class FuturisticSidebarHeader(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar-header")
        self.setMinimumHeight(120)
        self.setMaximumHeight(160)
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(8)
        
        # Logo con efecto futurista
        self.logo_container = QFrame()
        self.logo_container.setFixedSize(70, 70)
        self.logo_container.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #00E5FF, stop:0.3 #B3009E, stop:0.7 #FF0080, stop:1 #00E5FF);
            border-radius: 35px;
            border: 2px solid #00E5FF;
        """)
        
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setAlignment(Qt.AlignCenter)
        
        self.logo_label = QLabel("MC")
        self.logo_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF;
            background: transparent;
        """)
        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.logo_label)
        
        # Título principal con efecto neón
        self.title_label = QLabel("MISKY CHOCLOS")
        self.title_label.setObjectName("sidebar-title")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                background: transparent;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                font-weight: 800;
                color: #00E5FF;
                letter-spacing: 2px;
            }
        """)
        
        # Subtítulo futurista
        self.subtitle_label = QLabel("CONTABILITY SYSTEM")
        self.subtitle_label.setObjectName("sidebar-subtitle")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            QLabel {
                background: transparent;
                font-family: 'Segoe UI', sans-serif;
                font-size: 10px;
                font-weight: 300;
                color: #B3009E;
                letter-spacing: 3px;
                text-transform: uppercase;
            }
        """)
        
        # Línea de efecto futurista
        self.glow_line = QFrame()
        self.glow_line.setFixedHeight(2)
        self.glow_line.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 transparent,
                stop:0.3 #00E5FF,
                stop:0.7 #FF0080,
                stop:1 transparent);
            border-radius: 1px;
        """)
        
        layout.addWidget(self.logo_container, 0, Qt.AlignCenter)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.glow_line)
    
    def setup_animations(self):
        # Animación del logo
        self.logo_animation = QPropertyAnimation(self.logo_container, b"styleSheet")
        self.logo_animation.setDuration(3000)
        self.logo_animation.setLoopCount(-1)
        self.logo_animation.setStartValue("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #00E5FF, stop:0.3 #B3009E, stop:0.7 #FF0080, stop:1 #00E5FF);
            border-radius: 35px;
            border: 2px solid #00E5FF;
        """)
        self.logo_animation.setEndValue("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #FF0080, stop:0.3 #00E5FF, stop:0.7 #B3009E, stop:1 #FF0080);
            border-radius: 35px;
            border: 2px solid #FF0080;
        """)
        
        # Animación de la línea
        self.line_animation = QPropertyAnimation(self.glow_line, b"maximumWidth")
        self.line_animation.setDuration(2000)
        self.line_animation.setLoopCount(-1)
        self.line_animation.setStartValue(50)
        self.line_animation.setEndValue(200)
        self.line_animation.setEasingCurve(QEasingCurve.InOutSine)
        
        self.logo_animation.start()
        self.line_animation.start()
    
    def update_responsive_layout(self, width):
        if width < 200:
            self.title_label.setText("MISKY")
            self.subtitle_label.setText("CONTABILITY")
            self.logo_container.setFixedSize(50, 50)
            self.logo_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        else:
            self.title_label.setText("MISKY CHOCLOS")
            self.subtitle_label.setText("CONTABILITY SYSTEM")
            self.logo_container.setFixedSize(70, 70)
            self.logo_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")

class FuturisticMenuButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setObjectName("menu-button")
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(60)
        
        self.full_text = text
        self.short_text = self.get_short_text(text)
        
        # Efecto de opacidad
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 15, 20, 15)
        self.layout.setSpacing(15)
        
        # Indicador de activo futurista
        self.active_indicator = QFrame()
        self.active_indicator.setFixedWidth(4)
        self.active_indicator.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #00E5FF, stop:0.5 #FF0080, stop:1 #00E5FF);
            border-radius: 2px;
        """)
        self.active_indicator.hide()
        
        # Texto grande y legible
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("""
            background: transparent; 
            color: inherit; 
            font-size: 14px;
            font-weight: 500;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: 0.5px;
        """)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.layout.addWidget(self.active_indicator)
        self.layout.addWidget(self.text_label)
        self.layout.addStretch()
        
        self.setup_animations()
        
        # Estilo inicial
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 0px;
                color: #98A0A6;
                text-align: left;
            }
        """)
    
    def setup_animations(self):
        # Animación de hover
        self.hover_animation = QPropertyAnimation(self, b"styleSheet")
        self.hover_animation.setDuration(300)
        
        # Animación del indicador
        self.indicator_animation = QPropertyAnimation(self.active_indicator, b"maximumHeight")
        self.indicator_animation.setDuration(400)
        self.indicator_animation.setEasingCurve(QEasingCurve.OutBack)
    
    def enterEvent(self, event):
        self.hover_animation.setStartValue(self.styleSheet())
        self.hover_animation.setEndValue("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 229, 255, 0.15),
                    stop:1 rgba(255, 0, 128, 0.1));
                border: none;
                border-radius: 0px;
                color: #00E5FF;
                text-align: left;
                border-left: 3px solid #00E5FF;
            }
        """)
        self.hover_animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        if not self.isChecked():
            self.hover_animation.setStartValue(self.styleSheet())
            self.hover_animation.setEndValue("""
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 0px;
                    color: #98A0A6;
                    text-align: left;
                    border-left: 0px solid transparent;
                }
            """)
            self.hover_animation.start()
        super().leaveEvent(event)
    
    def setChecked(self, checked):
        super().setChecked(checked)
        if checked:
            self.active_indicator.show()
            self.indicator_animation.setStartValue(0)
            self.indicator_animation.setEndValue(35)
            self.indicator_animation.start()
            
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(0, 229, 255, 0.2),
                        stop:1 rgba(255, 0, 128, 0.15));
                    border: none;
                    border-radius: 0px;
                    color: #00E5FF;
                    text-align: left;
                    border-left: 3px solid #00E5FF;
                    font-weight: 600;
                }
            """)
        else:
            self.active_indicator.hide()
            self.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 0px;
                    color: #98A0A6;
                    text-align: left;
                    border-left: 0px solid transparent;
                }
            """)
    
    def get_short_text(self, text):
        short_versions = {
            "Dashboard": "Inicio",
            "Libro Diario": "Diario",
            "Libro Mayor": "Mayor",
            "Balances": "Balances",
            "Ventas": "Ventas",
            "Compras": "Compras",
            "Tesorería": "Tesorería",
            "Inventarios": "Inventarios",
            "Clientes": "Clientes",
            "Proveedores": "Proveedores", 
            "Reportes": "Reportes",
            "Configuración": "Configuración"
        }
        return short_versions.get(text, text[:8])
    
    def update_responsive_layout(self, width):
        if width < 180:
            self.text_label.setText(self.short_text)
            self.layout.setContentsMargins(15, 12, 15, 12)
            self.text_label.setStyleSheet("font-size: 12px; font-weight: 500; color: inherit;")
        else:
            self.text_label.setText(self.full_text)
            self.layout.setContentsMargins(20, 15, 20, 15)
            self.text_label.setStyleSheet("font-size: 14px; font-weight: 500; color: inherit;")

class FuturisticUserSection(QFrame):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setObjectName("user-section")
        self.setMinimumHeight(80)
        self.setMaximumHeight(100)
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 12, 15, 12)
        self.layout.setSpacing(12)
        
        # Avatar futurista
        self.avatar_container = QFrame()
        self.avatar_container.setObjectName("user-avatar")
        self.avatar_container.setFixedSize(50, 50)
        self.avatar_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00E5FF, stop:0.5 #B3009E, stop:1 #FF0080);
                border-radius: 25px;
                border: 2px solid #00E5FF;
            }
        """)
        
        avatar_layout = QVBoxLayout(self.avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        
        self.avatar_text = QLabel("MC")
        self.avatar_text.setAlignment(Qt.AlignCenter)
        self.avatar_text.setStyleSheet("""
            color: #FFFFFF; 
            font-weight: bold; 
            font-size: 14px;
            background: transparent;
        """)
        avatar_layout.addWidget(self.avatar_text)
        
        # Información de usuario
        self.user_info = QFrame()
        self.user_info.setObjectName("user-info")
        self.user_layout = QVBoxLayout(self.user_info)
        self.user_layout.setContentsMargins(0, 0, 0, 0)
        self.user_layout.setSpacing(4)
        
        self.name_label = QLabel(self.usuario.username.upper())
        self.name_label.setObjectName("user-name")
        self.name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.name_label.setStyleSheet("""
            color: #00E5FF;
            font-size: 13px;
            font-weight: 600;
            background: transparent;
            letter-spacing: 0.5px;
        """)
        
        self.role_label = QLabel("SENIOR CONTADOR")
        self.role_label.setObjectName("user-role")
        self.role_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.role_label.setStyleSheet("""
            color: #B3009E;
            font-size: 10px;
            font-weight: 400;
            background: transparent;
            letter-spacing: 1px;
        """)
        
        self.user_layout.addWidget(self.name_label)
        self.user_layout.addWidget(self.role_label)
        
        self.layout.addWidget(self.avatar_container)
        self.layout.addWidget(self.user_info)
        self.layout.addStretch()
    
    def setup_animations(self):
        # Animación del avatar
        self.avatar_animation = QPropertyAnimation(self.avatar_container, b"styleSheet")
        self.avatar_animation.setDuration(4000)
        self.avatar_animation.setLoopCount(-1)
        self.avatar_animation.setStartValue("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00E5FF, stop:0.5 #B3009E, stop:1 #FF0080);
                border-radius: 25px;
                border: 2px solid #00E5FF;
            }
        """)
        self.avatar_animation.setEndValue("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FF0080, stop:0.5 #00E5FF, stop:1 #B3009E);
                border-radius: 25px;
                border: 2px solid #FF0080;
            }
        """)
        self.avatar_animation.start()
    
    def update_responsive_layout(self, width):
        if width < 200:
            self.user_info.hide()
            self.avatar_container.setFixedSize(40, 40)
            self.avatar_text.setStyleSheet("font-size: 12px;")
        else:
            self.user_info.show()
            self.avatar_container.setFixedSize(50, 50)
            self.avatar_text.setStyleSheet("font-size: 14px;")

class MainWindow(QMainWindow):
    logout_requested = Signal()
    
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"Misky Choclos Contability | {usuario.username}")
        
        # Configuración de ventana
        self.setMinimumSize(1000, 700)
        self.resize(1400, 900)
        
        # Variables para modo responsive
        self.sidebar_collapsed = False
        self.last_sidebar_width = 300
        
        self.load_fonts()
        self.apply_style()
        self.setup_ui()
        self.setup_responsive_behavior()
        
        print(f"✅ MainWindow creada para usuario: {usuario.username}")
        
    def load_fonts(self):
        font_dir = "src/assets/fonts/"
        if os.path.exists(font_dir):
            for font_file in os.listdir(font_dir):
                if font_file.endswith(('.ttf', '.otf')):
                    QFontDatabase.addApplicationFont(os.path.join(font_dir, font_file))
    
    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0A0E17, stop:0.5 #13182B, stop:1 #0A0E17);
            }
            
            QFrame#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(16, 20, 35, 0.95),
                    stop:1 rgba(25, 30, 45, 0.9));
                border: none;
                border-right: 1px solid rgba(0, 229, 255, 0.2);
            }
            
            QFrame#menu-container {
                background: transparent;
                border: none;
            }
            
            QFrame#menu-group {
                background: transparent;
                border: none;
                margin-bottom: 10px;
            }
            
            QLabel#menu-group-title {
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                color: rgba(0, 229, 255, 0.7);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 2px;
                padding: 15px 20px 8px 20px;
                background: transparent;
                border-bottom: 1px solid rgba(0, 229, 255, 0.2);
                margin-bottom: 5px;
                text-align: left;
            }
            
            QPushButton#logout-button {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 0, 128, 0.3),
                    stop:1 rgba(0, 229, 255, 0.3));
                border: 1px solid rgba(255, 0, 128, 0.4);
                border-radius: 8px;
                padding: 12px;
                margin: 15px 15px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                font-weight: 500;
                text-align: center;
                font-family: 'Segoe UI', sans-serif;
                min-height: 45px;
            }
            
            QPushButton#logout-button:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 0, 128, 0.5),
                    stop:1 rgba(0, 229, 255, 0.5));
                border: 1px solid rgba(255, 0, 128, 0.6);
                font-weight: 600;
            }
        """)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.setup_sidebar()
        self.setup_content_area()
        self.setup_header()
        self.setup_statusbar()
    
    def setup_sidebar(self):
        # Scroll area para el sidebar
        self.sidebar_scroll = QScrollArea()
        self.sidebar_scroll.setWidgetResizable(True)
        self.sidebar_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sidebar_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.sidebar_scroll.setStyleSheet("""
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
        
        # Widget del sidebar
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setObjectName("sidebar")
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        
        # Header futurista
        self.sidebar_header = FuturisticSidebarHeader()
        self.sidebar_layout.addWidget(self.sidebar_header)
        
        # Área de scroll para el menú
        self.menu_scroll = QScrollArea()
        self.menu_scroll.setWidgetResizable(True)
        self.menu_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.menu_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.menu_scroll.setStyleSheet("border: none; background: transparent;")
        
        self.menu_container = QFrame()
        self.menu_container.setObjectName("menu-container")
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(0, 15, 0, 15)
        self.menu_layout.setSpacing(0)
        
        self.setup_menu_buttons()
        self.menu_layout.addStretch()
        
        # User section futurista
        self.user_section = FuturisticUserSection(self.usuario)
        self.menu_layout.addWidget(self.user_section)
        
        # Botón de logout futurista
        self.logout_btn = QPushButton("CERRAR SESIÓN")
        self.logout_btn.setObjectName("logout-button")
        self.logout_btn.clicked.connect(self.cerrar_sesion)
        self.logout_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.logout_btn.setMinimumHeight(50)
        self.menu_layout.addWidget(self.logout_btn)
        
        self.menu_scroll.setWidget(self.menu_container)
        self.sidebar_layout.addWidget(self.menu_scroll)
        
        self.sidebar_scroll.setWidget(self.sidebar_widget)
        
        # Configuración inicial del sidebar
        self.set_sidebar_width(300)
        self.main_layout.addWidget(self.sidebar_scroll)
    
    def setup_menu_buttons(self):
        self.menu_buttons = []
        
        # Grupo 1: CONTABILIDAD
        core_group = self.create_menu_group("CONTABILIDAD")
        core_buttons = [
            "Dashboard",
            "Libro Diario", 
            "Libro Mayor",
            "Balances"
        ]
        
        for text in core_buttons:
            btn = FuturisticMenuButton(text)
            btn.clicked.connect(lambda checked, idx=len(self.menu_buttons): self.cambiar_modulo(idx))
            core_group.layout().addWidget(btn)
            self.menu_buttons.append(btn)
        
        self.menu_layout.addWidget(core_group)
        
        # Grupo 2: OPERACIONES
        ops_group = self.create_menu_group("OPERACIONES")
        ops_buttons = [
            "Ventas",
            "Compras",
            "Tesorería",
            "Inventarios"
        ]
        
        for text in ops_buttons:
            btn = FuturisticMenuButton(text)
            btn.clicked.connect(lambda checked, idx=len(self.menu_buttons): self.cambiar_modulo(idx))
            ops_group.layout().addWidget(btn)
            self.menu_buttons.append(btn)
        
        self.menu_layout.addWidget(ops_group)
        
        # Grupo 3: ADMINISTRACIÓN
        admin_group = self.create_menu_group("ADMINISTRACIÓN")
        admin_buttons = [
            "Clientes",
            "Proveedores", 
            "Reportes",
            "Configuración"
        ]
        
        for text in admin_buttons:
            btn = FuturisticMenuButton(text)
            btn.clicked.connect(lambda checked, idx=len(self.menu_buttons): self.cambiar_modulo(idx))
            admin_group.layout().addWidget(btn)
            self.menu_buttons.append(btn)
        
        self.menu_layout.addWidget(admin_group)
        
        if self.menu_buttons:
            self.menu_buttons[0].setChecked(True)
    
    def create_menu_group(self, title):
        group = QFrame()
        group.setObjectName("menu-group")
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        title_label = QLabel(title)
        title_label.setObjectName("menu-group-title")
        title_label.setFixedHeight(35)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(title_label)
        
        return group
    
    def setup_content_area(self):
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0A0E17, stop:0.5 #13182B, stop:1 #0A0E17);
                border: none;
            }
        """)
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.stacked_widget)
        
        # Añadir vistas
        self.load_views()
        
        self.main_layout.addWidget(self.content_frame)
    
    def load_views(self):
        """Cargar vistas con manejo de errores"""
        print("🔄 Cargando vistas...")
        
        try:
            # Dashboard principal futurista (Index 0)
            from src.views.dashboard_view import DashboardView
            dashboard = DashboardView(self.usuario)
            self.stacked_widget.addWidget(dashboard)
            print("✅ DashboardView cargada correctamente en índice 0")
        except Exception as e:
            print(f"❌ Error cargando DashboardView: {e}")
            self.stacked_widget.addWidget(self.create_placeholder_view("Dashboard Principal", e))
        
        try:
            # Vista completa del libro diario (Index 1)
            from src.views.libro_diario_view import LibroDiarioView
            libro_diario = LibroDiarioView(self.usuario)
            self.stacked_widget.addWidget(libro_diario)
            print("✅ LibroDiarioView cargada correctamente en índice 1")
        except Exception as e:
            print(f"❌ Error cargando LibroDiarioView: {e}")
            self.stacked_widget.addWidget(self.create_placeholder_view("Libro Diario", e))
        
        try:
            # Vista de registro de asientos (Index 2)
            from src.views.journal_view import JournalView
            journal = JournalView(self.usuario)
            self.stacked_widget.addWidget(journal)
            print("✅ JournalView cargada correctamente en índice 2")
        except Exception as e:
            print(f"❌ Error cargando JournalView: {e}")
            self.stacked_widget.addWidget(self.create_placeholder_view("Registro Asientos", e))
        
        # SOLO PLACEHOLDERS para módulos futuros (Index 3 en adelante)
        # No debería haber importaciones de módulos reales aquí
        modulo_placeholders = [
            ("Libro Mayor", "📚 Módulo en desarrollo - Próximamente"),
            ("Balances", "⚖️ Módulo en desarrollo - Próximamente"), 
            ("Ventas", "🛒 Módulo en desarrollo - Próximamente"),
            ("Compras", "📦 Módulo en desarrollo - Próximamente"),
            ("Tesorería", "💼 Módulo en desarrollo - Próximamente"),
            ("Inventarios", "📋 Módulo en desarrollo - Próximamente"),
            ("Clientes", "👥 Módulo en desarrollo - Próximamente"),
            ("Proveedores", "🤝 Módulo en desarrollo - Próximamente"),
            ("Reportes", "📊 Módulo en desarrollo - Próximamente"),
            ("Configuración", "⚙️ Módulo en desarrollo - Próximamente")
        ]
        
        for i, (modulo, mensaje) in enumerate(modulo_placeholders):
            placeholder = self.create_placeholder_view(modulo, mensaje)
            self.stacked_widget.addWidget(placeholder)
            print(f"✅ Placeholder para {modulo} creado en índice {i+3}")
        
        print(f"🎯 Total de vistas cargadas: {self.stacked_widget.count()}")
        
    def create_placeholder_view(self, title, message=None):
        """Crea una vista placeholder para módulos en desarrollo"""
        if message is None:
            message = f"Módulo {title} - En desarrollo"
        
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.setAlignment(Qt.AlignCenter)
        
        # Icono de construcción
        icon_label = QLabel("🚧")
        icon_label.setStyleSheet("""
            font-size: 80px;
            margin-bottom: 20px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Título del módulo
        title_label = QLabel(title.upper())
        title_label.setStyleSheet("""
            font-size: 32px;
            color: #00E5FF;
            font-weight: bold;
            margin-bottom: 15px;
            font-family: 'Segoe UI', sans-serif;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Mensaje de desarrollo
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            font-size: 16px;
            color: #94A3B8;
            margin-bottom: 30px;
            font-family: 'Segoe UI', sans-serif;
        """)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        
        # Información adicional
        info_label = QLabel("Este módulo estará disponible en futuras actualizaciones")
        info_label.setStyleSheet("""
            font-size: 14px;
            color: #B3009E;
            font-style: italic;
            margin-bottom: 40px;
        """)
        info_label.setAlignment(Qt.AlignCenter)
        
        # Botón para volver al dashboard
        back_btn = QPushButton("⬅️ VOLVER AL DASHBOARD")
        back_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00E5FF, stop:1 #B3009E);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00F7FF, stop:1 #FF0080);
            }
        """)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(message_label)
        layout.addWidget(info_label)
        layout.addWidget(back_btn)
        
        # Fondo minimalista
        placeholder.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0A0E17, stop:0.5 #13182B, stop:1 #0A0E17);
            }
        """)
        
        return placeholder
    
    def setup_header(self):
        self.toolbar = QToolBar()
        self.toolbar.setObjectName("header")
        self.toolbar.setFixedHeight(55)
        self.toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addToolBar(self.toolbar)
        
        # Botón para toggle sidebar futurista
        self.toggle_sidebar_btn = QPushButton("≡")
        self.toggle_sidebar_btn.setToolTip("Alternar menú lateral")
        self.toggle_sidebar_btn.setFixedSize(40, 40)
        self.toggle_sidebar_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 229, 255, 0.2),
                    stop:1 rgba(255, 0, 128, 0.2));
                border: 1px solid rgba(0, 229, 255, 0.4);
                border-radius: 6px;
                color: #00E5FF;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 229, 255, 0.3),
                    stop:1 rgba(255, 0, 128, 0.3));
                border: 1px solid rgba(0, 229, 255, 0.6);
            }
        """)
        self.toggle_sidebar_btn.clicked.connect(self.toggle_sidebar)
        self.toolbar.addWidget(self.toggle_sidebar_btn)
        
        self.context_label = QLabel("MISKY CHOCLOS - SISTEMA CONTABLE AVANZADO")
        self.context_label.setStyleSheet("""
            color: #00E5FF; 
            padding: 8px; 
            font-size: 16px; 
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: 0.5px;
        """)
        self.context_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toolbar.addWidget(self.context_label)
    
    def setup_statusbar(self):
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(0, 229, 255, 0.1),
                stop:1 rgba(255, 0, 128, 0.1));
            color: #00E5FF; 
            border-top: 1px solid rgba(0, 229, 255, 0.3);
            padding: 8px;
            font-family: 'Segoe UI', sans-serif;
            font-size: 11px;
            font-weight: 400;
        """)
        self.status_bar.showMessage(f"Misky Choclos Contability v3.0 | Usuario: {self.usuario.username} | Sistema operativo")
        self.setStatusBar(self.status_bar)
    
    def setup_responsive_behavior(self):
        """Configurar comportamiento responsive"""
        # Timer para actualizaciones responsive
        self.responsive_timer = QTimer()
        self.responsive_timer.setSingleShot(True)
        self.responsive_timer.timeout.connect(self.update_responsive_layout)
        
        # Animación para sidebar
        self.sidebar_animation = QPropertyAnimation(self.sidebar_scroll, b"minimumWidth")
        self.sidebar_animation.setDuration(400)
        self.sidebar_animation.setEasingCurve(QEasingCurve.InOutQuart)
    
    def set_sidebar_width(self, width):
        """Establecer ancho del sidebar"""
        self.sidebar_scroll.setMinimumWidth(width)
        self.sidebar_scroll.setMaximumWidth(width)
        self.update_responsive_layout()
    
    def toggle_sidebar(self):
        """Alternar visibilidad del sidebar"""
        if self.sidebar_collapsed:
            # Expandir
            self.sidebar_animation.setStartValue(80)
            self.sidebar_animation.setEndValue(self.last_sidebar_width)
            self.sidebar_collapsed = False
            self.toggle_sidebar_btn.setText("≡")
        else:
            # Colapsar
            self.last_sidebar_width = self.sidebar_scroll.width()
            self.sidebar_animation.setStartValue(self.last_sidebar_width)
            self.sidebar_animation.setEndValue(80)
            self.sidebar_collapsed = True
            self.toggle_sidebar_btn.setText("≡")
        
        self.sidebar_animation.start()
    
    def update_responsive_layout(self):
        """Actualizar layout según el tamaño de la ventana"""
        current_width = self.sidebar_scroll.width()
        
        # Actualizar componentes del sidebar
        self.sidebar_header.update_responsive_layout(current_width)
        self.user_section.update_responsive_layout(current_width)
        
        for button in self.menu_buttons:
            button.update_responsive_layout(current_width)
        
        # Actualizar botón de logout
        if current_width < 200:
            self.logout_btn.setText("SALIR")
        else:
            self.logout_btn.setText("CERRAR SESIÓN")
    
    def resizeEvent(self, event):
        """Manejar redimensionamiento de la ventana"""
        super().resizeEvent(event)
        
        # Programar actualización responsive
        self.responsive_timer.start(100)
        
        # Ajustar sidebar automáticamente en pantallas pequeñas
        window_width = self.width()
        if window_width < 1100 and not self.sidebar_collapsed:
            self.toggle_sidebar()
        elif window_width >= 1100 and self.sidebar_collapsed:
            self.toggle_sidebar()
    
    def cambiar_modulo(self, index):
        """Cambiar módulo actual"""
        for btn in self.menu_buttons:
            btn.setChecked(False)
        
        if 0 <= index < len(self.menu_buttons):
            self.menu_buttons[index].setChecked(True)
        
        if index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(index)
            
            # Actualizar título en toolbar
            modulo_nombre = self.menu_buttons[index].full_text
            self.context_label.setText(f"MISKY CHOCLOS - {modulo_nombre.upper()}")
            
            # Conectar los botones de acción del dashboard cuando esté activo
            if index == 0:  # Dashboard principal
                try:
                    dashboard = self.stacked_widget.widget(0)
                    # Conectar los botones de acción del dashboard a la navegación
                    if hasattr(dashboard, 'ir_libro_diario'):
                        # Reconectar los botones del dashboard
                        dashboard.ir_libro_diario = lambda: self.stacked_widget.setCurrentIndex(1)
                        dashboard.ir_registro_asientos = lambda: self.stacked_widget.setCurrentIndex(2)
                        print("✅ Botones del dashboard conectados a la navegación")
                except Exception as e:
                    print(f"⚠️ No se pudieron conectar los botones del dashboard: {e}")
    
    def cerrar_sesion(self):
        """Cerrar sesión del usuario"""
        reply = QMessageBox.question(self, "Cerrar Sesión", 
                                   "¿Confirmar cierre de sesión del sistema?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.logout_requested.emit()