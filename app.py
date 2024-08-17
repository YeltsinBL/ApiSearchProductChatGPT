"""Archivo Principal"""
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv()

app = Flask(__name__)
app.config["MYSQL_USER"] = os.environ['MYSQL_USER']
app.config["MYSQL_PASSWORD"] = os.environ['MYSQL_PASSWORD']
app.config["MYSQL_HOST "] = os.environ['MYSQL_HOST']
app.config["MYSQL_PORT "] = os.environ['MYSQL_PORT']
app.config["MYSQL_DB"] = os.environ['MYSQL_DATABASE']
app.config["MYSQL_CURSORCLASS"] = os.environ['MYSQL_CURSORCLASS']

mysql=MySQL(app)


# @app.route('/', methods=['GET'])
# def home():
#     """Principal"""
#     return jsonify(productos)
@app.route('/category', methods=['GET'])
def category():
    """Categoria"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""select id, nombre from ecommerce.categorias""")
        result = cur.fetchall()
        categoria=[]
        for fila in result:
            categoria.append(fila)
            print(fila)
        return jsonify(categoria)
    except Exception as ex:
        return "Error"
@app.route('/brand', methods=['GET'])
def brand():
    """Marca"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""select id, nombre from ecommerce.marcas""")
        result = cur.fetchall()
        marca=[]
        for fila in result:
            marca.append(fila)
            print(fila)
        return jsonify(marca)
    except Exception as ex:
        return "Error"
@app.route('/product', methods=['GET'])
def products():
    """Principal"""
    try:
        add_where =""
        if request.args:
            print(request.args)
            # add_where="where "
            if request.args.get('nombre'):
                add_where += "where nombre like '%{0}%' ".format(request.args.get('nombre'))
            if request.args.get('precio_min'):
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "precio>={0} ".format(float(request.args.get('precio_min')))
            if request.args.get('precio_max'):
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "precio<{0} ".format(float(request.args.get('precio_max')))
            if request.args.get('categoria_id'):
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "categoria_id={0} ".format(int(request.args.get('categoria_id')))
            if request.args.get('marca_id'):
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "marca_id={0} ".format(int(request.args.get('marca_id')))
            if request.args.get('en_oferta') and request.args.get('en_oferta')=='true':
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "en_oferta=1 "
                add_where += "and descuento>0 "
            if request.args.get('popularidad'):
                add_where += "order by popularidad desc"
                #print(request.args.get('popularidad'))
        cur = mysql.connection.cursor()
        sql_consulta ="""select id, nombre, descripcion, precio, stock, en_oferta,\
                descuento, popularidad from ecommerce.productos """+add_where
        print(sql_consulta)
        cur.execute(sql_consulta)
        result = cur.fetchall()
        productos=[]
        for fila in result:
            productos.append(fila)
            #print(fila)
        return jsonify(productos)
    except Exception as ex:
        return "Error"

@app.route('/product/<productId>', methods=['GET'])
def product_by_id(productId):
    """Principal"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""select id, nombre, descripcion, precio, stock, en_oferta, descuento, popularidad\
                     from ecommerce.productos where id='{0}'""".format(int(productId)))
        result = cur.fetchall()
        # print(result)
        producto={}
        for fila in result:
            producto=fila
            print(producto)
        return jsonify(producto)
    except Exception as ex:
        return "Error"

def pagina_no_encontrada(error):
    """Página"""
    # return jsonify({"error":404, "mensaje":"Ruta no encontrada"})
    return "<h1>Página no encontrada</h1>"

# Configurar Swagger
SWAGGER_URL = ''
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={ 
        'app_name': "Api Ecommerce Search Products"
    }
)
app.register_blueprint(swaggerui_blueprint)

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
