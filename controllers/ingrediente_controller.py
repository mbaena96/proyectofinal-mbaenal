from models.ingrediente import Ingrediente
from flask import Blueprint, render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from db import db
import urllib

ingrediente_bp = Blueprint('ingrediente_bp', __name__, url_prefix='/ingrediente')
ingrediente_bp_api = Blueprint('ingrediente_bp_api', __name__, url_prefix='/api/ingredientes')

@ingrediente_bp.route('/<int:id>')
@login_required
def mostrar_ingredientes(id):
    if current_user.es_admin or current_user.es_empleado:
        ingrediente = Ingrediente.query.get(id)
        es_sano = ingrediente.es_sano()
        return render_template('ingrediente.html', ingrediente=ingrediente, es_sano=es_sano)
    else:
        return redirect(url_for('no_autorizado'))

@ingrediente_bp.route('renovar_ingrediente/<int:id>')
@login_required
def renovar_ingrediente(id):
    if current_user.es_admin or current_user.es_empleado:
        ingrediente = Ingrediente.query.get(id)
        ingrediente.renovar_inventario()
        db.session.commit()
        flash(f'Inventario de {ingrediente.nombre} renovado')
        return redirect(url_for('ingrediente_bp.mostrar_ingredientes', id=ingrediente.id))
    
    return redirect(url_for('no_autorizado'))

@ingrediente_bp.route('abastecer_ingrediente/<int:id>')
@login_required
def abastecer_ingrediente(id):
    if current_user.es_admin or current_user.es_empleado:
        ingrediente = Ingrediente.query.get(id)
        ingrediente.abastecer()
        db.session.commit()
        flash(f'{ingrediente.nombre} abastecido')
        return redirect(url_for('ingrediente_bp.mostrar_ingredientes', id=ingrediente.id))
    
    return redirect(url_for('no_autorizado'))

#API

@ingrediente_bp_api.route('/')
def api_listar_ingredientes():
    ingredientes = Ingrediente.query.all()
    return jsonify(data = [ingrediente.show() for ingrediente in ingredientes])

@ingrediente_bp_api.route('/<int:id>')
def api_listar_ingredientes_id(id):
    ingrediente = Ingrediente.query.get(id)
    return jsonify(data = ingrediente.show())
    
@ingrediente_bp_api.route('/<string:nombre>')
def api_listar_ingredientes_nombre(nombre):
    nombre = urllib.parse.unquote(nombre)
    ingrediente = Ingrediente.query.filter_by(nombre=nombre).first()
    return jsonify(data = ingrediente.show())

@ingrediente_bp_api.route('/<int:id>/es_sano')
def api_listar_ingredientes_id_es_sano(id):
    ingrediente = Ingrediente.query.get(id)
    return jsonify(data = ingrediente.es_sano())