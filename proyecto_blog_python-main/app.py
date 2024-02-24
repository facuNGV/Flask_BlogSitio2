
import traceback
from datetime import datetime
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for

# Base de datos
from flask_sqlalchemy import SQLAlchemy

# Crear el server Flask
app = Flask(__name__)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

# Asociamos nuestro controlador de la base de datos con la aplicacion
db = SQLAlchemy()
db.init_app(app)


# ------------ Base de datos ----------------- #
class Posteos(db.Model):
    __tablename__ = "posteos"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String)
    titulo = db.Column(db.String)
    texto = db.Column(db.String)
    fecha = db.Column(db.DateTime)


# ------------ Endpoints Frontend ----------------- #
# Ruta que se ingresa por la ULR 127.0.0.1:5000
@app.route("/")
def index():
    try:
        return render_template('blog.html')
    except:
        # En caso de falla, retornar el mensaje de error
        return jsonify({'trace': traceback.format_exc()})


@app.route("/login")
def login():
    try:
        return render_template('login.html')
    except:
        # En caso de falla, retornar el mensaje de error
        return jsonify({'trace': traceback.format_exc()})


# ------------ Endpoints Backend ----------------- #

@app.route("/posteos/<usuario>", methods=['GET', 'POST'])
def post(usuario):
    if request.method == 'GET':

        try:

            datos = []

            # implementar aquí su código...
            query = db.session.query(Posteos).filter(Posteos.usuario == usuario)

            query=query.order_by(Posteos.fecha.desc())

            query=query.limit(3)

            for posteo in query:
                query_result = {}
                query_result["titulo"]=posteo.titulo
                query_result["texto"]=posteo.texto
                query_result["fecha"]=posteo.fecha.strftime("%Y-%m-%d %H:%M:%S.%f")
                datos.append(query_result)

                # Renderizar el temaplate HTML agregar.html
            return jsonify(datos)
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
            # Alumno:
            # Obtener del HTTP POST del formulario (request.form)
            # la categoria (en minisculas) y el gasto
            usuario = usuario
            titulo= str(request.form.get('titulo')).lower()
            texto= str(request.form.get('texto')).lower()

            if(titulo is None or texto is None):
            # Datos ingresados incorrectos
                return Response(status=400)

            fecha = datetime.now()
            # Alumno
            # Crear un nuevo registro de gastos utilizando
            # los datos capturados (fecha, categoria, gasto)
            # para crear una nueva entrada ne la base de datos
            posteos = Posteos(usuario= usuario, titulo= titulo, texto= texto, fecha=fecha)

            db.session.add(posteos)
            db.session.commit()


            # Como respuesta al POST devolvemos la tabla de valores
            return Response(status=201)
        except:
            return jsonify({'trace': traceback.format_exc()})


# Este método se ejecutará la primera vez
# cuando se construye la app.
with app.app_context():
    # Crear aquí la base de datos
    db.create_all()
    print("Base de datos generada")


if __name__ == "__main__":

    app.run(host="127.0.0.1", port=5000)