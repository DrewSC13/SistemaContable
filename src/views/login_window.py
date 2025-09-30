from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame,
                             QMessageBox)
from PySide6.QtCore import Qt, Signal

class LoginWindow(QWidget):
    login_successful = Signal(object)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NecroLedger - Sistema Contable")
        self.setFixedSize(450, 500)
        self.apply_style()
        self.setup_ui()
    
    def apply_style(self):
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0B0D0F, stop:0.5 #101315, stop:1 #0B0D0F);
                color: #E6EEF3;
                font-family: 'Segoe UI', sans-serif;
            }
            
            QFrame#login_frame {
                background: rgba(16, 19, 21, 0.95);
                border: 2px solid #2B2F36;
                border-radius: 15px;
                padding: 30px;
            }
            
            QLabel#title {
                font-family: 'Segoe UI', sans-serif;
                font-size: 24px;
                font-weight: bold;
                color: #00E5FF;
                background: transparent;
            }
            
            QLabel#subtitle {
                font-size: 12px;
                color: #98A0A6;
                background: transparent;
            }
            
            QLineEdit {
                background: rgba(43, 47, 54, 0.8);
                border: 1px solid #2B2F36;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #E6EEF3;
            }
            
            QLineEdit:focus {
                border-color: #00E5FF;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E5FF, stop:1 #B3009E);
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00F7FF, stop:1 #CC00B3);
            }
        """)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Frame de login
        login_frame = QFrame()
        login_frame.setObjectName("login_frame")
        frame_layout = QVBoxLayout(login_frame)
        frame_layout.setSpacing(20)
        
        # Título
        title = QLabel("NECROLEDGER")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(title)
        
        subtitle = QLabel("SISTEMA CONTABLE")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(subtitle)
        
        frame_layout.addSpacing(30)
        
        # Campos de formulario
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Usuario
        user_layout = QVBoxLayout()
        user_label = QLabel("USUARIO:")
        user_label.setStyleSheet("color: #98A0A6; font-size: 12px; font-weight: 500;")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingresa tu usuario...")
        self.user_input.setText("admin")
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_input)
        form_layout.addLayout(user_layout)
        
        # Contraseña
        pass_layout = QVBoxLayout()
        pass_label = QLabel("CONTRASEÑA:")
        pass_label.setStyleSheet("color: #98A0A6; font-size: 12px; font-weight: 500;")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Ingresa tu contraseña...")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setText("admin123")
        pass_layout.addWidget(pass_label)
        pass_layout.addWidget(self.pass_input)
        form_layout.addLayout(pass_layout)
        
        frame_layout.addLayout(form_layout)
        
        frame_layout.addSpacing(25)
        
        # Botón de login
        self.login_btn = QPushButton("INICIAR SESIÓN")
        self.login_btn.clicked.connect(self.intentar_login)
        frame_layout.addWidget(self.login_btn)
        
        # Información de credenciales
        info_label = QLabel("Usuario: admin\nContraseña: admin123")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #666; font-size: 10px; margin-top: 20px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 5px;")
        frame_layout.addWidget(info_label)
        
        layout.addWidget(login_frame)
        
        # Conectar Enter para login
        self.user_input.returnPressed.connect(self.intentar_login)
        self.pass_input.returnPressed.connect(self.intentar_login)
    
    def intentar_login(self):
        from services.auth_service import AuthService
        from models import get_session, init_db
        
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
