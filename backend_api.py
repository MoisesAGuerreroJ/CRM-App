from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import Identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://crm_user:4en14Q1w2e3r4t5*@mysql-server/crm_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
CORS(app)  # Enable CORS for all routes

db = SQLAlchemy(app)


# Models
class Departamento(db.Model):
    __tablename__ = 'departamentos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)


class Ciudad(db.Model):
    __tablename__ = 'ciudades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_formulario = db.Column(db.Integer, Identity(), primary_key=True)
    numero_documento = db.Column(db.String(20), nullable=False)
    tipo_documento = db.Column(db.String(5), nullable=False)
    nombre_completo = db.Column(db.String(100), nullable=False)
    departamento_id = db.Column(db.Integer, nullable=False)
    ciudad_id = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    horario = db.Column(db.String(10))
    nombre_distribuidor = db.Column(db.String(100))
    telefono_distribuidor = db.Column(db.String(15))
    promotor = db.Column(db.String(100), nullable=False)
    telefono_promotor = db.Column(db.String(15))
    fecha_inicio = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date)


class Referido(db.Model):
    __tablename__ = 'referidos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150))
    telefono = db.Column(db.String(15), nullable=False)
    departamento_id = db.Column(db.Integer, nullable=False)
    ciudad_id = db.Column(db.Integer, nullable=False)
    relacion_cliente = db.Column(db.String(50), nullable=False)
    credito = db.Column(db.String(5))
    informacion_personal = db.Column(db.String(200))
    trabajo = db.Column(db.String(10))
    vivienda = db.Column(db.String(10))
    conoce_royal = db.Column(db.String(5))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id_formulario'), nullable=False)


# Validation function
def validate_fields(data, required_fields):
    errors = []
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Field '{field}' is required.")
    return errors


# Helper function to convert date strings
def parse_date(date_string):
    if date_string:
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            return None
    return None


# Routes
@app.route('/departamentos', methods=['GET'])
def get_departamentos():
    departamentos = Departamento.query.all()
    departamentos_list = [{"id": dept.id, "nombre": dept.nombre} for dept in departamentos]
    return jsonify({"status": "success", "departamentos": departamentos_list})


@app.route('/ciudades', methods=['GET'])
def get_ciudades():
    ciudades = Ciudad.query.all()
    ciudades_dict = {}
    for city in ciudades:
        if city.departamento_id not in ciudades_dict:
            ciudades_dict[city.departamento_id] = []
        ciudades_dict[city.departamento_id].append({"id": city.id, "nombre": city.nombre})
    return jsonify({"status": "success", "ciudades": ciudades_dict})

@app.route('/form_number', methods=['GET'])
def get_form_number():
    # Get the last inserted id_formulario
    last_cliente = Cliente.query.order_by(Cliente.id_formulario.desc()).first()

    if last_cliente:
       next_form_number = last_cliente.id_formulario + 1
    else:
        next_form_number = 1
    return jsonify({"status": "success", "form_number": next_form_number})


@app.route('/clientes', methods=['POST'])
def add_cliente():
    data = request.json
    required_fields = ['numero_documento', 'tipo_documento', 'nombre_completo', 'departamento_id', 'ciudad_id',
                       'telefono', 'promotor', 'id_formulario']
    errors = validate_fields(data, required_fields)

    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    # Parse date strings into date objects
    fecha_inicio = parse_date(data.get('fecha_inicio'))
    fecha_vencimiento = parse_date(data.get('fecha_vencimiento'))

    try:
        cliente = Cliente(
            id_formulario = data['id_formulario'], #Get the form number from frontend
            numero_documento=data['numero_documento'],
            tipo_documento=data['tipo_documento'],
            nombre_completo=data['nombre_completo'],
            departamento_id=data['departamento_id'],
            ciudad_id=data['ciudad_id'],
            direccion=data.get('direccion'),
            telefono=data['telefono'],
            horario=data.get('horario'),
            nombre_distribuidor=data.get('nombre_distribuidor'),
            telefono_distribuidor=data.get('telefono_distribuidor'),
            promotor=data['promotor'],
            telefono_promotor=data.get('telefono_promotor'),
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento
        )
        db.session.add(cliente)
        db.session.commit()
        return jsonify({"status": "success", "message": "Cliente added successfully!", "id_formulario": cliente.id_formulario}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Cliente with this document already exists.", "error": str(e)}), 400

@app.route('/clientes/<int:id_formulario>', methods=['GET'])
def get_cliente(id_formulario):
    cliente = Cliente.query.filter_by(id_formulario=id_formulario).first()
    if not cliente:
        return jsonify({"status": "error", "message": "Cliente not found."}), 404

    referidos = Referido.query.filter_by(cliente_id=id_formulario).all()
    referidos_list = [{
        "id": r.id,
        "nombre": r.nombre,
        "direccion": r.direccion,
        "telefono": r.telefono,
        "departamento_id": r.departamento_id,
        "ciudad_id": r.ciudad_id,
        "relacion_cliente": r.relacion_cliente,
        "credito": r.credito,
        "informacion_personal": r.informacion_personal,
        "trabajo": r.trabajo,
        "vivienda": r.vivienda,
        "conoce_royal": r.conoce_royal
    } for r in referidos]

    return jsonify({
        "status": "success",
        "cliente": {
            "id_formulario": cliente.id_formulario,
            "numero_documento": cliente.numero_documento,
            "tipo_documento": cliente.tipo_documento,
            "nombre_completo": cliente.nombre_completo,
            "departamento_id": cliente.departamento_id,
            "ciudad_id": cliente.ciudad_id,
            "direccion": cliente.direccion,
            "telefono": cliente.telefono,
            "horario": cliente.horario,
            "nombre_distribuidor": cliente.nombre_distribuidor,
            "telefono_distribuidor": cliente.telefono_distribuidor,
            "promotor": cliente.promotor,
            "telefono_promotor": cliente.telefono_promotor,
            "fecha_inicio": cliente.fecha_inicio,
            "fecha_vencimiento": cliente.fecha_vencimiento,
            "referidos": referidos_list
        }
    }), 200

@app.route('/clientes/<int:id_formulario>', methods=['DELETE'])
def delete_cliente(id_formulario):
    cliente = Cliente.query.filter_by(id_formulario=id_formulario).first()
    if not cliente:
        return jsonify({"status": "error", "message": "Cliente not found."}), 404

    Referido.query.filter_by(cliente_id=id_formulario).delete()
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"status": "success", "message": "Cliente and related referidos deleted successfully."}), 200

@app.route('/referidos', methods=['POST'])
def add_referido():
    data = request.json
    required_fields = ['nombre', 'telefono', 'departamento_id', 'ciudad_id', 'relacion_cliente', 'cliente_id']
    errors = validate_fields(data, required_fields)

    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    try:
        referido = Referido(**data)
        db.session.add(referido)
        db.session.commit()
        return jsonify({"status": "success", "message": "Referido added successfully!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Error adding referido."}), 400

@app.route('/referidos/<int:referido_id>', methods=['DELETE'])
def delete_referido(referido_id):
    referido = Referido.query.filter_by(id=referido_id).first()
    if not referido:
        return jsonify({"status": "error", "message": "Referido not found."}), 404

    db.session.delete(referido)
    db.session.commit()
    return jsonify({"status": "success", "message": "Referido deleted successfully."}), 200


if __name__ == "__main__":
    with app.app_context():  # Establece el contexto de la aplicación
        db.create_all()  # Crea las tablas en la base de datos
        print("Tablas creadas correctamente.")
    app.run(host='crm-backend-server', port=5000, debug=True)