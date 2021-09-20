
import random
from bottle import Bottle, template, static_file, request, response, redirect, HTTPError, post
import json
import model
import session
import bottle
app = Bottle()



@app.route('/')
def home(db):
    session.get_or_create_session(db)
    product_list = model.product_list(db)
    products = []
    for row in product_list:
        
        product = {
            'id': row['id'],
            'name' : row['name'],
            'image_url' : row['image_url'],
            'description' : row['description'],
            'unit_cost' : row['unit_cost']
        }
        products.append(product)
    about = None 
    return template('home',{'products':products,'about':about})

@app.route('/about')
def about(db):
    about = "Welcome to WT! The innovative online store"  
    session.get_or_create_session(db)
    product_list = model.product_list(db)
    products = []
    for row in product_list:
        
        product = {
            'id' : row['id'],
            'name' : row['name'],
            'image_url' : row['image_url'],
            'description' : row['description'],
            'unit_cost' : row['unit_cost']
        }
        products.append(product)
    return template('home',{'products':products,'about':about})  

@app.route('/category/<cat>')
def filter_by_category(db,cat):
    session.get_or_create_session(db)
    if cat == "men" or cat == "women":
        product_list = model.product_list(db,category=cat)
        products = []
        for row in product_list:
            
            product = {
                'id' : row['id'],
                'name' : row['name'],
                'image_url' : row['image_url'],
                'description' : row['description'],
                'unit_cost' : row['unit_cost']
            }
            products.append(product)
            
        about = None 
        return template('home',{'products':products,'about':about})
    else :
        return template('error',{'message':"No products in this category"})    

@app.route('/product/<id>')
def product(db,id):
    key = session.get_or_create_session(db)
    row = model.product_get(db,id)
    if row :
        product = {
                'id' : row['id'],
                'name' : row['name'],
                'image_url' : row['image_url'],
                'description' : row['description'],
                'unit_cost' : row['unit_cost']
            }
        
        response.set_cookie("session",key,path='/')
        return template('product',{'product':product})
    else :
        response.status = 404
        return template('error',{'message':'No product with that id'})  



@app.route("/cart",method="POST")
def add_to_cart_post(db):

    id = request.forms.get('product')
    quantity = int(request.forms.get('quantity'))
    row = model.product_get(db,id)
    name = row['name']
    session.get_or_create_session(db)
    session.add_to_cart(db,id,quantity)
    message = str(quantity) + " items of "+name+" added to the cart "
    #response.status=302
    redirect('/cart',302)
    return template('success',{'message':message})


@app.route('/cart',method="GET")
def list_cart_items(db):
    session.get_or_create_session(db)
    print(session.get_cart_contents(db))
    items = session.get_cart_contents(db)
    products = []
    total_cost = 0
    for item in items:
        row = model.product_get(db,item['id'])
        product = {
            'id' : row['id'],
            'name' : row['name'],
            'image_url' : row['image_url'],
            'description' : row['description'],
            'cost' : item['cost'],
            'quantity': item['quantity'] 
        }
        total_cost += item['cost']
        products.append(product)
    return template('cart',{'products':products,'total_cost':total_cost})

@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':

    from bottle.ext import sqlite
    from dbschema import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
