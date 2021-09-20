"""
Code for handling sessions in the web application
"""

from bottle import request, response
import uuid
import json

import model
import dbschema

COOKIE_NAME = 'session'


def get_or_create_session(db):
    """Get the current sessionid either from a
    cookie in the current request or by creating a
    new session if none are present.

    If a new session is created, a cookie is set in the response.

    Returns the session key (string)
    """

    key = request.get_cookie(COOKIE_NAME)
    row = None
    if key : 
        #print('key exists')
        cur = db.cursor()
        cur.execute("SELECT sessionid FROM sessions WHERE sessionid=?", (key,))
        row = cur.fetchone()
        if row:
            key = row['sessionid']

    # if row is empty, i.e., there is no session associated, create a new one.
    if not row :
        # print('creating new session')
        key = str(uuid.uuid4())
        data = "[]"
        cur = db.cursor()
        # store this new session key in the database with data as an empty string
        cur.execute("INSERT INTO sessions VALUES (?,?)", (key,data,))
        db.commit()
        
        response.set_cookie(COOKIE_NAME, key)

    return key

   
def add_to_cart(db, itemid, quantity,update=False):
    """Add an item to the shopping cart"""
    session_id = get_or_create_session(db)
    # get product details from database
    item_to_be_added = model.product_get(db,itemid)
    item_name = item_to_be_added['name']
    unit_cost = item_to_be_added['unit_cost']
    print(item_name)
    is_already_in_cart = False
    # get the cart items from session table.
    cart_items = get_cart_contents(db)
    if (cart_items):
        for item in cart_items:
            if item['id'] == itemid:  # checking if item is already in cart
                is_already_in_cart = True
                if not update:
                    item['quantity'] += quantity
                else:  # if update flag is set, the quantity should be rewritten entirely instead of adding to the current quantity
                    item['quantity'] = quantity
                item['cost'] = item['quantity'] * unit_cost
                break
    if not is_already_in_cart:  # if already not in cart, create a new entry
           cart_items.append(
                    {
                'id': itemid,
                'quantity': quantity,
                'name': item_name,
                'cost': quantity * unit_cost 
                    }
           )
    cart_items = json.dumps(cart_items)

    cur = db.cursor()
    cur.execute("UPDATE sessions SET data=? WHERE sessionid=?",(cart_items,session_id))
    db.commit()


def get_cart_contents(db):
    """Return the contents of the shopping cart as
    a list of dictionaries:
    [{'id': <id>, 'quantity': <qty>, 'name': <name>, 'cost': <cost>}, ...]
    """
    session_id = get_or_create_session(db)
    cur = db.cursor()
    cur.execute("SELECT data FROM sessions WHERE sessionid=?", (session_id,))
    row = cur.fetchone()
    print(row['data'])
    items_in_cart = []
    if(row['data']):
        items_in_cart = json.loads(row['data'])
    print(items_in_cart)
    return items_in_cart

