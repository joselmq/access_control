# Control de Acceso - API REST

API REST para control de acceso vehicular en condominios mediante reconocimiento automático de patentes.

## Descripción

Esta API recibe patentes vehiculares detectadas por un sistema OCR externo, verifica si están autorizadas en la base de datos y registra todos los intentos de acceso para auditoría.

## Características

- ✅ Verificación de patentes autorizadas en tiempo real
- ✅ Registro automático de todos los intentos de acceso
- ✅ Normalización automática de patentes (mayúsculas, sin espacios/guiones)
- ✅ Validación robusta de requests
- ✅ Logging completo para auditoría
- ✅ Health check endpoint para monitoreo
- ✅ Manejo profesional de errores

## Ejemplos (input/output)

![Imagen 1](<images/Screenshot%20(78).png>)
![Imagen 2](<images/Screenshot%20(79).png>)
![Imagen 3](<images/Screenshot%20(80).png>)
![Imagen 4](<images/Screenshot%20(81).png>)

## Requisitos

- Python 3.8+
- MySQL 5.7+ o MariaDB 10.3+
- pip

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd control-acceso-condominio
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-muy-segura-cambiala-en-produccion
DATABASE_URL=mysql+pymysql://usuario:password@localhost/control_acceso
```

**Nota:** Reemplaza `usuario`, `password` y `localhost` con tus credenciales reales de MySQL.

### 6. Crear base de datos

Ejecuta en tu cliente MySQL (base de datos dummy):

```sql
-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS control_acceso
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos recién creada
USE control_acceso;

-- Crear tabla: patentes_autorizadas
CREATE TABLE IF NOT EXISTS patentes_autorizadas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patente VARCHAR(10) UNIQUE NOT NULL,
  nombre_residente VARCHAR(100) NOT NULL,
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Crear tabla: registro_accesos
CREATE TABLE IF NOT EXISTS registro_accesos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patente VARCHAR(10) NOT NULL,
  autorizado BOOLEAN NOT NULL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX (patente)
) ENGINE=InnoDB;

-- Insertar datos de ejemplo
INSERT INTO patentes_autorizadas (patente, nombre_residente)
VALUES
  ('BBKL45', 'Juan Pérez'),
  ('XXYZ99', 'María González'),
  ('ABCD12', 'Pedro Ramírez');

```

### 7. Ejecutar la aplicación

```bash
python run.py
```

La API estará disponible en `http://localhost:5000`

## Uso

### Verificar acceso

**Endpoint:** `POST /api/verificar-acceso`

**Request:**

```json
{
  "patente": "BBKL45"
}
```

**Response (Autorizado):**

```json
{
  "autorizado": true
}
```

**Response (No autorizado):**

```json
{
  "autorizado": false
}
```

**Códigos de estado:**

- `200`: Request procesado correctamente
- `400`: Request inválido (falta campo, tipo incorrecto, etc.)
- `500`: Error interno del servidor

### Health Check

**Endpoint:** `GET /api/health`

**Response:**

```json
{
  "status": "ok",
  "timestamp": "2025-10-21T14:30:00.123456",
  "service": "Control de Acceso API"
}
```

## Ejemplos con cURL

### Verificar patente autorizada

```bash
curl -X POST http://localhost:5000/api/verificar-acceso \
  -H "Content-Type: application/json" \
  -d "{\"patente\": \"BBKL45\"}"
```

### Verificar patente con espacios (se normalizará)

```bash
curl -X POST http://localhost:5000/api/verificar-acceso \
  -H "Content-Type: application/json" \
  -d "{\"patente\": \"BB-KL 45\"}"
```

### Health check

```bash
curl http://localhost:5000/api/health
```

## Estructura del proyecto

```
control-acceso-condominio/
├── app/
│   ├── __init__.py          # Inicialización de Flask
│   ├── models.py            # Modelos de base de datos
│   ├── routes.py            # Endpoints de la API
│   └── utils.py             # Funciones auxiliares
├── logs/                    # Logs de la aplicación (auto-generado)
├── venv/                    # Entorno virtual
├── .env                     # Variables de entorno (no subir a git)
├── .gitignore              # Archivos ignorados por git
├── config.py               # Configuración de la aplicación
├── requirements.txt        # Dependencias Python
├── run.py                  # Punto de entrada
└── README.md              # Este archivo
```

## Base de Datos

### Tabla: patentes_autorizadas

| Campo            | Tipo         | Descripción                  |
| ---------------- | ------------ | ---------------------------- |
| id               | Integer (PK) | Identificador único          |
| patente          | String(10)   | Patente normalizada (UNIQUE) |
| nombre_residente | String(100)  | Nombre del residente         |
| fecha_registro   | DateTime     | Fecha de registro            |

### Tabla: registro_accesos

| Campo      | Tipo         | Descripción              |
| ---------- | ------------ | ------------------------ |
| id         | Integer (PK) | Identificador único      |
| patente    | String(10)   | Patente detectada        |
| autorizado | Boolean      | Si fue autorizado o no   |
| timestamp  | DateTime     | Fecha y hora del intento |

## Agregar patentes manualmente

Para testing, puedes insertar patentes directamente en MySQL:

```sql
USE control_acceso;

INSERT INTO patentes_autorizadas (patente, nombre_residente, fecha_registro)
VALUES
  ('BBKL45', '304', 'Juan Pérez', NOW()),
  ('XXYZ99', '102', 'María González', NOW()),
  ('ABCD12', '205', 'Pedro Ramírez', NOW());
```

## Logs

Los logs se guardan automáticamente en `logs/control_acceso.log` con rotación automática:

- Máximo 10MB por archivo
- Mantiene 10 archivos históricos
- Incluye timestamp, nivel y mensaje detallado

## Desarrollo

### Ejecutar en modo desarrollo

```bash
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows CMD
$env:FLASK_ENV="development"  # Windows PowerShell

python run.py
```

### Testing

Puedes usar herramientas como:

- **cURL**: Ejemplos incluidos arriba
- **Postman**: Importa los endpoints
- **HTTPie**: `http POST localhost:5000/api/verificar-acceso patente=BBKL45`
- **Python requests**: Ver scripts de ejemplo en `/tests` (si existen)

## Producción

Para deployment en producción:

1. Cambia `FLASK_ENV=production` en `.env`
2. Usa un servidor WSGI como **Gunicorn**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```
3. Configura un reverse proxy (Nginx/Apache)
4. Usa supervisor/systemd para mantener el proceso corriendo
5. Configura backups automáticos de la base de datos

## Seguridad

⚠️ **Para producción, considera implementar:**

- Autenticación con API Keys
- Rate limiting (ya incluido flask-limiter en requirements)
- HTTPS/TLS
- Firewall para restringir acceso a IPs conocidas
- Secrets management (Vault, AWS Secrets Manager, etc.)

## Troubleshooting

### Error: "Access denied for user"

- Verifica credenciales en `.env`
- Asegúrate que el usuario MySQL tenga permisos

### Error: "Can't connect to MySQL server"

- Verifica que MySQL esté corriendo
- Comprueba host y puerto en `DATABASE_URL`

### Error: "Unknown database 'control_acceso'"

- Crea la base de datos manualmente (ver paso 6)

### Logs no se generan

- Verifica permisos de escritura en la carpeta del proyecto
- La carpeta `logs/` se crea automáticamente al iniciar

## Licencia

MIT

## Autor

Desarrollado como proyecto de demostración técnica.

## Contacto

Para consultas o issues, crear un ticket en el repositorio.
