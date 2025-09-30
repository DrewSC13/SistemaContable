from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100))
    creado_en = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

class CuentaContable(Base):
    __tablename__ = 'cuentas_contables'
    
    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(20))  # activo, pasivo, patrimonio, ingreso, gasto
    descripcion = Column(Text)
    activa = Column(Boolean, default=True)

class AsientoContable(Base):
    __tablename__ = 'asientos_contables'
    
    id = Column(Integer, primary_key=True)
    numero = Column(String(20), unique=True, nullable=False)
    fecha = Column(DateTime, nullable=False)
    descripcion = Column(Text)
    creado_por = Column(Integer, ForeignKey('usuarios.id'))
    creado_en = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario")
    lineas = relationship("LineaAsiento", back_populates="asiento")

class LineaAsiento(Base):
    __tablename__ = 'lineas_asiento'
    
    id = Column(Integer, primary_key=True)
    asiento_id = Column(Integer, ForeignKey('asientos_contables.id'))
    cuenta_id = Column(Integer, ForeignKey('cuentas_contables.id'))
    debe = Column(Numeric(15, 2), default=0)
    haber = Column(Numeric(15, 2), default=0)
    descripcion = Column(Text)
    
    # Relaciones
    asiento = relationship("AsientoContable", back_populates="lineas")
    cuenta = relationship("CuentaContable")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    accion = Column(String(100), nullable=False)
    tabla_afectada = Column(String(50))
    registro_id = Column(Integer)
    detalles = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario")

# Configuración de la base de datos
def init_db():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# Crear usuario por defecto
def create_default_user(session):
    import bcrypt
    
    default_user = session.query(Usuario).filter_by(username='admin').first()
    if not default_user:
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw('Popete13'.encode(), bcrypt.gensalt()).decode()
        
        default_user = Usuario(
            username='admin',
            password_hash=hashed_password,
            email='admin@necroledger.com'
        )
        session.add(default_user)
        session.commit()
        print("✅ Usuario admin creado: admin / Popete13")

# Crear cuentas contables básicas por defecto
def create_default_accounts(session):
    cuentas_basicas = [
        # ACTIVOS
        {'codigo': '1', 'nombre': 'ACTIVOS', 'tipo': 'activo', 'descripcion': 'Cuenta de control de activos'},
        {'codigo': '1.1', 'nombre': 'CAJA GENERAL', 'tipo': 'activo', 'descripcion': 'Efectivo en caja'},
        {'codigo': '1.2', 'nombre': 'BANCOS', 'tipo': 'activo', 'descripcion': 'Cuentas bancarias'},
        {'codigo': '1.3', 'nombre': 'CUENTAS POR COBRAR', 'tipo': 'activo', 'descripcion': 'Clientes por cobrar'},
        {'codigo': '1.4', 'nombre': 'INVENTARIOS', 'tipo': 'activo', 'descripcion': 'Mercaderías en stock'},
        
        # PASIVOS
        {'codigo': '2', 'nombre': 'PASIVOS', 'tipo': 'pasivo', 'descripcion': 'Cuenta de control de pasivos'},
        {'codigo': '2.1', 'nombre': 'CUENTAS POR PAGAR', 'tipo': 'pasivo', 'descripcion': 'Proveedores por pagar'},
        {'codigo': '2.2', 'nombre': 'PRÉSTAMOS BANCARIOS', 'tipo': 'pasivo', 'descripcion': 'Deudas con bancos'},
        
        # PATRIMONIO
        {'codigo': '3', 'nombre': 'PATRIMONIO', 'tipo': 'patrimonio', 'descripcion': 'Cuenta de control de patrimonio'},
        {'codigo': '3.1', 'nombre': 'CAPITAL SOCIAL', 'tipo': 'patrimonio', 'descripcion': 'Capital de los socios'},
        {'codigo': '3.2', 'nombre': 'UTILIDADES ACUMULADAS', 'tipo': 'patrimonio', 'descripcion': 'Ganancias retenidas'},
        
        # INGRESOS
        {'codigo': '4', 'nombre': 'INGRESOS', 'tipo': 'ingreso', 'descripcion': 'Cuenta de control de ingresos'},
        {'codigo': '4.1', 'nombre': 'VENTAS', 'tipo': 'ingreso', 'descripcion': 'Ingresos por ventas'},
        {'codigo': '4.2', 'nombre': 'SERVICIOS', 'tipo': 'ingreso', 'descripcion': 'Ingresos por servicios'},
        
        # GASTOS
        {'codigo': '5', 'nombre': 'GASTOS', 'tipo': 'gasto', 'descripcion': 'Cuenta de control de gastos'},
        {'codigo': '5.1', 'nombre': 'GASTOS DE VENTAS', 'tipo': 'gasto', 'descripcion': 'Gastos operativos de ventas'},
        {'codigo': '5.2', 'nombre': 'GASTOS ADMINISTRATIVOS', 'tipo': 'gasto', 'descripcion': 'Gastos de administración'},
        {'codigo': '5.3', 'nombre': 'GASTOS FINANCIEROS', 'tipo': 'gasto', 'descripcion': 'Intereses y gastos financieros'},
    ]
    
    for cuenta_data in cuentas_basicas:
        cuenta_existente = session.query(CuentaContable).filter_by(codigo=cuenta_data['codigo']).first()
        if not cuenta_existente:
            nueva_cuenta = CuentaContable(
                codigo=cuenta_data['codigo'],
                nombre=cuenta_data['nombre'],
                tipo=cuenta_data['tipo'],
                descripcion=cuenta_data['descripcion']
            )
            session.add(nueva_cuenta)
    
    session.commit()
    print("✅ Cuentas contables básicas creadas")
