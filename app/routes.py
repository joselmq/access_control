from flask import Blueprint, request, jsonify
from app import db
from app.models import PatenteAutorizada, RegistroAcceso
from app.utils import normalizar_patente
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configurar logging
logger = logging.getLogger(__name__)

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/verificar-acceso', methods=['POST'])
def verificar_acceso():
    """
    Verifica si una patente está autorizada para acceder al condominio.
    
    Request Body:
        {
            "patente": str (requerido) - Patente del vehículo a verificar
        }
    
    Returns:
        200: {"autorizado": bool}
        400: {"error": str} - Request inválido
        500: {"error": str} - Error interno del servidor
    """
    try:
        # Validar Content-Type
        if not request.is_json:
            logger.warning("Request sin Content-Type: application/json")
            return jsonify({
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        # Obtener datos del request
        data = request.get_json()
        
        # Validar campo requerido
        patente_raw = data.get('patente')
        if not patente_raw:
            logger.warning("Request sin campo 'patente'")
            return jsonify({
                'error': 'El campo "patente" es requerido'
            }), 400
        
        # Validar tipo de dato
        if not isinstance(patente_raw, str):
            logger.warning(f"Tipo de dato inválido para patente: {type(patente_raw)}")
            return jsonify({
                'error': 'El campo "patente" debe ser una cadena de texto'
            }), 400
        
        # Normalizar patente
        patente = normalizar_patente(patente_raw)
        
        if not patente:
            logger.warning(f"Patente vacía después de normalización: {patente_raw}")
            return jsonify({
                'error': 'Patente inválida o vacía'
            }), 400
        
        # Validar longitud razonable
        if len(patente) > 10:
            logger.warning(f"Patente demasiado larga: {patente}")
            return jsonify({
                'error': 'Patente excede longitud máxima permitida'
            }), 400
        
        # Buscar patente en base de datos
        patente_autorizada = PatenteAutorizada.query.filter_by(
            patente=patente
        ).first()
        
        autorizado = patente_autorizada is not None
        
        # Registrar intento de acceso
        registro = RegistroAcceso(
            patente=patente,
            autorizado=autorizado,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        db.session.add(registro)
        db.session.commit()
        
        # Log del evento
        if autorizado:
            logger.info(f"Acceso autorizado - Patente: {patente}")
        else:
            logger.warning(f"Acceso denegado - Patente no registrada: {patente}")
        
        return jsonify({
            'autorizado': autorizado
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado: {str(e)}")
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


@api.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint para monitoreo.
    
    Returns:
        200: {"status": "ok", "timestamp": str}
        503: {"status": "error", "message": str} - Si hay problemas con la BD
    """
    try:
        # Verificar conexión a base de datos
        db.session.execute(db.text('SELECT 1'))
        
        return jsonify({
            'status': 'ok',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'service': 'Control de Acceso API'
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Problema de conexión con la base de datos'
        }), 503


@api.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas"""
    return jsonify({
        'error': 'Endpoint no encontrado'
    }), 404


@api.errorhandler(405)
def method_not_allowed(error):
    """Manejo de métodos HTTP no permitidos"""
    return jsonify({
        'error': 'Método HTTP no permitido'
    }), 405