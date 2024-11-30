from models.heladeria import Heladeria
from models.producto import Producto
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from db import db

heladeria_bp = Blueprint('heladeria_bp',__name__, url_prefix='/vender')
heladeria_bp_api = Blueprint('heladeria_bp_api',__name__, url_prefix='/api/vender')

@heladeria_bp.route('/', methods=["GET", "POST"])
@login_required
def vender():
    if request.method == 'GET':
        productos = Producto.query.all()
        return render_template('venta.html', productos = productos)
    else:
        response = request.form['producto']
        # producto_vender = Producto.query.filter_by(nombre=response).first()
        heladeria = Heladeria.query.filter_by(id=1).first()

        try:
            if heladeria.vender(response):
                db.session.commit()
                flash(f'{response} vendido con éxito')
        except ValueError as error:
            flash(str(error))
            # print (error)
        
        return redirect(url_for('heladeria_bp.vender'))
    
@heladeria_bp.route('/rentable')
@login_required
def producto_rentable():
    if current_user.es_admin:
        heladeria = Heladeria.query.get(1)
        venta_dia = heladeria.venta_dia
        producto_rentable = heladeria.producto_mas_rentable()
        rentabilidad = Producto.query.filter_by(nombre=producto_rentable).first().calcular_rentabilidad()
        return render_template('producto_rentable.html', producto_rentable=producto_rentable, rentabilidad=rentabilidad, venta_dia=venta_dia)
    else:
        return redirect(url_for('no_autorizado'))
    
#API
@heladeria_bp_api.route('/<int:id>')
def vender_id(id):
    heladeria = Heladeria.query.get(1)
    try:
        producto = Producto.query.get(id)
        resultado = heladeria.vender(producto.nombre)
        if resultado:
            db.session.commit()
            return jsonify(data = resultado)
        return jsonify(data = False)
    except Exception as e:
        return jsonify(data = str(e))