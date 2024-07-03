import pymysql
import os
from dotenv import load_dotenv
import pymysql.cursors
load_dotenv()

# La conexión a la base de datos de artículos
def dame_conexion():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'))

    
# La conexión a la base de datos de artículos, esta necesita el cursorclass pymysql.cursors.DictCursor
# porque sino no funciona la asociación con session['id']
def dame_conexion_usuarios():
    host = os.getenv('DB_HOST')
    usr = os.getenv('DB_USERNAME')
    passw = os.getenv('DB_PASSWORD')
    db = os.getenv('DB_NAME')
    return pymysql.connect(
        host=host,
        user=usr,
        password=passw,
        db=db,
        cursorclass=pymysql.cursors.DictCursor)


def insertar_articulo(nombre, precio):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO articulos(nombre,precio) VALUES (%s, %s)", (nombre, precio))
        conexion.commit()
        conexion.close()


def listar_articulos():
    conexion = dame_conexion()
    articulos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, precio FROM articulos")
        articulos = cursor.fetchall()
        conexion.close()
        return articulos
    

def eliminar_articulo(id):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM articulos WHERE id = %s", (id))
        conexion.commit()
        conexion.close()


def obtener_articulo(id):
    conexion = dame_conexion()
    articulos = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, precio FROM articulos WHERE id = %s", (id))
        articulos = cursor.fetchone()
        conexion.close()
        return articulos


def actualizar_articulo(id, nombre, precio):
    conexion = dame_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE articulos SET nombre = %s, precio = %s WHERE id = %s",(nombre, precio, id))
        conexion.commit()
        conexion.close()

        
def iniciar_sesion(username, password):
    conexion = dame_conexion_usuarios()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT * FROM teatro_arg WHERE Email = % s AND Password = % s', (username, password, ))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario

    
def buscar_cuenta(email):
    conexion = dame_conexion_usuarios()
    with conexion.cursor() as cursor:
        cursor.execute('SELECT * FROM teatro_arg WHERE Email = % s', (email, ))
        usuario = cursor.fetchone()
        conexion.close()
        return usuario

    
def crear_usuario(nombre, apellido, dni, email, password):
        conexion = dame_conexion_usuarios()
        with conexion.cursor() as cursor:
            cursor.execute('INSERT INTO teatro_arg VALUES (NULL, % s, % s, % s, % s, % s)', (nombre, apellido, dni, email, password ))
            conexion.commit()
            conexion.close()


if __name__ == '__main__':
    #dame_conexion()
    articulos = listar_articulos()
    print(articulos)
