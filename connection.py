from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "argyanggara22"


# Fungsi koneksi MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost", user="root", password="", database="db_koperasi"
    )
    return connection


# Fungsi format Rupiah
def format_rupiah(amount):
    return "Rp {:,}".format(amount).replace(",", ".")
app.jinja_env.filters["rupiah"] = format_rupiah


# Halaman index (beranda) setelah login
@app.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))


# Halaman About
@app.route("/ab")
def about():
    if "user_id" in session:
        return render_template("about.html")
    else:
        return redirect(url_for("login"))


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login berhasil!", "success")
            return redirect(url_for("index"))
        else:
            flash("Username atau password salah.", "danger")

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for("login"))


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password),
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Pendaftaran berhasil, silakan login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# Tampilkan data anggota
@app.route("/anggota")
def anggota():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM anggota")
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("anggota.html", users=users)


# Tambah data anggota
@app.route("/anggota/tambah", methods=["GET", "POST"])
def tambah_anggota():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nama = request.form["nama"]
        alamat = request.form["alamat"]
        no_hp = request.form["no_hp"]

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO anggota (nama, alamat, no_hp) VALUES (%s, %s, %s)",
            (nama, alamat, no_hp),
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Anggota baru berhasil ditambahkan.", "success")
        return redirect(url_for("anggota"))

    return render_template("tambah_anggota.html")


# Edit data anggota
@app.route("/anggota/edit/<int:id>", methods=["GET", "POST"])
def edit_anggota(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM anggota WHERE id = %s", (id,))
    anggota = cursor.fetchone()
    cursor.close()

    if request.method == "POST":
        nama = request.form["nama"]
        alamat = request.form["alamat"]
        no_hp = request.form["no_hp"]

        cursor = connection.cursor()
        cursor.execute(
            "UPDATE anggota SET nama = %s, alamat = %s, no_hp = %s WHERE id = %s",
            (nama, alamat, no_hp, id),
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Data anggota berhasil diperbarui.", "success")
        return redirect(url_for("anggota"))

    return render_template("edit_anggota.html", anggota=anggota)


# Hapus data anggota
@app.route("/anggota/hapus/<int:id>", methods=["POST"])
def hapus_anggota(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM anggota WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Anggota berhasil dihapus.", "success")
    return redirect(url_for("anggota"))


# Tampilkan data transaksi
@app.route("/transaksi")
def transaksi():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transaksi")
    transactions = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("transaksi.html", transactions=transactions)


# Tambah data transaksi
@app.route("/transaksi/tambah", methods=["GET", "POST"])
def tambah_transaksi():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        id_anggota = request.form["id_anggota"]
        jenis_transaksi = request.form["jenis_transaksi"]
        jumlah = request.form["jumlah"]

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO transaksi (id_anggota, jenis_transaksi, jumlah) VALUES (%s, %s, %s)",
            (id_anggota, jenis_transaksi, jumlah),
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Transaksi berhasil ditambahkan.", "success")
        return redirect(url_for("transaksi"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM anggota")
    anggota = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("tambah_transaksi.html", anggota=anggota)


# Edit data transaksi
@app.route("/transaksi/edit/<int:id>", methods=["GET", "POST"])
def edit_transaksi(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transaksi WHERE id = %s", (id,))
    transaksi = cursor.fetchone()

    if request.method == "POST":
        jenis_transaksi = request.form["jenis_transaksi"]
        jumlah = request.form["jumlah"]

        cursor = connection.cursor()
        cursor.execute(
            "UPDATE transaksi SET jenis_transaksi = %s, jumlah = %s WHERE id = %s",
            (jenis_transaksi, jumlah, id),
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Transaksi berhasil diperbarui.", "success")
        return redirect(url_for("transaksi"))

    cursor.execute("SELECT * FROM anggota")
    anggota = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("edit_transaksi.html", transaksi=transaksi, anggota=anggota)


# Hapus data transaksi
@app.route("/transaksi/hapus/<int:id>", methods=["POST"])
def hapus_transaksi(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM transaksi WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Transaksi berhasil dihapus.", "success")
    return redirect(url_for("transaksi"))


if __name__ == "__main__":
    app.run(debug=True)
