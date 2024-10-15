import os
import pymysql.cursors
# Connect to the database
connection = pymysql.connect(host=os.environ['MYSQL_HOST'],
                             user=os.environ['MYSQL_USER'],
                             password=os.environ['MYSQL_PASSWORD'],
                             database=os.environ['MYSQL_DATABASE'],
                             cursorclass=pymysql.cursors.DictCursor)

def list_categories():
    """Categoria"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("select id, nombre from categorias")
            result = cursor.fetchall()
            return result
    except Exception as ex:
        return "Error"
def list_brand():
    """Marca"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""select id, nombre from marcas""")
            result = cursor.fetchall()
            return result
    except Exception as ex:
        return "Error"
def list_products(category_id):
    """Obtener productos por categoría"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM productos WHERE categoria_id = {0}""".format(int(category_id)))
            result = cursor.fetchall()
            return result
    except Exception as ex:
        return "Error"
def search_all_products(request):
    """Principal"""
    try:
        add_where =""
        if request:
            if request.get('nombre'):
                add_where += "where nombre like '%{0}%' ".format(request.get('nombre'))
            if request.get('precio_min'):
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "precio>={0} ".format(float(request.get('precio_min')))
            if request.get('precio_max'):
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "precio<{0} ".format(float(request.get('precio_max')))
            if request.get('categoria_id'):
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "categoria_id={0} ".format(int(request.get('categoria_id')))
            if request.get('marca_id'):
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "marca_id={0} ".format(int(request.get('marca_id')))
            if request.get('en_oferta') and request.get('en_oferta')=='true':
                add_where += "where " if len(add_where)==0 else "and "
                add_where += "en_oferta=1 "
                add_where += "and descuento>0 "
            if request.get('popularidad'):
                add_where += "order by popularidad desc"
        with connection.cursor() as cursor:
            sql_consulta ="""select p.id, p.nombre, p.descripcion, p.precio, p.stock, p.descuento, p.popularidad,  c.nombre as \"categianombre\", m.nombre as \"marcanombre\"\
            from ecommerce.productos p\
            left join ecommerce.categorias c on p.categoria_id=c.id\
            left join ecommerce.marcas m on p.marca_id = m.id """+add_where
            cursor.execute(sql_consulta)
            result = cursor.fetchall()
            return result
    except Exception as ex:
        return "Error"
def get_product_id(productId):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""select id, nombre, descripcion, precio, stock, en_oferta, descuento, popularidad\
                        from productos where id='{0}'""".format(int(productId)))
            result = cursor.fetchall()
            return result
    except Exception as ex:
        return "Error"