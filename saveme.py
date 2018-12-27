with connection.cursor() as cursor:
    sql = 'SELECT * from products'
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps({'STATUS': 'SUCCESS', 'PRODUCTS': result})
except:
return json.dumps({'STATUS': 'ERROR', 'MSG': "Internal error"})