from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_mail import Mail, Message
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import wrapper as wp
import os, uuid

# Load env config
load_dotenv()

app = Flask(__name__)
mail = Mail(app)

# Configuration of mail
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = os.getenv("APP_SECRET_KEY")

################ App Routes ################
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
        
        send_email(sess_values, token, total_summary, cart_items, order_dt)
        
        return render_template('bill.html', page_name="Bill", token=token, total=total_summary, items=cart_items, user=sess_values, order_dt=order_dt)
    else:
        return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html', page_name="About")

################ Admin routes ################
@app.route('/admin', strict_slashes=False)
def admin():
    return render_template('admin.html', page_name='Admin Panel', admin=True)

@app.route('/admin/items/add', methods=['GET', 'POST'])
def admin_add():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']
        category = request.form['category']
        price = request.form['price']
        desc = request.form['desc']
        imageName = save_image(name, image, category)

        if imageName != False:
            if wp.add_item_to_menu(name, category, price, desc, imageName):
                return render_template('item_add.html', page_name='Add Item', admin=True, add=True, itemName=name, category=category)
        return render_template('item_add.html', page_name='Add Item', admin=True, add=False)
    else:
        return render_template('item_add.html', page_name='Add Item', admin=True)

@app.route('/admin/items/remove')
def admin_remove():
    if request.method == 'GET':
        menu_items = wp.get_all_menu_items()
        return render_template('item_remove.html', page_name='Remove Item', admin=True, items=menu_items)
    else:
        return redirect(url_for('admin'))

@app.route('/admin/items/update')
def admin_update():
    return render_template('item_update.html', page_name='Update Item', admin=True)

@app.route('/admin/orders/show')
def admin_show_orders():
    data = wp.show_orders_data()
    return render_template('show_orders.html', page_name='Show Orders', admin=True, data=data)

@app.route('/admin/manage/menu-of-the-day')
def admin_manage_menu_of_the_day():
    menu_items = wp.get_all_menu_items()
    return render_template('motd.html', page_name='Menu of the Day', admin=True, items=menu_items)

################ API Routes ################
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

@app.route('/api/cart/empty', methods=['POST'])
def cart_empty():
    if request.method == 'POST':
        data = request.get_json()
        if data['token']:
            sess_keys = ['u_fullname', 'u_phone', 'u_email', 'u_payment']
            result = chk_sess_var(sess_keys)
            if result:
                session.clear()
            result = wp.make_cart_empty()
            return jsonify({'result': result})
        else:
            return jsonify({'result': False})   
    else:
        return redirect(url_for('index'))

@app.route('/api/menu/remove', methods=['POST'])
def remove_item_from_menu():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        category = data['category']
        image = data['image']

        if wp.remove_item_from_menu(name, category):
            result = remove_image(image, category)
            return jsonify({'result': result})
        else:
            return jsonify({'result': False})

################ Helper Functions ################
def chk_sess_var(variables: list):
    missing_variables = [var for var in variables if var not in session]

    if not missing_variables:
        return True
    else:
        return False
    
def send_email(user, token, total, cart_items, order_dt):
    
    body = f"Invoice #{token} for Your Recent Orders via HFC"
    msg = Message( 
                    body,
                    sender ='noreply@gmail.com',
                    recipients = [f'{user[2]}'] 
                ) 
    view = render_template('mail.html', user=user, token=token, total=total, items=cart_items, order_dt=order_dt)
    msg.html = view
    if mail.send(msg):
        return True
    return False

def save_image(name:str, image: object, category: str):
    try:
        if image.filename != '':
            new_filename = secure_filename(name) + os.path.splitext(image.filename)[1]
            save_path = os.path.join('static/products', category)

            # Create category folder if not exists
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            # Check if the file already exists
            while os.path.exists(os.path.join(save_path, new_filename)):
                # If the filename already exists, add a unique identifier to the name
                unique_id = str(uuid.uuid4().hex)[:6] 
                new_filename = secure_filename(name + '_' + unique_id) + os.path.splitext(image.filename)[1]

            image.save(os.path.join(save_path, new_filename))
            return new_filename
        return False
    except:
        return False

def remove_image(filename: str, category: str):
    try:
        file_path = os.path.join('static/products', category, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
