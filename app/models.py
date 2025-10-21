from app import db
from datetime import datetime, timezone

class PatenteAutorizada(db.Model):
    __tablename__ = 'patentes_autorizadas'
    
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(10), unique=True, nullable=False, index=True)
    nombre_residente = db.Column(db.String(100))
    fecha_registro = db.Column(db.DateTime, default=datetime.now(timezone.utc).isoformat())


class RegistroAcceso(db.Model):
    __tablename__ = 'registro_accesos'
    
    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(10), nullable=False, index=True)
    autorizado = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc).isoformat(), index=True)
    
    def __repr__(self):
        return f'<Acceso {self.patente} - {"Autorizado" if self.autorizado else "Denegado"}>'
