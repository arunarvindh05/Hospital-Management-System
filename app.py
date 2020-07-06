from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect
)
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
from datetime import datetime

rid = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


class Patients(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    doa = db.Column(db.DateTime)
    tob = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    meds = db.relationship('Medicines', backref='patients')


diag_meds = db.Table('diag_meds',
                     db.Column('med_id', db.Integer, db.ForeignKey(
                         'medicines.id'), primary_key=True),
                     db.Column('diagn_id', db.Integer, db.ForeignKey(
                         'diagnostics.id'), primary_key=True)
                     )


class Medicines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(50), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)

    diagn = db.relationship('Diagnostics', secondary=diag_meds)


class Diagnostics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diagn = db.Column(db.String(500), nullable=False)


@app.route('/')
def home():
    error = ''
    return render_template('home.html')


@app.route('/login1', methods=['GET', 'POST'])
def login1():
    message = 'Welcome Registration/Admission desk executive'
    error = ''
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for i in cur.execute('SELECT * FROM Login'):
            if i[0] == username and i[1] == password:
                return redirect(url_for('profile1'))
        return render_template('login.html', z=message, error='Error: Incorrect Username or Password')
    return render_template('login.html', z=message)


@app.route('/login2', methods=['GET', 'POST'])
def login2():
    message = 'Welcome Pharmacist'
    error = ''
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for i in cur.execute('SELECT * FROM Pharma_Login'):
            if i[0] == username and i[1] == password:
                return redirect(url_for('profile2'))
        return render_template('login.html', z=message, error='Error: Incorrect Username or Password')

    return render_template('login.html', z=message)


@app.route('/login3', methods=['GET', 'POST'])
def login3():

    message = 'Welcome Diagnostic services Executive'
    error = ''
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for i in cur.execute('SELECT * FROM Diagnostics_Login'):
            if i[0] == username and i[1] == password:
                return redirect(url_for('profile3'))
        return render_template('login.html', z=message, error='Error: Incorrect Username or Password')
    return render_template('login.html', z=message)


@app.route('/profile1')
def profile1():
    return render_template('profile1.html')


@app.route('/profile2')
def profile2():
    return render_template('profile2.html')


@app.route('/profile3')
def profile3():
    return render_template('profile3.html')


