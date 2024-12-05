from models.producto import Producto
from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from db import db
import urllib

producto_bp = Blueprint('producto_bp',__name__, url_prefix='/productos')
producto_bp_api = Blueprint('producto_bp_api',__name__, url_prefix='/api/productos')

@producto_bp.route('/lista')
def listar_productos():
    productos = Producto.query.all()
    return render_template('consultar_productos.html', productos = productos)

@producto_bp.route('/detalle/<int:id>')
@login_required
def detalle_producto(id):

    if current_user.es_admin:
        producto = Producto.query.get(id)
        calorias = producto.calcular_calorias()
        costo = producto.calcular_costo()
        rentabilidad = producto.calcular_rentabilidad()
        return render_template('detalle_producto.html', producto=producto, calorias=calorias, costo=costo, rentabilidad=rentabilidad)
    else:
        # producto = db.session.query(Producto.nombre).filter_by(id=id).first()
        producto = Producto.query.get(id)
        calorias = producto.calcular_calorias()
        return render_template('detalle_producto.html', producto=producto, calorias=calorias)

@producto_bp.route('renovar_producto/<int:id>')
@login_required
def renovar_producto(id):
    if current_user.es_admin or current_user.es_empleado:
        producto = Producto.query.get(id)
        for ingrediente in producto.ingredientes:
            ingrediente.renovar_inventario()

        db.session.commit()
        flash(f'Inventario de {producto.nombre} renovado')
        return redirect(url_for('producto_bp.listar_productos'))

    return redirect(url_for('no_autorizado'))

@producto_bp.route('abastecer_producto/<int:id>')
@login_required
def abastecer_producto(id):
    if current_user.es_admin or current_user.es_empleado:
        producto = Producto.query.get(id)
        for ingrediente in producto.ingredientes:
            ingrediente.abastecer()

        db.session.commit()
        flash(f'ingredientes de {producto.nombre} abastecidos')
        return redirect(url_for('producto_bp.listar_productos'))
    
    return redirect(url_for('no_autorizado'))

#API

@producto_bp_api.route('/')
def api_listar_productos():
    productos = Producto.query.all()
    return jsonify(data = [producto.show() for producto in productos])

@producto_bp_api.route('/<int:id>')
def api_listar_producto_id(id):
    try:
        producto = Producto.query.get(id)
        return jsonify(data = producto.show())
    except Exception as e:
        return jsonify(data = str(e))

@producto_bp_api.route('/<string:nombre>')
def api_listar_producto_nombre(nombre):
    try:
        nombre = urllib.parse.unquote(nombre)
        # print(nombre)
        producto = Producto.query.filter_by(nombre=nombre).first()
        return jsonify(data = producto.show())
    except Exception as e:
        return jsonify(data = str(e))

@producto_bp_api.route('/<int:id>/calorias')
def api_listar_producto_calorias_id(id):
    producto = Producto.query.get(id)
    return jsonify(data = producto.calcular_calorias())

@producto_bp_api.route('/<int:id>/rentabilidad')
def api_listar_producto_rentabilidad_id(id):
    producto = Producto.query.get(id)
    return jsonify(data = producto.calcular_rentabilidad())

@producto_bp_api.route('/<int:id>/costo')
def api_listar_producto_costo_id(id):
    producto = Producto.query.get(id)
    return jsonify(data = producto.calcular_costo())

@producto_bp_api.route('/<int:id>/abastecer')
def api_abastecer_producto(id):
    producto = Producto.query.get(id)
    for ingrediente in producto.ingredientes:
        ingrediente.abastecer()

    db.session.commit()
    return jsonify(data = 'Proceso realizado con exito')

@producto_bp_api.route('/<int:id>/renovar')
def api_renovar_producto(id):
    producto = Producto.query.get(id)
    for ingrediente in producto.ingredientes:
        ingrediente.renovar_inventario()

    db.session.commit()
    return jsonify(data = 'Proceso realizado con exito')