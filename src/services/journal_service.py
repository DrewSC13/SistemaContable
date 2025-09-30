from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from models import AsientoContable, LineaAsiento, CuentaContable, AuditLog

class JournalService:
    def __init__(self):
        pass
    
    def crear_asiento(self, session: Session, numero: str, fecha: datetime, 
                     descripcion: str, lineas: list, usuario_id: int) -> tuple[bool, str]:
        """
        Crea un nuevo asiento contable con validación de partida doble
        """
        try:
            # Validar partida doble
            total_debe = sum(linea['debe'] for linea in lineas)
            total_haber = sum(linea['haber'] for linea in lineas)
            
            if abs(total_debe - total_haber) > 0.01:  # Tolerancia para decimales
                return False, f"❌ ERROR: La partida no está cuadrada\nDebe: Q {total_debe:,.2f}\nHaber: Q {total_haber:,.2f}\nDiferencia: Q {total_debe - total_haber:,.2f}"
            
            # Verificar que el número de asiento no exista
            asiento_existente = session.query(AsientoContable).filter_by(numero=numero).first()
            if asiento_existente:
                return False, f"❌ El número de asiento {numero} ya existe"
            
            # Validar que todas las cuentas existan
            for linea in lineas:
                cuenta = session.query(CuentaContable).filter_by(id=linea['cuenta_id']).first()
                if not cuenta:
                    return False, f"❌ La cuenta con ID {linea['cuenta_id']} no existe"
                if not cuenta.activa:
                    return False, f"❌ La cuenta {cuenta.codigo} - {cuenta.nombre} está inactiva"
            
            # Crear asiento
            nuevo_asiento = AsientoContable(
                numero=numero,
                fecha=fecha,
                descripcion=descripcion,
                creado_por=usuario_id
            )
            session.add(nuevo_asiento)
            session.flush()  # Para obtener el ID
            
            # Crear líneas del asiento
            for linea in lineas:
                nueva_linea = LineaAsiento(
                    asiento_id=nuevo_asiento.id,
                    cuenta_id=linea['cuenta_id'],
                    debe=linea['debe'],
                    haber=linea['haber'],
                    descripcion=linea.get('descripcion', '')
                )
                session.add(nueva_linea)
            
            # Registrar en audit log
            audit = AuditLog(
                usuario_id=usuario_id,
                accion="CREAR_ASIENTO",
                tabla_afectada="asientos_contables",
                registro_id=nuevo_asiento.id,
                detalles=f"Asiento {numero} creado: {descripcion} - Total: Q {total_debe:,.2f}"
            )
            session.add(audit)
            
            session.commit()
            return True, f"✅ Asiento {numero} creado exitosamente\nTotal: Q {total_debe:,.2f}\nLíneas: {len(lineas)}"
            
        except Exception as e:
            session.rollback()
            return False, f"❌ Error al crear asiento: {str(e)}"
    
    def obtener_asientos(self, session: Session, fecha_inicio: datetime = None, 
                        fecha_fin: datetime = None) -> list:
        """
        Obtiene asientos contables con filtros opcionales
        """
        try:
            query = session.query(AsientoContable)
            
            if fecha_inicio:
                query = query.filter(AsientoContable.fecha >= fecha_inicio)
            if fecha_fin:
                query = query.filter(AsientoContable.fecha <= fecha_fin)
            
            asientos = query.order_by(AsientoContable.fecha.desc(), 
                                    AsientoContable.numero.desc()).all()
            
            resultado = []
            for asiento in asientos:
                lineas = session.query(LineaAsiento).filter_by(asiento_id=asiento.id).all()
                
                asiento_data = {
                    'id': asiento.id,
                    'numero': asiento.numero,
                    'fecha': asiento.fecha,
                    'descripcion': asiento.descripcion,
                    'creado_por': asiento.creado_por,
                    'creado_en': asiento.creado_en,
                    'lineas': []
                }
                
                for linea in lineas:
                    cuenta = session.query(CuentaContable).filter_by(id=linea.cuenta_id).first()
                    linea_data = {
                        'id': linea.id,
                        'cuenta_codigo': cuenta.codigo if cuenta else '',
                        'cuenta_nombre': cuenta.nombre if cuenta else '',
                        'debe': float(linea.debe),
                        'haber': float(linea.haber),
                        'descripcion': linea.descripcion
                    }
                    asiento_data['lineas'].append(linea_data)
                
                resultado.append(asiento_data)
            
            return resultado
            
        except Exception as e:
            print(f"❌ Error al obtener asientos: {e}")
            return []
    
    def eliminar_asiento(self, session: Session, asiento_id: int, usuario_id: int) -> tuple[bool, str]:
        """
        Elimina un asiento contable
        """
        try:
            asiento = session.query(AsientoContable).filter_by(id=asiento_id).first()
            if not asiento:
                return False, "❌ Asiento no encontrado"
            
            # Obtener información para el log
            numero_asiento = asiento.numero
            lineas_count = session.query(LineaAsiento).filter_by(asiento_id=asiento_id).count()
            
            # Eliminar líneas primero
            session.query(LineaAsiento).filter_by(asiento_id=asiento_id).delete()
            
            # Eliminar asiento
            session.delete(asiento)
            
            # Registrar en audit log
            audit = AuditLog(
                usuario_id=usuario_id,
                accion="ELIMINAR_ASIENTO",
                tabla_afectada="asientos_contables",
                registro_id=asiento_id,
                detalles=f"Asiento {numero_asiento} eliminado - Líneas: {lineas_count}"
            )
            session.add(audit)
            
            session.commit()
            return True, f"✅ Asiento {numero_asiento} eliminado exitosamente"
            
        except Exception as e:
            session.rollback()
            return False, f"❌ Error al eliminar asiento: {str(e)}"
    
    def obtener_cuentas_contables(self, session: Session) -> list:
        """
        Obtiene todas las cuentas contables activas
        """
        try:
            cuentas = session.query(CuentaContable).filter_by(activa=True).order_by(CuentaContable.codigo).all()
            return [{'id': c.id, 'codigo': c.codigo, 'nombre': c.nombre, 'tipo': c.tipo} for c in cuentas]
        except Exception as e:
            print(f"❌ Error al obtener cuentas: {e}")
            return []
    
    def generar_numero_asiento(self, session: Session) -> str:
        """
        Genera un número de asiento automático
        """
        try:
            # Formato: AS-YYYYMMDD-XXX
            fecha_actual = datetime.now()
            prefijo = f"AS-{fecha_actual.strftime('%Y%m%d')}"
            
            # Contar asientos del día
            asientos_hoy = session.query(AsientoContable).filter(
                AsientoContable.numero.like(f"{prefijo}-%")
            ).count()
            
            numero = f"{prefijo}-{asientos_hoy + 1:03d}"
            return numero
            
        except Exception as e:
            print(f"❌ Error generando número de asiento: {e}")
            return f"AS-{datetime.now().strftime('%Y%m%d')}-001"
    
    def obtener_resumen_diario(self, session: Session, fecha: datetime = None) -> dict:
        """
        Obtiene resumen del libro diario para una fecha específica
        """
        try:
            if not fecha:
                fecha = datetime.now()
            
            # Asientos del día
            asientos = session.query(AsientoContable).filter(
                AsientoContable.fecha == fecha.date()
            ).all()
            
            total_debe = 0
            total_haber = 0
            
            for asiento in asientos:
                lineas = session.query(LineaAsiento).filter_by(asiento_id=asiento.id).all()
                for linea in lineas:
                    total_debe += float(linea.debe)
                    total_haber += float(linea.haber)
            
            return {
                'fecha': fecha,
                'total_asientos': len(asientos),
                'total_debe': total_debe,
                'total_haber': total_haber,
                'diferencia': total_debe - total_haber
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo resumen diario: {e}")
            return {'fecha': fecha, 'total_asientos': 0, 'total_debe': 0, 'total_haber': 0, 'diferencia': 0}
