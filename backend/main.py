import re
from flask import Flask, redirect, url_for, render_template, request, session
import basedatos

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = 'es_necesaria_sino_pincha_la_app'


@app.route('/agregar_articulo')
def agregar_articulo():
    return render_template("agregar_articulo.html")


@app.route('/guardar_articulo', methods=['POST'])
def guardar_articulo():
    nombre = request.form['nombre']
    precio = request.form['precio']
    try:
        basedatos.insertar_articulo(nombre, precio)
    except Exception as e:
        print(f"Ha ocurrido el error {e}")
    finally:
        return redirect('/articulos')


@ app.route('/')
def bienvenida():
    return "Backend 1.0"


@ app.route('/articulos')
def articulos():
    # Este endpoint solo va a listar los artículos si el usuario está logueado
    if session.get('loggedin')==True:
        try:
            articulos = basedatos.listar_articulos()
        except Exception as e:
            print(f"Ha ocurrido el error {e}")
        finally:
            return render_template('articulos.html', articulos=articulos)
    else:
        return "Usuario no logueado"
    

@ app.route("/eliminar_articulo", methods=['POST'])
def eliminar_articulo():
    try:
        basedatos.eliminar_articulo(request.form['id'])
    except Exception as e:
        print(f"Ha ocurrido el error {e}")
    finally:

        return redirect("/articulos")


@ app.route("/editar_articulo/<int:id>")
def editar_articulo(id):
    try:
        articulo = basedatos.obtener_articulo(id)
    except Exception as e:
        print(f"Ha ocurrido el error {e}")
    finally:
        return render_template("editar_articulo.html", articulo=articulo)


@ app.route("/actualizar_articulo", methods=['POST'])
def actualizar_articulo():
    id = request.form["id"]
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    try:
        basedatos.actualizar_articulo(id, nombre, precio)
    except Exception as e:
        print(f"Ha ocurrido el error {e}")
    finally:
        return redirect("/articulos")


@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    # Si el request es un post que trae nombre de usuario y pass los capturo
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        # Busco en la base si existe la cuenta con ese user y pass
        try:
            account=basedatos.iniciar_sesion(username,password) 
        except Exception as e:
                print(f"Ha ocurrido el error {e}")
        
        # Si existe la cuenta creo la sesión y redirijo a profile.html
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['Email']
            session['nombre'] = account['Nombre']
            session['apellido'] = account['Apellido']
            
            msg = 'Usuario logueado!'
            return render_template('profile.html', msg = msg)
        else:
            msg = 'Usuario o password incorrectos !'
    
    return render_template('login.html', msg = msg)


@app.route('/logout')
def logout():
    # Remuevo la info de sesion y redirijo a login.html
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods =['GET', 'POST'])
def register():

    msg = ''

    # Solo trabaja si el request está completo
    if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'dni' in request.form and 'password' in request.form and 'email' in request.form :

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        password = request.form['password']
        dni = request.form['dni']
        email = request.form['email']


        # Chequea que la cuenta a ingresar no exista ya en la BD
        try:
            account = basedatos.buscar_cuenta(email)
        except Exception as e:
            print(f"Ha ocurrido el error {e}")
            

        if account:
            msg = 'Cuenta existente !'

        # Validaciones de los campos
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Email invalido !'

        elif not re.match(r'[A-Za-z]+', nombre):
            msg = 'El nombre debe contener solo caracteres!'

        elif not re.match(r'[A-Za-z]+', apellido):
            msg = 'El apellido debe contener solo caracteres!'

        elif not nombre or not apellido or not password or not email:
            msg = 'Completar todos los campos!'

        else:
            try:
                basedatos.crear_usuario(nombre, apellido, dni, email, password)
            except Exception as e:
                print(f"Ha ocurrido el error {e}")
            finally:
                msg = 'Te registraste exitosamente, ya podes loguearte desde la pantalla de login!'

    elif request.method == 'POST':
        msg = 'Por favor completar todos los campos !'

    return render_template('register.html', msg = msg)


if __name__ == '__main__':

    app.run(debug=True)