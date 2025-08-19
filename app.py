
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta_simple"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "abc_tech"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM usuarios WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close(); db.close()
        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["nombre"]
            return redirect(url_for("dashboard"))
        flash("Correo o contraseña incorrectos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
        db.commit()
        cur.close(); db.close()
        flash("Usuario creado, ahora puedes iniciar sesión")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    mensaje = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        mensaje = "Si el correo existe, se enviaron instrucciones de recuperación."
    return render_template("recuperar.html", mensaje=mensaje)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", nombre=session.get("user_name", "Usuario"))

# --------- CRUD CLIENTES ---------
@app.route("/clientes")
def clientes_list():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM clientes ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close(); db.close()
    return render_template("clientes_list.html", clientes=rows)

@app.route("/clientes/nuevo", methods=["GET", "POST"])
def clientes_nuevo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")
        historial = request.form.get("historial_compras")
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO clientes (nombre, correo, telefono, direccion, historial_compras) VALUES (%s,%s,%s,%s,%s)",
                    (nombre, correo, telefono, direccion, historial))
        db.commit(); cur.close(); db.close()
        return redirect(url_for("clientes_list"))
    return render_template("clientes_form.html", data=None)

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def clientes_editar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")
        historial = request.form.get("historial_compras")
        cur.execute("UPDATE clientes SET nombre=%s, correo=%s, telefono=%s, direccion=%s, historial_compras=%s WHERE id=%s",
                    (nombre, correo, telefono, direccion, historial, id))
        db.commit(); cur.close(); db.close()
        return redirect(url_for("clientes_list"))
    cur.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    row = cur.fetchone(); cur.close(); db.close()
    return render_template("clientes_form.html", data=row)

@app.route("/clientes/eliminar/<int:id>")
def clientes_eliminar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM clientes WHERE id=%s", (id,))
    db.commit(); cur.close(); db.close()
    return redirect(url_for("clientes_list"))

# --------- CRUD PROVEEDORES ---------
@app.route("/proveedores")
def proveedores_list():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM proveedores ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close(); db.close()
    return render_template("proveedores_list.html", proveedores=rows)

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def proveedores_nuevo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        empresa = request.form["empresa"]
        contacto = request.form.get("contacto")
        telefono = request.form.get("telefono")
        productos = request.form.get("productos")
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO proveedores (empresa, contacto, telefono, productos) VALUES (%s,%s,%s,%s)",
                    (empresa, contacto, telefono, productos))
        db.commit(); cur.close(); db.close()
        return redirect(url_for("proveedores_list"))
    return render_template("proveedores_form.html", data=None)

@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
def proveedores_editar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method == "POST":
        empresa = request.form["empresa"]
        contacto = request.form.get("contacto")
        telefono = request.form.get("telefono")
        productos = request.form.get("productos")
        cur.execute("UPDATE proveedores SET empresa=%s, contacto=%s, telefono=%s, productos=%s WHERE id=%s",
                    (empresa, contacto, telefono, productos, id))
        db.commit(); cur.close(); db.close()
        return redirect(url_for("proveedores_list"))
    cur.execute("SELECT * FROM proveedores WHERE id=%s", (id,))
    row = cur.fetchone(); cur.close(); db.close()
    return render_template("proveedores_form.html", data=row)

@app.route("/proveedores/eliminar/<int:id>")
def proveedores_eliminar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM proveedores WHERE id=%s", (id,))
    db.commit(); cur.close(); db.close()
    return redirect(url_for("proveedores_list"))

# --------- CRUD PRODUCTOS ---------
@app.route("/productos")
def productos_list():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT p.*, pr.empresa AS proveedor_nombre
        FROM productos p
        LEFT JOIN proveedores pr ON pr.id = p.proveedor_id
        ORDER BY p.id DESC
    """)
    rows = cur.fetchall()
    cur.close(); db.close()
    return render_template("productos_list.html", productos=rows)

@app.route("/productos/nuevo", methods=["GET", "POST"])
def productos_nuevo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method == "POST":
        codigo = request.form["codigo"]
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        stock = request.form.get("stock")
        proveedor_id = request.form.get("proveedor_id") or None
        cur2 = db.cursor()
        cur2.execute("INSERT INTO productos (codigo, descripcion, precio, stock, proveedor_id) VALUES (%s,%s,%s,%s,%s)",
                     (codigo, descripcion, precio, stock, proveedor_id))
        db.commit(); cur2.close(); cur.close(); db.close()
        return redirect(url_for("productos_list"))
    cur.execute("SELECT id, empresa FROM proveedores ORDER BY empresa")
    proveedores = cur.fetchall(); cur.close(); db.close()
    return render_template("productos_form.html", data=None, proveedores=proveedores)

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def productos_editar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method == "POST":
        codigo = request.form["codigo"]
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        stock = request.form.get("stock")
        proveedor_id = request.form.get("proveedor_id") or None
        cur.execute("UPDATE productos SET codigo=%s, descripcion=%s, precio=%s, stock=%s, proveedor_id=%s WHERE id=%s",
                    (codigo, descripcion, precio, stock, proveedor_id, id))
        db.commit(); cur.close(); db.close()
        return redirect(url_for("productos_list"))
    cur.execute("SELECT * FROM productos WHERE id=%s", (id,))
    row = cur.fetchone()
    cur.execute("SELECT id, empresa FROM proveedores ORDER BY empresa")
    proveedores = cur.fetchall(); cur.close(); db.close()
    return render_template("productos_form.html", data=row, proveedores=proveedores)

@app.route("/productos/eliminar/<int:id>")
def productos_eliminar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM productos WHERE id=%s", (id,))
    db.commit(); cur.close(); db.close()
    return redirect(url_for("productos_list"))

# --------- CRUD SERVICIOS ---------
@app.route("/servicios")
def servicios_list():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM servicios ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close(); db.close()
    return render_template("servicios_list.html", servicios=rows)

@app.route("/servicios/nuevo", methods=["GET", "POST"])
def servicios_nuevo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        tecnico = request.form.get("tecnico_asignado")
        costo = request.form.get("costo")
        tiempo = request.form.get("tiempo_estimado")
        db = get_db(); cur = db.cursor()
        cur.execute("INSERT INTO servicios (nombre, tecnico_asignado, costo, tiempo_estimado) VALUES (%s,%s,%s,%s)",
                    (nombre, tecnico, costo, tiempo))
        db.commit(); cur.close(); db.close()
        return redirect(url_for("servicios_list"))
    return render_template("servicios_form.html", data=None)

@app.route("/servicios/editar/<int:id>", methods=["GET", "POST"])
def servicios_editar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor(dictionary=True)
    if request.method == "POST":
        nombre = request.form["nombre"]
        tecnico = request.form.get("tecnico_asignado")
        costo = request.form.get("costo")
        tiempo = request.form.get("tiempo_estimado")
        cur.execute("UPDATE servicios SET nombre=%s, tecnico_asignado=%s, costo=%s, tiempo_estimado=%s WHERE id=%s",
                    (nombre, tecnico, costo, tiempo, id))
        db.commit(); cur.close(); db.close()
        return redirect(url_for("servicios_list"))
    cur.execute("SELECT * FROM servicios WHERE id=%s", (id,))
    row = cur.fetchone(); cur.close(); db.close()
    return render_template("servicios_form.html", data=row)

@app.route("/servicios/eliminar/<int:id>")
def servicios_eliminar(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db(); cur = db.cursor()
    cur.execute("DELETE FROM servicios WHERE id=%s", (id,))
    db.commit(); cur.close(); db.close()
    return redirect(url_for("servicios_list"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



