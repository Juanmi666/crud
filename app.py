from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import pymysql as mysql
import pg8000 as pg
import fpdf
from fpdf import FPDF

app = Flask(__name__)
app.py:7
#nueva ruta para la página web
@app.route("/")
def web():

    con = pg.connect(host="localhost", user="postgres", password="metal666", database="msc2019")
    cursor = con.cursor()
    cursor.execute("select * from empleadas")
    rows = cursor.fetchall()

    return render_template('index.html', empleados=rows)

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

@app.route("/reportes")
def report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 20, )
    pdf.cell(180, 10, 'Reportes de empleados', 1, 1, 'C')
    pdf.set_font('Arial', 'B', 10, )
    pdf.cell(60, 10, 'Clave', 1, 0, 'C')
    pdf.cell(60, 10, 'Nombre', 1, 0, 'C')
    pdf.cell(60, 10, 'Clave', 1, 1, 'C')

    con = pg.connect(host="localhost", user="postgres", password="metal666", database="msc2019")
    cursor = con.cursor()
    cursor.execute("select * from empleadas")
    rows = cursor.fetchall()

    pdf.set_font('Arial', '', 10)
    for row in rows:
        pdf.cell(60, 10, str(row[0]), 1, 0, 'C')
        pdf.cell(60, 10, str(row[1]), 1, 0, 'C')
        pdf.cell(60, 10, str(row[2]), 1, 1, 'C')

    con.close()
    pdf.output('templates/reportes.pdf', 'F')

    return send_from_directory(directory='templates',filename='reportes.pdf')
    #return render_template('reportes.pdf')
    #return redirect(url_for('web'))


def do_the_login():
    details = request.form
    clave = details['id']
    nombre = details['username']
    sueldo = details['money']

    connection = pg.connect(host="localhost", user="postgres", password="metal666", database="msc2019")

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO empleadas (clave,nombre,sueldo) VALUES (%s, %s, %s)"
            cursor.execute(sql, (int(clave), str(nombre), str(sueldo)))
        connection.commit()
    finally:
        connection.close()

    mensaje ="Se guardo correctamente"
    tipo= "success"
    return redirect(url_for('web'))

@app.route('/insertar', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return render_template('insertar.html')


def do_delete(id):
    details = request.form
    clave = id

    connection = pg.connect(host='localhost',
                                 user='postgres',
                                 password='metal666',
                                 database='msc2019')
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM empleadas WHERE clave="+id
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()

    mensaje ="Se elimino correctamente"
    tipo= "success"
    return redirect(url_for('web'))

@app.route('/eliminar', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        clave = request.args.get('id')
        return do_delete(clave)
    else:
        return render_template('insertar.html')

def obtener_datos(clave):
    con = pg.connect(host="localhost", user="postgres", password="metal666", database="msc2019")
    cursor = con.cursor()
    cursor.execute("select * from empleadas where clave="+clave)
    rows = cursor.fetchone()

    clave_o = rows[0]
    nombre_o = rows[1]
    sueldo_o = rows[2]

    return render_template('actualizar.html',clave=clave_o, nombre=nombre_o, sueldo=sueldo_o)

def do_update():
    details = request.form
    clave = details['id']
    nombre = details['username']
    sueldo = details['money']

    connection = pg.connect(host='localhost',
                                 user='postgres',
                                 password='metal666',
                                 database='msc2019')
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "UPDATE empleadas SET nombre='"+nombre+"' ,sueldo='"+sueldo+"' where clave="+clave
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()

    mensaje ="Se guardo correctamente"
    tipo= "success"
    return redirect(url_for('web'))


@app.route('/actualizar', methods=['GET', 'POST'])
def actualizar():
    if request.method == 'POST':
        return do_update()
    else:
        clave = request.args.get('clave')
        return obtener_datos(clave)



if __name__ == '__main__':
    app.run(debug=True)
