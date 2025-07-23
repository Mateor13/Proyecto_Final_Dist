from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
import os
import logging
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configuración de la aplicación Flask
app = Flask(__name__)
# Cargar las variables de entorno desde un archivo .env
app.secret_key = os.getenv("FLASK_SECRET_KEY", "clave_predeterminada_insegura")

# Configuración del logger (El logger se utiliza para registrar eventos y errores)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la conexión a la base de datos
def obtener_conexion_usuarios():
    """Se establece la conexión a la base de datos MySQL."""
    try:
        connection = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_USUARIOS"),
            port = int(os.getenv("DB_PORT")),
            charset = 'utf8mb4',
            autocommit=False
        )
        return connection
    except Error as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None

def obtener_conexion_productos():
    """Se establece la conexión a la base de datos MySQL."""
    try:
        connection = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_PRODUCTOS"),
            port = int(os.getenv("DB_PORT")),
            charset = 'utf8mb4',
            autocommit=False
        )
        return connection
    except Error as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None

# Validar datos del registro de productos
def validar_datos_registro_producto(nombre, codigo, descripcion, unidad, categoria):
    """Validar los datos del registro de productos"""
    errores = []
    # Validar campos obligatorios
    if not nombre or not codigo or not descripcion or not unidad or not categoria:
        errores.append("Todos los campos son obligatorios.")
        return errores
    # Validar nombre
    if len(nombre.strip()) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    # Validar código
    if not codigo.isnumeric():
        errores.append("El código debe ser numérico.")
    # Validar descripción
    if len(descripcion.strip()) < 10:
        errores.append("La descripción debe tener al menos 10 caracteres.")
    # Validar unidad
    #Validar que la unidad sea mayor a 0
    if not unidad.isdigit() or int(unidad) <= 0:
        errores.append("La unidad debe ser un número entero positivo.")
    # Validar categoría
    if not categoria.strip():
        errores.append("La categoría es obligatoria.")
    # Siempre retornar lista (vacía si no hay errores)
    return errores

# Validar datos de la actualización de productos (sin validar código)
def validar_datos_actualizacion_producto(nombre, descripcion, unidad, categoria):
    """Validar los datos de la actualización de productos (sin código)"""
    errores = []
    # Validar campos obligatorios
    if not nombre or not descripcion or not unidad or not categoria:
        errores.append("Todos los campos son obligatorios.")
        return errores
    # Validar nombre
    if len(nombre.strip()) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    # Validar descripción
    if len(descripcion.strip()) < 10:
        errores.append("La descripción debe tener al menos 10 caracteres.")
    # Validar unidad
    if not unidad.isdigit() or int(unidad) <= 0:
        errores.append("La unidad debe ser un número entero positivo.")
    # Validar categoría
    if not categoria.strip():
        errores.append("La categoría es obligatoria.")
    # Siempre retornar lista (vacía si no hay errores)
    return errores

# Validar datos del inicio de sesión
def validar_datos_login(email, password):
    """Validar los datos de inicio de sesión"""
    errores = []
    # Validar campos obligatorios
    if not email or not password:
        errores.append("El correo electrónico y la contraseña son obligatorios.")
        return errores
    # Validar email
    if '@' not in email or '.' not in email.split('@')[-1]:
        errores.append("El correo electrónico no es válido.")
    # Validar password
    if len(password) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres.")
    # Siempre retornar lista (vacía si no hay errores)
    return errores

# Validar datos del registro de usuario
def validar_datos_registro_usuario(nombre, email, password, apellido):
    """Validar los datos del registro de usuario"""
    errores = []
    # Validar campos obligatorios
    if not nombre or not email or not password or not apellido:
        errores.append("Todos los campos son obligatorios.")
        return errores
    # Validar nombre
    if len(nombre.strip()) < 3:
        errores.append("El nombre debe tener al menos 3 caracteres.")
    # Validar apellido
    if len(apellido.strip()) < 3:
        errores.append("El apellido debe tener al menos 3 caracteres.")
    # Validar email
    if '@' not in email or '.' not in email.split('@')[-1]:
        errores.append("El correo electrónico no es válido.")
    # Validar password
    if len(password) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres.")
    # Siempre retornar lista (vacía si no hay errores)
    return errores

