from flask import Flask, render_template, request, redirect, url_for
import wrapper as wp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page_name="Home")

@app.route('/category/<name>', methods=['GET', 'POST'])
def category(name):
    items = wp.get_menu_items(name)
    return render_template('category.html', page_name="Category", name=name.capitalize(), items=items)

@app.route('/cart')
def cart():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
