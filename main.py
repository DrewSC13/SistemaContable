import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Añadir src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.views.login_window import LoginWindow
from src.views.main_window import MainWindow
from src.models import init_db, create_default_user, create_default_accounts, get_session

class ContabilidadApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("NecroLedger")
        self.app.setApplicationVersion("1.0.0")
        
        # Inicializar base de datos
        self.init_database()
        
        # Mostrar login
        self.show_login()
    
    def init_database(self):
        try:
            self.engine = init_db()
            
            # Crear usuario y cuentas por defecto
            session = get_session(self.engine)
            create_default_user(session)
            create_default_accounts(session)
            session.close()
            
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"❌ Error inicializando DB: {e}")
            # Puedes continuar sin DB para desarrollo
    
    def show_login(self):
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
    
    def on_login_success(self, usuario):
        self.login_window.close()
        self.main_window = MainWindow(usuario)
        self.main_window.logout_requested.connect(self.on_logout)
        self.main_window.show()
    
    def on_logout(self):
        self.main_window.close()
        self.show_login()
    
    def run(self):
        return self.app.exec()

def main():
    app = ContabilidadApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main()
