"""Archivo Principal"""
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint
from queries import list_categories, list_brand, list_products, search_all_products, get_product_id

load_dotenv()

app = Flask(__name__)

@app.route('/category', methods=['GET'])
def category():
    """Categoria"""
    try:
        result = list_categories()
        categoria=[]
        for fila in result:
            categoria.append(fila)
        return jsonify(categoria)
    except Exception as ex:
        return ex
@app.route('/brand', methods=['GET'])
def brand():
    """Marca"""
    try:
        result = list_brand()
        marca=[]
        for fila in result:
            marca.append(fila)
        return jsonify(marca)

    except Exception as ex:
        return "Error"
@app.route('/product', methods=['GET'])
def products():
    """Principal"""
    try:
        result = search_all_products(request.args)
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
        result = get_product_id(productId)
        producto={}
        for fila in result:
            producto=fila
            print(producto)
        return jsonify(producto)
    except Exception as ex:
        return "Error"

@app.route('/')
def index():
    """Ruta para mostrar la página principal con las categorías"""
    try:
        categories = list_categories()
        marcas = list_brand()
        productos = search_all_products(request.args)
        return render_template('index.html', categories=categories, marcas= marcas, products= productos)
    except Exception as ex:
        return jsonify({})
@app.route('/products/<int:category_id>')
def get_products(category_id):
    """Ruta para obtener productos por categoría en formato JSON"""
    try:
        print(category_id)
        productos = list_products(category_id)
        print('get_products()', productos)
        return jsonify([dict(row) for row in productos])
    except Exception as ex:
        return jsonify({})
@app.route('/search')
def search():
    try:
        productos = search_all_products(request.args)
        print('search()', productos)
        return render_template('response.html', products= productos)
    except Exception as ex:
        return jsonify({})


def pagina_no_encontrada(error):
    """Página"""
    # return jsonify({"error":404, "mensaje":"Ruta no encontrada"})
    return "<h1>Página no encontrada</h1>"

# Configurar Swagger
SWAGGER_URL = '/swagger'
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
