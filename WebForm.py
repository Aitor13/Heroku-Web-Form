from flask import Flask, jsonify, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Hecho el deployment en Heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tcncwrqssasksf:34dd1a83e2c1f46c16647da84db10691f049fe432ddf7c0a9d99c3be110727ac@ec2-34-251-118-151.eu-west-1.compute.amazonaws.com/d2qkutr0arlq2g'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
CORS(app)

db = SQLAlchemy(app)
mm = Marshmallow(app)

class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    calle = db.Column(db.String(50))
    comida = db.Column(db.String(50))
    
    def __init__(self, nombre, calle, comida):
        self.nombre = nombre
        self.calle = calle
        self.comida = comida
        
db.create_all()
        
# con este esquema configuramos los datos a mostrar en la peticiones get
class schema(mm.Schema):
    class Meta:
        fields = ('id','nombre', 'calle', 'comida')  # siempre hay que darle el nombre fields sino no funciona
        
esquema = schema()
esquemas = schema(many=True)

# En index ya cogermos los datos del formulario web en caso de rellenarse
@app.route('/',methods=['POST', 'GET'])
@app.route('/indice', methods=['POST', 'GET'])
def indice():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        calle = request.form['calle']
        comida = request.form['comida']
        restaurante = Restaurante(nombre, calle, comida)
        db.session.add(restaurante)
        db.session.commit()
        mensaje = 'Registro insertado con éxito!'
    return render_template('indice.html',mensaje=mensaje)


if __name__ == '__main__':
    app.run(port=2000)