# Ruta para la página de inicio (login) 
@app.route('/' , methods=['GET', 'POST'])
def login():
    """Ruta para la página de inicio (login)"""
    print("Variables de entorno cargadas:")
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        errores = validar_datos_login(email, password)
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('login.html', email=email)
        
        #Conectar a la base de datos
        conn = obtener_conexion_usuarios()
        if conn is None:
            flash("Error al conectar a la base de datos.", 'error')
            return render_template('login.html', email=email)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, password))
            usuario = cursor.fetchone()
            if usuario:
                print("Usuario encontrado:", usuario)
                flash("Inicio de sesión exitoso.", 'success')
                return redirect(url_for('listar_productos'))
            else:
                flash("Correo electrónico o contraseña incorrectos.", 'error')
                return render_template('login.html', email=email)
        except Error as e:
            logger.error(f"Error al iniciar sesión: {e}")
            flash("Error al iniciar sesión.", 'error')
            return render_template('login.html', email=email)
        finally:
            if conn:
                conn.close()
    else:
        return render_template('login.html')

# Ruta para el registro de usuarios
@app.route('/registro-usuario', methods=['GET', 'POST'])
def registro_usuario():
    """Ruta para el registro de usuarios"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        apellido = request.form.get('apellido', '').strip()

        errores = validar_datos_registro_usuario(nombre, email, password, apellido)
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('registro_usuario.html', nombre=nombre, apellido=apellido, email=email)

        #Conectar a la base de datos
        conn = obtener_conexion_usuarios()
        if conn is None:
            flash("Error al conectar a la base de datos.", 'error')
            return render_template('registro_usuario.html', nombre=nombre, apellido=apellido, email=email)

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if usuario:
                flash("El correo electrónico ya está registrado.", 'error')
                return render_template('registro_usuario.html', nombre=nombre, apellido=apellido, email=email)
            cursor.execute("INSERT INTO usuarios (nombre, email, password, apellido) VALUES (%s, %s, %s, %s)",
                          (nombre, email, password, apellido))
            conn.commit()
            flash("Usuario registrado exitosamente.", 'success')
            return redirect(url_for('login'))
        except Error as e:
            logger.error(f"Error al registrar usuario: {e}")
            flash("Error al registrar usuario.", 'error')
            return render_template('registro_usuario.html', nombre=nombre, apellido=apellido, email=email)
        finally:
            if conn:
                conn.close()
    return render_template('registro_usuario.html')
       
#Ruta para buscar productos
@app.route('/buscar-productos', methods=['GET', 'POST'])
def buscar_productos():
    """Ruta para buscar productos"""
    if request.method == 'POST':
        codigo = request.form.get('codigo', '').strip()

        #Conectar a la base de datos
        conn = obtener_conexion_productos()
        if conn is None:
            flash("Error al conectar a la base de datos.", 'error')
            return render_template('home.html', codigo=codigo)

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM productos WHERE 1=1"
            params = []
            if codigo:
                query += " AND codigo = %s"
                params.append(codigo)
            cursor.execute(query, tuple(params))
            productos = cursor.fetchall()
            return render_template('home.html', productos=productos, codigo=codigo)
        except Error as e:
            logger.error(f"Error al buscar productos: {e}")
            flash("Error al buscar productos.", 'error')
            return render_template('home.html', codigo=codigo)
        finally:
            if conn:
                conn.close()

# Ruta para listar productos
@app.route('/home', methods=['GET'])
def listar_productos():
    """Ruta para listar productos"""
    #Conectar a la base de datos
    
    conn = obtener_conexion_productos()
    if conn is None:
        flash("Error al conectar a la base de datos.", 'error')
        return render_template('home.html')

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        return render_template('home.html', productos=productos)
    except Error as e:
        logger.error(f"Error al listar productos: {e}")
        flash("Error al listar productos.", 'error')
        return render_template('home.html')
    finally:
        if conn:
            conn.close()
    

@app.route('/registro-producto', methods=['GET', 'POST'])
def registro_producto():
    """Ruta para registro de productos"""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        codigo = request.form.get('codigo', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        unidad = request.form.get('unidad', '').strip()
        categoria = request.form.get('categoria', '').strip()

        errores = validar_datos_registro_producto(nombre, codigo, descripcion, unidad, categoria)
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('registro_producto.html',
                                   nombre=nombre, 
                                   codigo=codigo,
                                   descripcion=descripcion, 
                                   unidad=unidad,
                                   categoria=categoria)
        
        #Conectar a la base de datos
        conn = obtener_conexion_productos()
        if conn is None:
            flash("Error al conectar a la base de datos.", 'error')
            return render_template('registro_producto.html',
                                   nombre=nombre, 
                                   codigo=codigo,
                                   descripcion=descripcion, 
                                   unidad=unidad,
                                   categoria=categoria)
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
            producto = cursor.fetchone()
            if producto:
                flash("El código de producto ya existe.", 'error')
                return render_template('registro_producto.html',
                                       nombre=nombre, 
                                       codigo=codigo,
                                       descripcion=descripcion, 
                                       unidad=unidad,
                                       categoria=categoria)
            cursor.execute("INSERT INTO productos (nombre, codigo, descripcion, unidad, categoria) VALUES (%s, %s, %s, %s, %s)",
                          (nombre, codigo, descripcion, unidad, categoria))
            conn.commit()
            flash("Producto registrado exitosamente.", 'success')
            return redirect(url_for('listar_productos'))
        except Error as e:
            logger.error(f"Error al registrar producto: {e}")
            flash("Error al registrar producto.", 'error')
            return render_template('registro_producto.html',
                                   nombre=nombre, 
                                   codigo=codigo,
                                   descripcion=descripcion, 
                                   unidad=unidad,
                                   categoria=categoria)
        finally:
            if conn:
                conn.close()
    return render_template('registro_producto.html')

@app.route('/actualizar-producto/<codigo>', methods=['GET', 'POST'])
def actualizar_producto(codigo):
    """Ruta para actualizar productos (sin modificar el código)"""
    #Conectar a la base de datos
    conn = obtener_conexion_productos()
    if conn is None:
        flash("Error al conectar a la base de datos.", 'error')
        return redirect(url_for('listar_productos'))
    
    try:
        cursor = conn.cursor()
        
        if request.method == 'GET':
            # Obtener los datos actuales del producto por código
            cursor.execute("SELECT codigo, nombre, descripcion, unidad, categoria FROM productos WHERE codigo = %s", (codigo,))
            producto = cursor.fetchone()
            if not producto:
                flash("Producto no encontrado.", 'error')
                return redirect(url_for('listar_productos'))
            
            # Convertir la tupla a diccionario para facilitar el acceso
            producto_dict = {
                'codigo': producto[0],
                'nombre': producto[1],
                'descripcion': producto[2],
                'unidad': producto[3],
                'categoria': producto[4]
            }
            return render_template('actualizar_producto.html', producto=producto_dict)
        
        elif request.method == 'POST':
            # Procesar la actualización (sin código - el código NO se recibe del formulario)
            nombre = request.form.get('nombre', '').strip()
            descripcion = request.form.get('descripcion', '').strip()
            unidad = request.form.get('unidad', '').strip()
            categoria = request.form.get('categoria', '').strip()
            
            # Validar los datos usando la función específica para actualización (sin código)
            errores = validar_datos_actualizacion_producto(nombre, descripcion, unidad, categoria)
            if errores:
                for error in errores:
                    flash(error, 'error')
                producto_dict = {
                    'codigo': codigo,
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'unidad': unidad,
                    'categoria': categoria
                }
                return render_template('actualizar_producto.html', producto=producto_dict)
            
            # Actualizar el producto (SOLO los campos permitidos - SIN código)
            cursor.execute("""
                UPDATE productos 
                SET nombre = %s, descripcion = %s, unidad = %s, categoria = %s 
                WHERE codigo = %s
            """, (nombre, descripcion, unidad, categoria, codigo))
            conn.commit()
            
            flash("Producto actualizado exitosamente.", 'success')
            return redirect(url_for('listar_productos'))
            
    except Error as e:
        logger.error(f"Error al actualizar producto: {e}")
        flash("Error al actualizar producto.", 'error')
        return redirect(url_for('listar_productos'))
    finally:
        if conn:
            conn.close()

@app.route('/eliminar-producto/<codigo>',  methods=['GET', 'POST'])
def eliminar_producto(codigo):
    """Ruta para eliminar productos con confirmación"""
    conn = obtener_conexion_productos()
    if conn is None:
        flash("Error al conectar a la base de datos.", 'error')
        return redirect(url_for('listar_productos'))

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))
        conn.commit()
        flash("Producto eliminado exitosamente.", 'success')
    except Error as e:
        logger.error(f"Error al eliminar producto: {e}")
        flash("Error al eliminar el producto.", 'error')
    finally:
        if conn:
            conn.close()
    return redirect(url_for('listar_productos'))

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)