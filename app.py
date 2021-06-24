from flask  import Flask, request, render_template, redirect, url_for, make_response
from flask_qrcode import QRcode
from flask_wtf.csrf import CSRFProtect
import pdfkit
from flask_login import LoginManager
from flask_mysqldb import MySQL


app = Flask(__name__, static_folder='static')
app.secret_key = 'isaac'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'k3nsh1n'
app.config['MYSQL_PASSWORD'] = 'k0rn82...'
app.config['MYSQL_DB'] = 'PLANVACACIONAL'
mysql = MySQL(app)
csrf = CSRFProtect(app)
qrcode = QRcode(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_worker', methods=['POST'])
def add_worker():
    if request.method == 'POST':
        name = request.form['name']
        adscription = request.form['adscription']
        category = request.form['category']
        matricula = request.form['matricula']
        nAfil = request.form['nAfil']
        cellphone = request.form['cellphone']
        direction = request.form['direction']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registerWorker (name, adscription, category, matricula, nAfil, cellphone, direction) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                        (name, adscription, category, matricula, nAfil, cellphone, direction))
        mysql.connection.commit()
        #   flash('Register was added successfully');
        return redirect(url_for('index'))


@app.route('/list', methods=['GET'])
def list_worker():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM registerWorker')
        data = cur.fetchall()
        return render_template('list.html', datas = data)

@app.route('/delete/<string:id>')
def delete_worker(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registerWorker WHERE id = {0}'.format(id))
    cur.connection.commit()
    return redirect(url_for('list_worker'))


@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registerWorker WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit.html', datas = data)


@app.route('/update/<string:id>', methods=['POST'])
def update(id):
   if request.method == 'POST':
       name = request.form['name']
       adscription = request.form['adscription']
       category = request.form['category']
       matricula = request.form['matricula']
       nAfil = request.form['nAfil']
       cellphone = request.form['cellphone']
       direction = request.form['direction']
       cur = mysql.connection.cursor()
       cur.execute('UPDATE registerWorker SET name=%s, adscription=%s, category=%s, matricula=%s, nAfil=%s, cellphone=%s, direction=%s WHERE id = %s', (name, adscription, category, matricula, nAfil, cellphone, direction, id))
       mysql.connection.commit()
       return redirect(url_for('list_worker'))


@app.route('/registerCh/<id>', methods=['GET', 'POST'])
def registerCh(id):
    if request.method == 'GET':
        return render_template('registerChildren.html')
    elif request.method == 'POST':
        name = request.form['name']
        fDate = request.form['fDate']
        tSangre = request.form['tSangre']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO registerChildrens(name, fDate, tSangre, worker_id) VALUES(%s, %s, %s, %s)', (name, fDate, tSangre, id))
        mysql.connection.commit()
        #print(name, fDate, tSangre)
        #return 'was addes successfully'
        return redirect(url_for('listC'))


@app.route('/listC')
def listC():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM registerChildrens')
        data = cur.fetchall()    
        return render_template('listC.html', datas = data)

@app.route('/deleteC/<string:id>')
def deleteC(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM registerChildrens WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('listC'))


@app.route('/qrcode/<id>', methods=['GET'])
def QrCode(id):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM registerWorker inner join registerChildrens WHERE worker_id = {0}'.format(id))
        rows = cur.fetchall()
        #print(rows[0])
        return render_template('qrcode.html', rows = rows)

@app.route('/printPdf/<string:id>', methods=['GET'])
def printPdf(id):
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM registerWorker inner join registerChildrens WHERE worker_id = {0}'.format(id))
    rows = cur.fetchall()
    mysql.connection.commit()
    res = render_template('printPdf.html', rows = rows)
    print(rows)
    print(res)


    css = '/Users/k3nsh1n/flask-projects/planVacacional/static/css/main.css'
    responseString = pdfkit.from_string(res, False)
    response = make_response(responseString)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response




if __name__ == '__main__':
    app.run(port = 3000, debug=True)
