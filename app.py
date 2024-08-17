"""Archivo Principal"""
import os
# from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "mysql123"
app.config["MYSQL_HOST "] = "localhost"
app.config["MYSQL_PORT "] = 3306
app.config["MYSQL_DB"] = "ecommerce"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql=MySQL(app)

productos=[
    {
        "productID":1,
        "nombre":"Shampoo"
    },
    {
        "productID":2,
        "nombre":"Jabón"
    },
    {
        "productID":3,
        "nombre":"Pasta"
    }
]

@app.route('/', methods=['GET'])
def home():
    """Principal"""
    return jsonify(productos)
@app.route('/product', methods=['GET'])
def products():
    """Principal"""
    try:
        add_where =""
        if request.args:
            add_where="where "
            if request.args.get('nombre'):
                if len(add_where)>6: add_where += "and "
                add_where += "nombre like '%{0}%' ".format(request.args.get('nombre'))
            if request.args.get('precio_min'):
                if len(add_where)>6: add_where += "and "
                add_where += "precio>={0} ".format(float(request.args.get('precio_min')))
            if request.args.get('precio_max'):
                if len(add_where)>6: add_where += "and "
                add_where += "precio<{0} ".format(float(request.args.get('precio_max')))
            if request.args.get('categoria_id'):
                if len(add_where)>6: add_where += "and "
                add_where += "categoria_id={0} ".format(int(request.args.get('categoria_id')))
            if request.args.get('marca_id'):
                if len(add_where)>6: add_where += "and "
                add_where += "marca_id={0} ".format(int(request.args.get('marca_id')))
            if request.args.get('en_oferta'):
                if len(add_where)>6: add_where += "and "
                add_where += "en_oferta=1 "
                add_where += "and descuento>0 "
            if request.args.get('popularidad'):
                add_where += "order by popularidad desc"
                print(request.args.get('popularidad'))
        cur = mysql.connection.cursor()
        sql_consulta ="""select id, nombre, descripcion, precio, stock, en_oferta, descuento, popularidad from productos """+add_where
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

@app.route('/product/<id>', methods=['GET'])
def product_by_id(id):
    """Principal"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""select id, nombre, descripcion, precio, stock\
                     from productos where id='{0}'""".format(int(id)))
        result = cur.fetchall()
        productos=[]
        for fila in result:
            productos.append(fila)
            print(fila)
        return jsonify(productos)
    except Exception as ex:
        return "Error"

def pagina_no_encontrada(error):
    """Página"""
    # return jsonify({"error":404, "mensaje":"Ruta no encontrada"})
    return "<h1>Página no encontrada</h1>"

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
