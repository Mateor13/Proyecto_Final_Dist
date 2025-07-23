# Sistema de Gestión de Usuarios y Productos con Balanceador de Carga

## 👥 Autores
- **Astudillo Anthony**
- **Cobacango Walter** 
- **García Mireya**
- **Torres Mateo**

## 🚀 ¿Qué hace este proyecto?

Este proyecto es un **sistema web** que permite gestionar usuarios y productos de manera eficiente. Lo especial de este sistema es que utiliza una **arquitectura distribuida** con múltiples servidores y un balanceador de carga para manejar muchas solicitudes al mismo tiempo.

### 🎯 Funcionalidades principales:
- **Registro de usuarios**: Las personas pueden crear cuentas nuevas
- **Inicio de sesión**: Los usuarios pueden acceder con su email y contraseña
- **Gestión de productos**: Se pueden registrar y administrar productos con información como:
  - Nombre del producto
  - Código único
  - Descripción detallada
  - Cantidad disponible
  - Categoría
- **Actualizar productos**: Puedes actualizar todos los campos de un producto excepto el código.
- **Eliminar productos**: Puedes eliminar productos desde la tabla, con confirmación de seguridad.
- **Mensajes de confirmación**: Al eliminar o actualizar, se muestra un mensaje de éxito o error en pantalla.
- **Validaciones mejoradas**: Los formularios validan correctamente los datos antes de guardar o actualizar.

## 🏗️ ¿Cómo está construido?

### Arquitectura del Sistema

El proyecto utiliza una **arquitectura de microservicios** con los siguientes componentes:

#### 🔄 **Balanceador de Carga (NGINX)**
- Es como un "director de tráfico" que recibe todas las peticiones
- Las distribuye entre los 3 servidores disponibles
- Si un servidor está ocupado, envía la petición a otro
- Funciona en el puerto 8080

#### 🖥️ **Tres Servidores Web Idénticos**
- **Servidor 1, 2 y 3**: Cada uno es una copia exacta del sistema
- Todos pueden manejar las mismas funciones (login, registro, etc.)
- Si uno falla, los otros siguen funcionando
- Están hechos con **Flask** (un framework de Python)

#### 🗄️ **Base de Datos MySQL**
- **db_usuarios**: Guarda información de las cuentas de usuario
- **db_productos**: Almacena el catálogo de productos
- Ambas bases de datos están conectadas a todos los servidores

### 🐳 **Docker y Contenedores**
Todo el sistema funciona con **Docker**, que es como tener "cajas" separadas para cada componente:
- Una caja para NGINX
- Una caja para cada servidor (3 en total)
- Las cajas se comunican entre sí a través de una red virtual

## 🚀 ¿Cómo ejecutar el proyecto?

### Requisitos previos:
- Tener **Docker** y **Docker Compose** instalados
- Tener acceso a las bases de datos MySQL configuradas

### Pasos para ejecutar:

1. **Crear la red de Docker:**
```bash
docker network create red_proyectof
```

2. **Ejecutar el sistema:**
```bash
docker-compose up --build
```

3. **Acceder al sistema:**
   - Abrir navegador web
   - Ir a: `http://localhost:8080`

## 🔧 Tecnologías Utilizadas

- **Python 3**: Lenguaje de programación principal
- **Flask**: Framework web para crear las páginas y funcionalidades
- **MySQL**: Base de datos para almacenar información
- **Docker**: Para empaquetar y ejecutar el sistema
- **NGINX**: Servidor web y balanceador de carga
- **HTML/CSS**: Para las páginas web que ven los usuarios

## 🌟 Ventajas de esta Arquitectura

1. **Alta disponibilidad**: Si un servidor falla, los otros siguen funcionando
2. **Escalabilidad**: Se pueden agregar más servidores fácilmente
3. **Distribución de carga**: Las peticiones se reparten entre servidores
4. **Mantenimiento**: Se puede actualizar un servidor sin afectar el servicio
5. **Aislamiento**: Cada componente funciona independientemente

## 📁 Estructura del Proyecto

```
Proyecto_Final_Dist/
├── docker-compose.yml           # Configuración de todos los contenedores
├── nginx.conf                   # Configuración del balanceador de carga
├── README.md                    # Documentación del proyecto
├── init/                        # Scripts de inicialización de las bases de datos
│   ├── esclavo_replicacion.sql
│   ├── init_replication.sql
│   ├── productos.sql
│   └── usuarios.sql
├── mysql/                       # Configuración de MySQL maestro y esclavo
│   ├── esclavo/
│   │   └── esclavo.cnf
│   └── maestro/
│       └── maestro.cnf
├── servidor1/                   # Primera instancia del servidor
│   ├── app.py                   # Código principal de la aplicación
│   ├── Dockerfile               # Instrucciones para crear el contenedor
│   ├── requirements.txt         # Librerías de Python necesarias
│   └── templates/               # Páginas web HTML
│       ├── actualizar_producto.html
│       ├── home.html
│       ├── login.html
│       ├── registro_producto.html
│       └── registro_usuario.html
├── servidor2/                   # Segunda instancia (idéntica a servidor1)
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
│       ├── actualizar_producto.html
│       ├── home.html
│       ├── login.html
│       ├── registro_producto.html
│       └── registro_usuario.html
├── servidor3/                   # Tercera instancia (idéntica a servidor1)
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
│       ├── actualizar_producto.html
│       ├── home.html
│       ├── login.html
│       ├── registro_producto.html
│       └── registro_usuario.html
```

## 🔍 ¿Cómo funciona el balanceador?

1. **Usuario**: Escribe `localhost:8080` en su navegador
2. **NGINX**: Recibe la petición en el puerto 8080
3. **Decisión**: Elige uno de los 3 servidores disponibles
4. **Redirección**: Envía la petición al servidor elegido
5. **Respuesta**: El servidor procesa y devuelve la página web
6. **Usuario**: Ve la página en su navegador