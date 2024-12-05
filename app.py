import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from os import getenv
from dotenv import load_dotenv
from db import db, init_db
from models.usuario import Usuario
from models.producto import Producto
from models.ingrediente import Ingrediente
from models.heladeria import Heladeria
from controllers.producto_controller import producto_bp, producto_bp_api
from controllers.heladeria_controller import heladeria_bp, heladeria_bp_api
from controllers.ingrediente_controller import ingrediente_bp, ingrediente_bp_api
import secrets

load_dotenv()

app = Flask(__name__, template_folder='views')
login_manager = LoginManager(app)
login_manager.login_view = 'no_autorizado'

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_STRING_CONNECTION')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
print(getenv('DB_STRING_CONNECTION'))
db.init_app(app)
# init_db(app)

def cargar_datos():

    usuario1 = Usuario(username = 'martin', password = '123', es_admin=True)
    usuario2 = Usuario(username = 'juan',  password = '456', es_empleado=True)
    usuario3 = Usuario(username = 'pepes',  password = '789')

    #Creando la heladeria
    heladeria = Heladeria('Heladería Don Juan')

    #Creando los productos
    samurai_de_fresas = Producto(nombre="Samurai de fresas", precio_publico=4900, tipo_vaso="Vaso de plástico", volumen=None, tipo='copa',)
    samurai_de_mandarinas = Producto(nombre="Samurai de mandarinas", precio_publico=2500, tipo_vaso="Vaso de vidrio", volumen=None, tipo='copa')
    malteada_choco_espacial = Producto(nombre="Malteda chocoespacial", precio_publico=11000, tipo_vaso=None, volumen=300.0, tipo='malteada')
    cupi_helado = Producto("Cupihelado", 3200, "Vaso de plástico", tipo='copa', volumen=None)

    #Creando los ingredientes
    helado_de_fresa = Ingrediente(nombre="Helado de Fresa",precio=1200, calorias=15, inventario=5.0, es_vegetariano=False, sabor="Fresa", tipo='base')
    helado_de_mandarina = Ingrediente(nombre="Helado de mandarina", precio=1000, calorias=100, inventario=10.0, es_vegetariano=False, sabor="Mandarina", tipo='base')
    chispas_de_chocolate = Ingrediente(nombre="Chispas de chocolate", precio=500, calorias=40, inventario=3.0, es_vegetariano=False, sabor="Chocolate", tipo='base')
    mani_japones = Ingrediente(nombre="Mani Japonés", precio=900, calorias=2, inventario=15.0, es_vegetariano=True, tipo='complemento')
    crema_de_leche = Ingrediente(nombre="Crema de leche", precio=1000, calorias=20, inventario=1.0, es_vegetariano=False, tipo='complemento')
    chispitas = Ingrediente(nombre="Chispitas", precio=100, calorias=2, inventario=5.0, es_vegetariano=False, tipo='complemento')

    #Asociando ingredientes a los productos
    samurai_de_fresas.ingredientes.append(helado_de_fresa)
    samurai_de_fresas.ingredientes.append(chispas_de_chocolate)
    samurai_de_fresas.ingredientes.append(mani_japones)

    samurai_de_mandarinas.ingredientes.append(helado_de_mandarina)
    samurai_de_mandarinas.ingredientes.append(chispas_de_chocolate)
    samurai_de_mandarinas.ingredientes.append(mani_japones)

    malteada_choco_espacial.ingredientes.append(helado_de_fresa)
    malteada_choco_espacial.ingredientes.append(crema_de_leche)
    malteada_choco_espacial.ingredientes.append(chispas_de_chocolate)

    cupi_helado.ingredientes.append(helado_de_mandarina)
    cupi_helado.ingredientes.append(chispas_de_chocolate)
    cupi_helado.ingredientes.append(chispitas)

    #Asociando ingredientes a la heladeria
    heladeria.ingredientes.append(helado_de_fresa)
    heladeria.ingredientes.append(helado_de_mandarina)
    heladeria.ingredientes.append(chispas_de_chocolate)
    heladeria.ingredientes.append(mani_japones)
    heladeria.ingredientes.append(crema_de_leche)

    #Asociando productos a la heladeria
    heladeria.productos.append(samurai_de_fresas)
    heladeria.productos.append(samurai_de_mandarinas)
    heladeria.productos.append(malteada_choco_espacial)
    heladeria.productos.append(cupi_helado)

    #Commit
    db.session.add_all([usuario1, usuario2, usuario3])
    db.session.add(heladeria)
    db.session.add_all([samurai_de_fresas, samurai_de_mandarinas, malteada_choco_espacial, cupi_helado]) 
    db.session.add_all([helado_de_fresa,helado_de_mandarina , chispas_de_chocolate, mani_japones, crema_de_leche, chispitas])
    # db.session.add(producto2)
    db.session.commit()

    #print(producto.calcular_calorias())

@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(id_usuario)

@app.route('/')
def index():
    #Descomentar estas dos líneas de código para crear la bd y cargar los datos, comentarlas si ya se cargó la info
    # init_db(app)
    # cargar_datos()


    heladeria = Heladeria.query.get(1)

    return render_template('index.html', heladeria=heladeria)

    # if current_user.is_authenticated:
    #     return redirect(url_for('perfil'))
    # return render_template('login.html')


@app.route('/login', methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('perfil'))
    
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['usuario']
        password = request.form['contrasena']
        usuario = Usuario(username=username, password=password)
        if usuario.validar_usuario():
            if usuario.validar_pass():
                login_user(usuario.validar_pass())
                return redirect(url_for('perfil'))
            else:
                flash('Contraseña incorrecta')
        else:
            flash('Usuario no encontrado')
        return render_template('login.html')
    
@app.route('/no_autorizado')
def no_autorizado():
    return render_template('no_autorizado.html')

# @app.route('/home')
# @login_required
# def home():

#     # init_db(app)
#     # cargar_datos()

#     heladeria = Heladeria.query.get(1)
#     producto_rentable = heladeria.producto_mas_rentable()
#     print(producto_rentable)

#     return render_template('index.html', heladeria=heladeria, producto_rentable=producto_rentable)

@app.route('/perfil')
@login_required
def perfil():
    nombre = current_user.username
    return render_template('perfil.html', nombre=nombre)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


app.register_blueprint(producto_bp)
app.register_blueprint(heladeria_bp)
app.register_blueprint(ingrediente_bp)
app.register_blueprint(producto_bp_api)
app.register_blueprint(ingrediente_bp_api)
app.register_blueprint(heladeria_bp_api)

if __name__ == '__main__':
    app.run(debug=True)
