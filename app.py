from flask import Flask, render_template, request, redirect, url_for, jsonify
import wrapper as wp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page_name="Home")

@app.route('/category/<name>', methods=['GET', 'POST'])
def category(name):
    if request.method == 'GET':
        items = wp.get_menu_items(name)
        names = wp.get_cart_item_names()
        return render_template('category.html', page_name="Category", name=name.capitalize(), items=items, names=names)
    else:
        return redirect(url_for('index'))
        
@app.route('/cart')
def cart():
    cart_items = wp.cart_items()
    cart_total = wp.get_cart_total()
    return render_template('cart.html', page_name="Cart", cartItems=cart_items, cart_total=cart_total)

@app.route('/orders')
def orders():
    return render_template('orders.html', page_name="Orders")

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        data = request.get_json()
        item = wp.create_item(
            data['p_name'],
            data['p_price'],
            data['p_desc'],
            data['p_img'],
            data['p_cat']
        )
        result = wp.add_item_to_cart(item, 1)
        return jsonify({'result': result})

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    if request.method == 'POST':
        data = request.get_json()
        item = wp.create_item(
            data['p_name'],
            data['p_price'],
            data['p_desc'],
            data['p_img'],
            data['p_cat']
        )
        result = wp.remove_cart_item(item)
        return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
