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
            result = cursor.fetchall()
            response = {
                'STATUS': 'SUCCESS',
                'MSG': '',
                'CATEGORIES': result,
                'CODE': 200
            }
            return json.dumps(response)
    except:
        response = {
            'STATUS': 'ERROR',
            'MSG': 'internal error',
            'CODE': 500
        }
        return json.dumps(response)


@post("/product")
def add_product():
    id = request.POST.get('id')
    cat_id = request.POST.get('category')
    title = request.POST.get('title')
    description = request.POST.get('desc')
    price = request.POST.get('price')
    favorite = request.POST.get('favorite')
    if favorite is None:
        n_fav = 0
    else:
        n_fav = 1
    img_url = request.POST.get('img_url')
    if cat_id != '':
        try:
            with connection.cursor() as cursor:
                sql = 'UPDATE products SET cat_id=%s, title=%s, description=%s, price=%s, favorite=%s, img_url=%s WHERE id=%s'
                data = (cat_id, str(title), str(description), price, n_fav, str(img_url), id)
                cursor.execute(sql, data)
                connection.commit()
                response = {
                    'STATUS': 'SUCCESS',
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


@get("/product/<pid>")
def load_products(pid):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM products'
            cursor.execute(sql)
            result = cursor.fetchall()
            if not result:
                response = {
                    'STATUS': 'ERROR',
                    'MSG': 'Product not found',
                    'CODE': 404
                }
                return json.dumps(response)
            response = {
                'STATUS': 'SUCCESS',
                'PRODUCT': result,
                'CODE': 200
            }
        return json.dumps(response)
    except:
        response = {
            'STATUS': 'ERROR',
            'MSG': 'internal error',
            'CODE': 500
        }
        return json.dumps(response)


@route('/product/<pid>', method='DELETE')
def delete_product(pid):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM products WHERE id = {}'.format(pid)
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            if result:
                sql = 'DELETE FROM products WHERE id = {}'.format(pid)
                cursor.execute(sql)
                connection.commit()
                response = {
                    'STATUS': 'SUCCESS',
                    'CODE': 201
                }
                return json.dumps(response)
            else:
                response = {
                    'STATUS': 'ERROR',
                    'MSG': 'Product not found',
                    'CODE': 404
                }
                return json.dumps(response)
    except:
        response = {
            'STATUS': 'ERROR',
            'MSG': 'internal error',
            'CODE': 500
        }
        return json.dumps(response)


@get("/products")
def show_products():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM products'
            cursor.execute(sql)
            result = cursor.fetchall()
            response = {
                'STATUS': 'SUCCESS',
                'PRODUCTS': result,
                'CODE': 200
            }
        return json.dumps(response)
    except:
        response = {
            'STATUS': 'ERROR',
            'MSG': 'internal error',
            'CODE': 500
        }
        return json.dumps(response)


@get('/category/<id>/products')
def list_products_cat(id):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM products WHERE cat_id = {} ORDER by favorite DESC'.format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            if not result:
                response = {
                    'STATUS': 'ERROR',
                    'MSG': 'Category not found',
                    'ERROR': 404
                }
                return json.dumps(response)
            response = {
                'STATUS': 'SUCCESS',
                'PRODUCTS': result,
                'CODE': 200
            }
        return json.dumps(response)
    except:
        response = {
            'STATUS': 'ERROR',
            'MSG': 'internal error',
            'CODE': 500
        }
        return json.dumps(response)


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
