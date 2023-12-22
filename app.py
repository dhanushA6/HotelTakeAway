from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import wrapper as wp

app = Flask(__name__)

app.secret_key = "hfc"

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

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "GET":
        total = wp.get_cart_total()
        sess_var = ['u_payment', 'u_phone', 'u_fullname', 'u_email']
        result = chk_sess_var(sess_var)
        new = []
        if result:
            new = [session['u_payment'], session['u_phone'], session['u_fullname'], session['u_email']]
        return render_template("checkout.html", page_name="Checkout", cart_total=total, e_session=new)
    else:
        session['u_payment'] = request.form['payment-method']
        session['u_phone'] = request.form['user-phoneno']
        session['u_fullname'] = request.form['user-fullname']
        session['u_email'] = request.form['user-email']
        return redirect(url_for('bill'))

@app.route('/checkout/bill')
def bill():
    sess_keys = ['u_fullname', 'u_phone', 'u_email', 'u_payment']
    result = chk_sess_var(sess_keys)
    if result == True and wp.cart_items():
        sess_values = [session['u_fullname'], session['u_phone'], session['u_email'], session['u_payment']]
        cust = wp.create_customer(
            sess_values[0], sess_values[1], sess_values[2]
        )
        new_order = wp.create_order(cust)
        wp.assign_token_and_datetime(new_order)
        token = new_order.token
        cart_items = wp.get_ordered_cart_items(new_order)            
        total_summary = wp.get_ordered_bill_total(new_order)
        order_dt = [new_order.order_date, new_order.order_time, new_order.type, new_order.is_paid]
        wp.do_payment(session['u_payment'], new_order)
        wp.push_orders(new_order)
        
        return render_template('bill.html', page_name="Bill", token=token, total=total_summary, items=cart_items, user=sess_values, order_dt=order_dt)
    else:
        return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html', page_name="About")

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

@app.route("/api/cart/update", methods=["POST"])
def update_cart():
    if request.method == "POST":
        data = request.get_json()
        for item in data:
            new = wp.create_item(
                item['p_name'],
                item['p_price'],
                item['p_desc'],
                item['p_img'],
                item['p_cat']
            )
            result = wp.add_item_to_cart(new, item['qty'])
        return jsonify({"message": result})

def chk_sess_var(variables: list):
    missing_variables = [var for var in variables if var not in session]

    if not missing_variables:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)
