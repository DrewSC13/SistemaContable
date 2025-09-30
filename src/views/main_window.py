from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QStackedWidget,
                             QFrame, QToolBar, QStatusBar, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFontDatabase, QAction
import os

class SidebarHeader(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar-header")
        self.setFixedHeight(120)  # Reducido para responsividad
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 10)  # Márgenes reducidos
        layout.setSpacing(5)
        
        title = QLabel("NECROLEDGER")
        title.setObjectName("sidebar-title")
        title.setAlignment(Qt.AlignCenter)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        subtitle = QLabel("CONTABILIDAD")
        subtitle.setObjectName("sidebar-subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)

class MenuButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setObjectName("menu-button")
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(60)  # Reducido para responsividad
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)  # Márgenes reducidos
        layout.setSpacing(0)
        
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            background: transparent; 
            color: inherit; 
            font-size: 14px;  # Reducido
            font-weight: 500;
            font-family: 'Segoe UI', sans-serif;
        """)
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)

class UserSection(QFrame):
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setObjectName("user-section")
        self.setFixedHeight(80)  # Reducido
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Márgenes reducidos
        layout.setSpacing(10)
        
        avatar_frame = QFrame()
        avatar_frame.setObjectName("user-avatar")
        avatar_frame.setFixedSize(40, 40)  # Reducido
        
        avatar_layout = QVBoxLayout(avatar_frame)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        
        avatar_text = QLabel("A")
        avatar_text.setAlignment(Qt.AlignCenter)
        avatar_text.setStyleSheet("""
            color: #0B0D0F; 
            font-weight: bold; 
            font-size: 14px;  # Reducido
            background: transparent;
        """)
        avatar_layout.addWidget(avatar_text)
        
        user_info = QFrame()
        user_info.setObjectName("user-info")
        user_layout = QVBoxLayout(user_info)
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(2)
        
        name_label = QLabel(self.usuario.username.upper())
        name_label.setObjectName("user-name")
        name_label.setAlignment(Qt.AlignCenter)
        
        role_label = QLabel("ADMIN")
        role_label.setObjectName("user-role")
        role_label.setAlignment(Qt.AlignCenter)
        
        user_layout.addWidget(name_label)
        user_layout.addWidget(role_label)
        
        layout.addWidget(avatar_frame)
        layout.addWidget(user_info)
        layout.addStretch()

class MainWindow(QMainWindow):
    logout_requested = Signal()
    
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.setWindowTitle(f"NecroLedger | {usuario.username}")
        
        # Hacer la ventana responsive
        self.setMinimumSize(1200, 700)  # Tamaño mínimo
        self.resize(1400, 800)  # Tamaño inicial
        
        self.load_fonts()
        self.apply_style()
        self.setup_ui()
        
    def load_fonts(self):
        font_dir = "src/assets/fonts/"
        if os.path.exists(font_dir):
            for font_file in os.listdir(font_dir):
                if font_file.endswith(('.ttf', '.otf')):
                    QFontDatabase.addApplicationFont(os.path.join(font_dir, font_file))
    
    def apply_style(self):
        style_file = "src/assets/styles/style.qss"
        if os.path.exists(style_file):
            with open(style_file, "r") as f:
                self.setStyleSheet(f.read())
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.setup_sidebar(main_layout)
        self.setup_content_area(main_layout)
        self.setup_header()
        self.setup_statusbar()
    
    def setup_sidebar(self, main_layout):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(280)  # Ancho mínimo
        sidebar.setMaximumWidth(350)  # Ancho máximo
        sidebar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        sidebar_header = SidebarHeader()
        sidebar_layout.addWidget(sidebar_header)
        
        menu_container = QFrame()
        menu_container.setObjectName("menu-container")
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(5, 10, 5, 10)
        menu_layout.setSpacing(0)
        
        # Grupo 1: CONTABILIDAD
        core_group = self.create_menu_group("CONTABILIDAD", menu_layout)
        self.menu_buttons = []
        
        core_buttons = [
            "Dashboard",
            "Libro Diario", 
            "Libro Mayor",
            "Balances"
        ]
        
        for text in core_buttons:
            btn = MenuButton(text)
            btn.clicked.connect(lambda checked, idx=len(self.menu_buttons): self.cambiar_modulo(idx))
            core_group.layout().addWidget(btn)
            self.menu_buttons.append(btn)
        
        menu_layout.addSpacing(8)
        
        # Grupo 2: OPERACIONES
        ops_group = self.create_menu_group("OPERACIONES", menu_layout)
        
        ops_buttons = [
            "Ventas",
            "Compras",
            "Tesorería",
            "Inventarios"
        ]
        
        for text in ops_buttons:
            btn = MenuButton(text)
            btn.clicked.connect(lambda checked, idx=len(self.menu_buttons): self.cambiar_modulo(idx))
            ops_group.layout().addWidget(btn)
            self.menu_buttons.append(btn)
        
        menu_layout.addSpacing(8)
        
        # Grupo 3: ADMINISTRACIÓN
        admin_group = self.create_menu_group("ADMINISTRACIÓN", menu_layout)
        
        admin_buttons = [
            "Clientes",
            "Proveedores", 
            "Reportes",
            "Configuración"
        ]
        
        for text in admin_buttons:
            btn = MenuButton(text)
            btn.clicked.connect(lambda checked, idx=len(self.menu_buttons): self.cambiar_modulo(idx))
            admin_group.layout().addWidget(btn)
            self.menu_buttons.append(btn)
        
        menu_layout.addStretch()
        
        user_section = UserSection(self.usuario)
        menu_layout.addWidget(user_section)
        
        logout_btn = QPushButton("CERRAR SESIÓN")
        logout_btn.setObjectName("logout-button")
        logout_btn.clicked.connect(self.cerrar_sesion)
        logout_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        menu_layout.addWidget(logout_btn)
        
        sidebar_layout.addWidget(menu_container)
        main_layout.addWidget(sidebar)
        
        if self.menu_buttons:
            self.menu_buttons[0].setChecked(True)
    
    def create_menu_group(self, title, parent_layout):
        group = QFrame()
        group.setObjectName("menu-group")
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        title_label = QLabel(title)
        title_label.setObjectName("menu-group-title")
        title_label.setFixedHeight(25)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        parent_layout.addWidget(group)
        return group
    
    def setup_content_area(self, main_layout):
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(self.stacked_widget)
        
        # Añadir vistas
        from .dashboard_view import DashboardView
        from .journal_view import JournalView
        
        self.stacked_widget.addWidget(DashboardView(self.usuario))
        self.stacked_widget.addWidget(JournalView(self.usuario))
        
        # Placeholders para otros módulos
        for i in range(10):
            placeholder = QLabel(f"Módulo {i+2}\nEn desarrollo")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet("""
                font-size: 18px; 
                color: #98A0A6; 
                padding: 40px;
                font-family: 'Segoe UI', sans-serif;
            """)
            placeholder.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.stacked_widget.addWidget(placeholder)
        
        main_layout.addWidget(content_frame)
    
    def setup_header(self):
        toolbar = QToolBar()
        toolbar.setObjectName("header")
        toolbar.setFixedHeight(50)
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addToolBar(toolbar)
        
        context_label = QLabel("SISTEMA CONTABLE PROFESIONAL")
        context_label.setStyleSheet("""
            color: #00E5FF; 
            padding: 6px; 
            font-size: 14px; 
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        """)
        context_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        toolbar.addWidget(context_label)
    
    def setup_statusbar(self):
        status_bar = QStatusBar()
        status_bar.setStyleSheet("""
            background-color: #101315; 
            color: #98A0A6; 
            border-top: 1px solid #2B2F36;
            padding: 6px;
            font-family: 'Segoe UI', sans-serif;
            font-size: 10px;
        """)
        status_bar.showMessage(f"Conectado: {self.usuario.username} | NecroLedger v1.0")
        self.setStatusBar(status_bar)
    
    def cambiar_modulo(self, index):
        for btn in self.menu_buttons:
            btn.setChecked(False)
        
        if 0 <= index < len(self.menu_buttons):
            self.menu_buttons[index].setChecked(True)
        
        if index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(index)
    
    def cerrar_sesion(self):
        reply = QMessageBox.question(self, "Cerrar Sesión", 
                                   "¿Confirmar cierre de sesión?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.logout_requested.emit()

    # Manejar redimensionamiento para responsividad
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Aquí puedes agregar lógica adicional para redimensionamiento
        pass
