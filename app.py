from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('customer.html')

@app.route('/cart')
def cart():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
