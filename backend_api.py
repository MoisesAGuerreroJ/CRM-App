from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://crm_user:4en14Q1w2e3r4t5*@mysql-server/crm_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Cliente(db.Model):
    __tablename__ = 'clientes'
    numero_documento = db.Column(db.String(20), primary_key=True)
    tipo_documento = db.Column(db.String(5), nullable=False)
    nombre_completo = db.Column(db.String(100), nullable=False)
    departamento_id = db.Column(db.Integer, nullable=False)
    ciudad_id = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    horario = db.Column(db.String(10))
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
    relacion_cliente = db.Column(db.String(50))
    credito = db.Column(db.String(5))
    informacion_personal = db.Column(db.String(200))
    trabajo = db.Column(db.String(10))
    vivienda = db.Column(db.String(10))
    conoce_royal = db.Column(db.String(5))
    cliente_id = db.Column(db.String(20), db.ForeignKey('clientes.numero_documento'), nullable=False)

# Validation function
def validate_fields(data, required_fields):
    errors = []
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Field '{field}' is required.")
    return errors

# Routes
@app.route('/clientes', methods=['POST'])
def add_cliente():
    data = request.json
    required_fields = ['numero_documento', 'tipo_documento', 'nombre_completo', 'departamento_id', 'ciudad_id', 'telefono', 'promotor']
    errors = validate_fields(data, required_fields)

    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    try:
        cliente = Cliente(**data)
        db.session.add(cliente)
        db.session.commit()
        return jsonify({"status": "success", "message": "Cliente added successfully!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Cliente with this document already exists."}), 400

@app.route('/clientes/<string:numero_documento>', methods=['GET'])
def get_cliente(numero_documento):
    cliente = Cliente.query.filter_by(numero_documento=numero_documento).first()
    if not cliente:
        return jsonify({"status": "error", "message": "Cliente not found."}), 404

    referidos = Referido.query.filter_by(cliente_id=numero_documento).all()
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
            "numero_documento": cliente.numero_documento,
            "tipo_documento": cliente.tipo_documento,
            "nombre_completo": cliente.nombre_completo,
            "departamento_id": cliente.departamento_id,
            "ciudad_id": cliente.ciudad_id,
            "telefono": cliente.telefono,
            "horario": cliente.horario,
            "promotor": cliente.promotor,
            "telefono_promotor": cliente.telefono_promotor,
            "fecha_inicio": cliente.fecha_inicio,
            "fecha_vencimiento": cliente.fecha_vencimiento,
            "referidos": referidos_list
        }
    }), 200

@app.route('/clientes/<string:numero_documento>', methods=['DELETE'])
def delete_cliente(numero_documento):
    cliente = Cliente.query.filter_by(numero_documento=numero_documento).first()
    if not cliente:
        return jsonify({"status": "error", "message": "Cliente not found."}), 404

    Referido.query.filter_by(cliente_id=numero_documento).delete()
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"status": "success", "message": "Cliente and related referidos deleted successfully."}), 200

@app.route('/referidos', methods=['POST'])
def add_referido():
    data = request.json
    required_fields = ['nombre', 'telefono', 'departamento_id', 'ciudad_id', 'cliente_id']
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
        db.create_all()      # Crea las tablas en la base de datos
        print("Tablas creadas correctamente.")
    app.run(host='crm-backend-server', port=5000,debug=True)