@app.route('/createpatient', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':

        sid = request.form['cid']
        id = int(sid)+1
        name = request.form['name']
        age = request.form['age']
        doa = request.form['date']
        tob = request.form['trans']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        status = "created"

        con = sql.connect("db.sqlite3")
        cur = con.cursor()
        cur.execute("INSERT INTO patients (sid,id,name,age,doa,tob,address,city,state,status) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (sid, id, name, age, doa, tob, address, city, state, status))
        con.commit()
        con.close()

    return render_template('createpatient.html')


@app.route('/updatepatient', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        if "get1" in request.form:
            getsid = request.form['sid']

            con = sql.connect("db.sqlite3")
            con.row_factory = sql.Row

            cur = con.cursor()
            ss = "SELECT * FROM patients WHERE SID=?;"
            for row in cur.execute(ss, [getsid]):
                sid = row[0]
                name = row[2]
                age = row[3]
                doa = row[4]
                tob = row[5]
                address = row[6]
                city = row[7]
                state = row[8]

            return render_template("updatepatient.html", sid=sid, tob=tob, name=name, age=age, doa=doa, address=address, city=city, state=state)
        if "sub" in request.form:
            sid = request.form['getsid']
            id = int(sid)+1
            name = request.form['name']
            age = request.form['age']
            doa = request.form['doa']
            tob = request.form.get('tob')
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            status = "created"

            con = sql.connect("db.sqlite3")
            cur = con.cursor()
            cur.execute("UPDATE patients SET id=?,name=?,age=?,doa=?,tob=?,address=?,city=?,state=?,status=? WHERE sid=?",
                        (id, name, age, doa, tob, address, city, state, status, sid))
            con.commit()
            con.close()
            return render_template('searchud.html', z='Updated Sucessfully')

    return render_template('searchud.html')


@app.route('/deletepatient', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        if "get1" in request.form:

            getsid = request.form['sid']
            count = 0
            l = []
            con = sql.connect("db.sqlite3")
            con.row_factory = sql.Row
            cur = con.cursor()
            ss = "SELECT * FROM patients WHERE SID=?;"

            for row in cur.execute(ss, [getsid]):
                count += 1
                sid = row[0]
                name = row[2]
                age = row[3]
                doa = row[4]
                tob = row[5]
                address = row[6]
                city = row[7]
                state = row[8]
            if count == 0:
                return render_template('searchud.html', z='No Data Found')
            elif count >= 1:

                return render_template('deletepatient.html', sid=sid, tob=tob, name=name, age=age, doa=doa, address=address, city=city, state=state)
        if 'del' in request.form:
            sid = request.form['getsid']
            con = sql.connect("db.sqlite3")
            cur = con.cursor()
            cur.execute("DELETE  FROM patients WHERE sid=?;", [sid])
            con.commit()
            con.close()
            return render_template('searchud.html', z='Deleted records sucessfully')

    return render_template('searchud.html')


@app.route('/searchpatients', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if "get1" in request.form:
            getsid = request.form['sid']

            con = sql.connect("db.sqlite3")
            con.row_factory = sql.Row
            cur = con.cursor()
            count = 0
            l = []
            ss = "SELECT * FROM patients WHERE SID=?;"
            for row in cur.execute(ss, [getsid]):
                l.append(row)
                count += 1

            if count == 0:
                return render_template('searchud.html', z='No Data Found')
            return render_template("searchresults.html", z=l)
    return render_template('searchud.html')


@app.route('/viewpatients')
def viewall():
    l = []
    con = sql.connect("db.sqlite3")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM patients'):
        l.append(row)
    return render_template('searchresults.html', z=l)


@app.route('/patientbill')
def patientbill():
    return render_template('patientbill.html')


@app.route('/diag', methods=['GET', 'POST'])
def diag():
    if request.method == 'POST':
        diagn = str(request.form['dname'])
        l = []

        con = sql.connect("db.sqlite3")
        cur = con.cursor()
        for row in cur.execute('SELECT * FROM diag_meds WHERE diag=?', [diagn]):
            l.append(row)
        if len(l) < 1:
            return render_template('diag.html', z='Diag_Meds is not Working')
        cur.execute("INSERT INTO diagnostics (id,diagn,med_id,amount) VALUES (?,?,?,?)",
                    (rid[-1], diagn, l[0][2], l[0][3]))
        con.commit()
        con.close()
        return render_template('diag.html', k=[rid[-1], diagn, l[0][2], l[0][3]], z='Diagnostics Issued Sucessfully')
    return render_template('diag.html')


@app.route('/issuemed', methods=['GET', 'POST'])
def issuemed():
    if request.method == 'POST':
        mname = request.form['mname']
        qty = int(request.form['qty'])
        con = sql.connect("db.sqlite3")
        con.row_factory = sql.Row
        cur = con.cursor()
        count = 0
        l = []
        rate = 0
        ss = "SELECT * FROM Medicines WHERE Medname = ?;"
        for row in cur.execute(ss, [mname]):
            l.append(row)
            rate = row[3]
            count += 1
        if count == 0:
            return render_template('issuemed.html', z='Medicine not found')
        if l[0][2] < qty:
            return render_template('issuemed.html', z='Not enough Medicine is Available')
        rem = l[0][2]-qty
        Amount = rate*qty
        cur.execute("INSERT INTO Patientsmedicines (id,mname,qty,pid,rate,amount) VALUES (?,?,?,?,?,?)",
                    (l[0][0], mname, qty, rid[-1], rate, Amount))
        cur.execute(
            'UPDATE Medicines SET Medqty = ? WHERE Medname = ?', (rem, mname))
        con.commit()
        con.close()
        return render_template('issuemed.html', z='Medicine Sucessfully Assigned', k=[l[0][0], mname, qty, rate, Amount])
    return render_template('issuemed.html')


@app.route('/getdiagpatients', methods=['GET', 'POST'])
def getdiagpatients():
    if request.method == 'POST':
        if "get1" in request.form:
            getsid = int(request.form['sid'])

            con = sql.connect("db.sqlite3")
            con.row_factory = sql.Row
            cur = con.cursor()
            count = 0
            l = []
            m = []
            n = []
            ss = "SELECT * FROM patients WHERE SID=?;"
            for row in cur.execute(ss, [getsid]):
                l.append(row)
                count += 1

            if count == 0:
                return render_template('diagsearchud.html', z='No Data Found')
            for row in cur.execute('SELECT * FROM Patientsmedicines WHERE pid=?', [getsid]):
                m.append(row)

            for row in cur.execute('SELECT * FROM diagnostics WHERE id=? ', [getsid]):
                n.append(row)
            if len(n) < 1:
                return render_template('diagsearchud.html', z='Table not working')
            rid.append(getsid)
            return render_template("diagsearchresults.html", y=l, w=m, x=n)
    return render_template('diagsearchud.html')


@app.route('/getpharmapatients', methods=['GET', 'POST'])
def getpharmapatients():
    if request.method == 'POST':
        if "get1" in request.form:
            getsid = request.form['sid']

            con = sql.connect("db.sqlite3")
            con.row_factory = sql.Row
            cur = con.cursor()
            count = 0
            l = []
            m = []
            ss = "SELECT * FROM patients WHERE SID=?;"
            for row in cur.execute(ss, [getsid]):
                l.append(row)
                count += 1

            if count == 0:
                return render_template('pharmasearchud.html', z='No Data Found')
            for row in cur.execute('SELECT * FROM Patientsmedicines WHERE pid=?', [getsid]):
                m.append(row)
            rid.append(getsid)
            return render_template("pharmasearchresults.html", z=l, w=m)
    return render_template('pharmasearchud.html')


if __name__ == '__main__':
    app.run(debug=True)
