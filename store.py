from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="axel1012",
                             db="store",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@post("/category")
def create_category():
    name = request.POST.get("name")
    if name == '' or name.isdigit():
        response = {
            'STATUS': 'ERROR',
            'MSG': 'Category cannot be a number or empty',
            'CAT_ID': '',
            'CODE': 400
        }
        return json.dumps(response)
    try:
        with connection.cursor() as cursor:
            sql = 'select * from categories where cate_name = "{}"'.format(name)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                response = {
                    'STATUS': 'ERROR',
                    'MSG': 'This category already exists',
                    'CAT_ID': '',
                    'CODE': 200
                }
                return json.dumps(response)
            sql = 'INSERT INTO categories (cate_name) VALUES ("{}")'.format(name)
            cursor.execute(sql)
            connection.commit()
            cat_id = cursor.lastrowid
            response = {
                'STATUS': 'SUCCESS',
                'MSG': '',
                'CAT_ID': cat_id,
                'CODE': 201
            }
            return json.dumps(response)
    except:
        response = {
            'STATUS': 'ERROR',
            'MSG': 'internal error',
            'CAT_ID': '',
            'CODE': 500
        }
        return json.dumps(response)


@route("/category/<catId>", method='DELETE')
def delete_category(catId):
    try:
        with connection.cursor() as cursor:
            sql = 'select * from categories WHERE cat_id = {}'.format(catId)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                response = {
                    'STATUS': 'ERROR',
                    'MSG': 'Category not found',
                    'CODE': 404
                }
                return json.dumps(response)
            sql = 'DELETE FROM categories WHERE cat_id = {}'.format(catId)
            cursor.execute(sql)
            connection.commit()
            response = {
                'STATUS': 'SUCCESS',
                'MSG': 'The category was deleted successfully',
                'CODE': 201
            }
            return json.dumps(response)
    except:
        response = {
            'STATUS': 'ERROR',
            'MSG': 'internal error',
            'CODE': 500
        }
        return json.dumps(response)


@get("/categories")
def load_categories():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * from categories'
            cursor.execute(sql)
            response = cursor.fetchall()
            return json.dumps(response)
        return
    except:
        response = {
            'STATUS': 'ERROR',
            'MSG': 'internal error',
            'CODE': 500
        }
        return json.dumps(response)


@route('/product/<pid>', method='DELETE')
def delete_product():
    try:
        return
    except:
        return


@get("/products")
def show_products():
    try:
        return
    except:
        return


@get("/product/<pid>")
def load_products():
    try:
        return
    except:
        return


@get('/category/<id>/products')
def list_products_cat():
    try:
        return
    except:
        return


@post("/product")
def add_product():
    try:
        return
    except:
        return


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


# run(host='0.0.0.0', port=argv[1])
run(host='localhost', port=7002)