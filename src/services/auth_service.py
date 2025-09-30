import bcrypt
from sqlalchemy.orm import Session
from models import Usuario, AuditLog

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception:
            return False
    
    def login(self, session: Session, username: str, password: str) -> tuple[bool, Usuario | None]:
        try:
            usuario = session.query(Usuario).filter_by(username=username, activo=True).first()
            
            if usuario and self.verify_password(password, usuario.password_hash):
                # Registrar en audit log
                audit = AuditLog(
                    usuario_id=usuario.id,
                    accion="LOGIN_EXITOSO",
                    tabla_afectada="usuarios",
                    registro_id=usuario.id,
                    detalles=f"Login exitoso para usuario {username}"
                )
                session.add(audit)
                session.commit()
                
                return True, usuario
            else:
                # Login fallido
                if usuario:
                    audit = AuditLog(
                        usuario_id=usuario.id,
                        accion="LOGIN_FALLIDO",
                        tabla_afectada="usuarios", 
                        registro_id=usuario.id,
                        detalles="Contraseña incorrecta"
                    )
                    session.add(audit)
                    session.commit()
                
                return False, None
                
        except Exception as e:
            print(f"Error en login: {e}")
            return False, None
    
    def cambiar_password(self, session: Session, usuario_id: int, nueva_password: str) -> bool:
        try:
            usuario = session.query(Usuario).filter_by(id=usuario_id).first()
            if usuario:
                usuario.password_hash = self.hash_password(nueva_password)
                
                audit = AuditLog(
                    usuario_id=usuario_id,
                    accion="CAMBIO_PASSWORD",
                    tabla_afectada="usuarios",
                    registro_id=usuario_id,
                    detalles="Contraseña cambiada exitosamente"
                )
                session.add(audit)
                session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error cambiando password: {e}")
            return False
