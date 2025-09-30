from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame,
                             QMessageBox, QGraphicsDropShadowEffect, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PySide6.QtGui import QColor, QFontDatabase
import os

class LoginWindow(QWidget):
    login_successful = Signal(object)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NecroLedger - Sistema Contable Inteligente")
        self.setMinimumSize(500, 600)
        self.setMaximumSize(800, 900)
        self.load_custom_fonts()
        self.apply_modern_style()
        self.setup_ui()
        self.setup_animations()
    
    def load_custom_fonts(self):
        """Cargar fuentes personalizadas para el diseño futurista"""
        font_dir = "src/assets/fonts/"
        if os.path.exists(font_dir):
            for font_file in os.listdir(font_dir):
                if font_file.endswith(('.ttf', '.otf')):
                    QFontDatabase.addApplicationFont(os.path.join(font_dir, font_file))
    
    def apply_modern_style(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #0A0E17, stop:0.3 #13182B, stop:0.7 #0F1425, stop:1 #0A0E17);
                color: #E6EEF3;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            
            QFrame#login_frame {
                background: rgba(16, 20, 35, 0.85);
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 20px;
                padding: 40px;
            }
            
            QLabel#title {
                font-size: 32px;
                font-weight: 800;
                color: #00E5FF;
                letter-spacing: 2px;
            }
            
            QLabel#subtitle {
                font-size: 14px;
                color: #8A94A6;
                font-weight: 300;
                letter-spacing: 1px;
            }
            
            QLineEdit {
                background: rgba(25, 30, 45, 0.9);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px 20px;
                font-size: 14px;
                color: #FFFFFF;
                font-weight: 400;
            }
            
            QLineEdit:focus {
                border: 1px solid rgba(0, 229, 255, 0.6);
                background: rgba(30, 35, 55, 0.95);
            }
            
            QLineEdit::placeholder {
                color: #5A6378;
                font-weight: 300;
            }
            
            QPushButton#login_btn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E5FF, stop:0.5 #B3009E, stop:1 #FF0080);
                border: none;
                border-radius: 12px;
                padding: 16px;
                font-size: 16px;
                font-weight: 600;
                color: white;
                letter-spacing: 1px;
            }
            
            QPushButton#login_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00F7FF, stop:0.5 #CC00B3, stop:1 #FF1A99);
            }
            
            QPushButton#login_btn:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00C4CC, stop:0.5 #990086, stop:1 #CC0066);
            }
            
            QPushButton#login_btn:disabled {
                background: #4A5568;
                color: #A0AEC0;
            }
            
            QLabel#credential_info {
                background: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 12px;
                font-size: 11px;
                color: #666;
            }
        """)
    
    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Frame central de login
        self.login_frame = QFrame()
        self.login_frame.setObjectName("login_frame")
        self.login_frame.setMinimumWidth(400)
        self.login_frame.setMaximumWidth(500)
        
        frame_layout = QVBoxLayout(self.login_frame)
        frame_layout.setSpacing(25)
        frame_layout.setContentsMargins(30, 40, 30, 40)
        
        # Header con título
        title = QLabel("⚡ NECROLEDGER")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("SISTEMA CONTABLE INTELIGENTE")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        
        frame_layout.addWidget(title)
        frame_layout.addWidget(subtitle)
        frame_layout.addSpacing(30)
        
        # Campos de formulario
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)
        
        # Usuario
        user_layout = QVBoxLayout()
        user_layout.setSpacing(8)
        
        user_label = QLabel("USUARIO")
        user_label.setStyleSheet("color: #98A0A6; font-size: 12px; font-weight: 600;")
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingresa tu usuario...")
        self.user_input.setText("admin")
        self.user_input.setMinimumHeight(45)
        
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_input)
        form_layout.addLayout(user_layout)
        
        # Contraseña
        pass_layout = QVBoxLayout()
        pass_layout.setSpacing(8)
        
        pass_label = QLabel("CONTRASEÑA")
        pass_label.setStyleSheet("color: #98A0A6; font-size: 12px; font-weight: 600;")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Ingresa tu contraseña...")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setText("admin123")
        self.pass_input.setMinimumHeight(45)
        
        pass_layout.addWidget(pass_label)
        pass_layout.addWidget(self.pass_input)
        form_layout.addLayout(pass_layout)
        
        frame_layout.addLayout(form_layout)
        frame_layout.addSpacing(30)
        
        # Botón de login
        self.login_btn = QPushButton("INICIAR SESIÓN")
        self.login_btn.setObjectName("login_btn")
        self.login_btn.setMinimumHeight(50)
        self.login_btn.clicked.connect(self.intentar_login)
        frame_layout.addWidget(self.login_btn)
        
        # Información de credenciales
        info_label = QLabel("Usuario: admin\nContraseña: admin123")
        info_label.setObjectName("credential_info")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setMinimumHeight(60)
        frame_layout.addWidget(info_label)
        
        # Añadir efectos de sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 229, 255, 80))
        shadow.setOffset(0, 0)
        self.login_frame.setGraphicsEffect(shadow)
        
        main_layout.addWidget(self.login_frame)
        
        # Conectar Enter para login
        self.user_input.returnPressed.connect(self.intentar_login)
        self.pass_input.returnPressed.connect(self.intentar_login)
    
    def setup_animations(self):
        # Animación de pulso para el frame
        self.frame_animation = QPropertyAnimation(self.login_frame, b"geometry")
        self.frame_animation.setDuration(1500)
        self.frame_animation.setLoopCount(-1)
        self.frame_animation.setEasingCurve(QEasingCurve.InOutSine)
        
        QTimer.singleShot(500, self.start_animations)
    
    def start_animations(self):
        original_geometry = self.login_frame.geometry()
        target_geometry = QRect(
            original_geometry.x() - 1,
            original_geometry.y() - 1,
            original_geometry.width() + 2,
            original_geometry.height() + 2
        )
        
        self.frame_animation.setStartValue(original_geometry)
        self.frame_animation.setEndValue(target_geometry)
        self.frame_animation.start()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = min(500, self.width() - 80)
        self.login_frame.setMaximumWidth(width)
    
    def intentar_login(self):
        from src.services.auth_service import AuthService
        from src.models import get_session, init_db
        
        username = self.user_input.text().strip()
        password = self.pass_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingresa usuario y contraseña")
            return
        
        try:
            engine = init_db()
            session = get_session(engine)
            
            auth_service = AuthService()
            success, usuario = auth_service.login(session, username, password)
            
            if success:
                QMessageBox.information(self, "Éxito", f"¡Bienvenido, {usuario.username}!")
                self.login_successful.emit(usuario)
            else:
                QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos")
                
            session.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {str(e)}")