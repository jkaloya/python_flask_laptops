from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
mysql = MySQLConnector(app,'laptops')

@app.route('/')
def index():
    query = "SELECT * FROM laptops"
    laptops = mysql.query_db(query)
    return render_template('index.html', all_laptops=laptops)

@app.route('/info/<id>', methods=['GET'])
def view(id):
    query = "SELECT * FROM laptops where id = :id"
    data = {'id':id}
    laptops = mysql.query_db(query, data)
    return render_template('info.html', one_laptop=laptops[0])
#add
@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/create', methods =['POST'])
def create():
    query = "INSERT INTO laptops (title, size, color, screen_options, touchpad, created_at, updated_at) VALUES (:title, :size, :color, :screen_options, :touchpad, NOW(), NOW())"
    data = {'title': request.form['title'], 'size': request.form['size'], 'color': request.form['color'], 'screen_options': request.form['screen_options'],'touchpad': request.form['touchpad']}

    mysql.query_db(query, data)
    return render_template('add.html')

@app.route('/update/<id>')
def update(id):
    query = "SELECT * FROM laptops WHERE id = :id"
    data = {'id': id}
    laptop = mysql.query_db(query, data)
    return render_template('update.html', laptop=laptop[0])

@app.route('/updatelaptop/<id>', methods=['POST'])
def updatelaptop(id):
    query = "UPDATE laptops SET title = :title, size = :size, color = :color, screen_options = :screen_options, touchpad = :touchpad WHERE id = :id"

    data = {'title': request.form['title'], 'size': request.form['size'], 'color': request.form['color'], 'screen_options': request.form['screen_options'], 'touchpad': request.form['touchpad'], 'id': id}

    mysql.query_db(query, data)
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    query = "SELECT * FROM laptops WHERE id = :id"
    data = {'id': id}
    laptop = mysql.query_db(query, data)
    return render_template('delete.html', laptop=laptop[0])

@app.route('/delete_yes/<id>', methods=['POST'])
def delete_yes(id):
    query = "DELETE FROM laptops where id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/delete_no/<id>', methods=['POST'])
def delete_no(id):
    return redirect('/')

app.run(debug=True)
