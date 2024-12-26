from flask import Flask, redirect, render_template, url_for, redirect, session, request,  flash, get_flashed_messages, Response
from mysql import connector
from werkzeug.security import generate_password_hash, check_password_hash 
from werkzeug.utils import secure_filename
import os
import time
import random
import openpyxl
from io import BytesIO
app = Flask (__name__)

app.secret_key = 'rodip'

#konek ke database
db = connector.connect(
    user="rodip", 
    password="Rentalmobil123#", 
    host="pbdrent.mysql.database.azure.com", 
    port=3306, database="fp_rentalmobil"
)
if db.is_connected():
    print('berhasil konek ke database')


id_pelanggan = ''
#halaman awal
@app.route('/')
def landing():
    cursor = db.cursor()
    cursor.execute('SELECT merk, bahan_bakar, gambar from daftar_mobil order by rand()')
    daftar_mobil_landing = cursor.fetchall()
    return render_template('landing.html', landing = daftar_mobil_landing)

#halaman admin
@app.route('/admin/', methods =['GET', 'POST'])
def admin_login():
    mesage = ''
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            cursor = db.cursor()
            cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                session['loggedin'] = True
                session['id'] = user[0]
                session['username'] = user[1]
                mesage = 'Logged in successfully !'
                return redirect(url_for('dashboard'))
            else:
                if username == "" or password =="":
                    mesage = 'Username/password Kosong'
                else:
                    mesage = 'Username/password Salah'
    return render_template('admin_login.html', mesage = mesage)

# Halaman admin dashboard
@app.route('/dashboard')
def dashboard():
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM daftar_mobil")
    total_mobil = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM driver")
    total_driver = cursor.fetchone()[0]
    
    cursor.close()
    
    return render_template('dashboard.html', total_mobil=total_mobil, total_driver=total_driver, username = session['username'])


#untuk logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('admin_login'))

# Direktori untuk menyimpan file yang diunggah
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan direktori untuk menyimpan file sudah ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Direktori untuk menyimpan file yang diunggah
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan direktori untuk menyimpan file sudah ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/detail_mobil', methods=['GET', 'POST'])
def detail_mobil():
    if request.method == 'POST':
        kode_mobil = request.form['kode_mobil']
        plat_no = request.form['plat_no']
        merk = request.form['merk']
        sewa_per_hari = request.form['sewa_per_hari']
        status = request.form['status']
        bahan_bakar = request.form['bahan_bakar']
        gambar = request.files['gambar']

        # Simpan file gambar ke folder static/images
        if gambar:
            gambar_filename = secure_filename(gambar.filename)
            gambar_path = os.path.join(app.config['UPLOAD_FOLDER'], gambar_filename)
            gambar.save(gambar_path)

        # Debug print untuk memastikan nilai status diterima
        print(f"Kode Mobil: {kode_mobil}, Plat No: {plat_no}, Merk: {merk}, Sewa Per Hari: {sewa_per_hari}, Status: {status}, Bahan Bakar: {bahan_bakar}, Gambar: {gambar_filename}")

        # Cek apakah semua field sudah diisi
        if not all([kode_mobil, plat_no, merk, sewa_per_hari, status, bahan_bakar, gambar]):
            flash('Semua field harus diisi!', 'error')
        else:
            try:
                cursor = db.cursor()

                # Query untuk tabel detail_mobil
                insert_query_detail = """
                INSERT INTO detail_mobil (kode_mobil, plat_no, sewa_per_hari, status) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query_detail, (kode_mobil, plat_no, sewa_per_hari, status))

                # Query untuk tabel daftar_mobil
                insert_query_daftar = """
                INSERT INTO daftar_mobil (kode_mobil, merk, bahan_bakar, gambar) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query_daftar, (kode_mobil, merk, bahan_bakar, gambar_filename))

                # Commit transaksi jika kedua query berhasil
                db.commit()
                cursor.close()
                flash('Mobil berhasil ditambahkan', 'success')
            except Exception as e:
                # Rollback transaksi jika terjadi kesalahan
                db.rollback()
                flash('Terjadi kesalahan saat menambahkan mobil', 'error')
                print("Error:", e)

                
    return render_template('detail_mobil.html')
 # menambahkan data mobil
@app.route('/tambah_plat/<kode_mobil>', methods=['GET', 'POST'])
def tambah_plat(kode_mobil):
    cursor=db.cursor()
    cursor.execute('select * from daftar_mobil where kode_mobil=%s',(kode_mobil,))
    mobil = cursor.fetchone()
    if request.method == 'POST':
        plat_no = request.form['plat_no_baru']
        sewa_per_hari = request.form['sewa_per_hari']
        status = request.form['status']
        try:
            cursor = db.cursor()

            # Query untuk tabel tambah_plat
            insert_query_detail = """
            INSERT INTO detail_mobil (kode_mobil, plat_no, sewa_per_hari, status) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query_detail, (kode_mobil, plat_no, sewa_per_hari, status))

            # Commit transaksi jika kedua query berhasil
            db.commit()
            cursor.close()
            flash('Mobil berhasil ditambahkan', 'success')
        except Exception as e:
            # Rollback transaksi jika terjadi kesalahan
            db.rollback()
            flash('Terjadi kesalahan saat menambahkan mobil', 'error')
            print("Error:", e)

    return render_template('tambah_plat.html', mobil=mobil)

@app.route('/update_plat/<plat_no>', methods=['GET','POST'])
def update_plat(plat_no):
    if request.method == 'POST':
        plat_no_baru = request.form['plat_no']
        sewa_per_hari = request.form['sewa_per_hari']
        status = request.form['status']

        try:
            cursor = db.cursor()

            # Update query untuk tabel detail_mobil
            update_query_detail = """
            UPDATE detail_mobil
            SET plat_no=%s, sewa_per_hari=%s, status=%s
            WHERE plat_no=%s
            """
            cursor.execute(update_query_detail, (plat_no_baru, sewa_per_hari, status, plat_no))

            db.commit()
            cursor.close()
            flash('Plat berhasil diperbarui', 'success')
        except Exception as e:
            # Rollback transaksi jika terjadi kesalahan
            db.rollback()
            flash('Terjadi kesalahan saat memperbarui mobil', 'error')
            print("Error:", e)

        return redirect(url_for('update_plat', plat_no = plat_no))
    cursor=db.cursor()
    cursor.execute('select plat_no, sewa_per_hari, status from detail_mobil where plat_no=%s', (plat_no,))
    platdetail = cursor.fetchone()
    return render_template('update_plat.html', platdetail = platdetail)

@app.route('/listmobil/<kode_mobil>/delete_plat/<plat_no>', methods=['GET'])
def delete_plat(kode_mobil,plat_no):
    cursor=db.cursor()
    cursor.execute('delete from detail_mobil where plat_no=%s', (plat_no,))
    db.commit()
    return redirect(url_for('mobil'))


@app.route('/listmobil/<kode_mobil>', methods=['GET','POST'])
def listmobil(kode_mobil):
    if request.method == 'POST':
        merk = request.form['merk']
        bahan_bakar = request.form['bahan_bakar']
        gambar = request.files['gambar']
        gambar_filename = None
        # Simpan file gambar ke folder static/images jika ada file yang diunggah
        if gambar:
            gambar_filename = secure_filename(gambar.filename)
            gambar_path = os.path.join(app.config['UPLOAD_FOLDER'], gambar_filename)
            gambar.save(gambar_path)

        # Debug print untuk memastikan nilai status diterima
        #print(f"Kode Mobil: {kode_mobil}, Plat No: {plat_no}, Merk: {merk}, Sewa Per Hari: {sewa_per_hari}, Status: {status}, Bahan Bakar: {bahan_bakar}, Gambar: {gambar_filename}")

        try:
            cursor = db.cursor()
            # Update query untuk tabel daftar_mobil
            if gambar_filename:
                update_query_daftar = """
                UPDATE daftar_mobil
                SET merk=%s, bahan_bakar=%s, gambar=%s
                WHERE kode_mobil=%s
                """
                cursor.execute(update_query_daftar, (merk, bahan_bakar, gambar_filename, kode_mobil))
            else:
                update_query_daftar = """
                UPDATE daftar_mobil
                SET merk=%s, bahan_bakar=%s
                WHERE kode_mobil=%s
                """
                cursor.execute(update_query_daftar, (merk, bahan_bakar, kode_mobil))

            # Commit transaksi jika kedua query berhasil
            db.commit()
            cursor.close()
            flash('Mobil berhasil diperbarui', 'success')
        except Exception as e:
            # Rollback transaksi jika terjadi kesalahan
            db.rollback()
            flash('Terjadi kesalahan saat memperbarui mobil', 'error')
            print("Error:", e)

        return redirect(url_for('listmobil',kode_mobil=kode_mobil))
    cursor=db.cursor()
    cursor.execute('select * from daftar_mobil where kode_mobil=%s',(kode_mobil,))
    detail = cursor.fetchone()
    cursor.execute('select plat_no, sewa_per_hari, status from detail_mobil where kode_mobil=%s', (kode_mobil,))
    listmobil = cursor.fetchall()
    return render_template('listmobil.html', listmobil = listmobil, detail = detail)

# Rute untuk menampilkan dan menambahkan mobil
@app.route('/mobil', methods=['GET', 'POST'])
def mobil():
    cursor = db.cursor()
    cursor.execute("select daftar_mobil.kode_mobil,merk,gambar, detail_mobil.sewa_per_hari, status, (select count(plat_no) from detail_mobil where detail_mobil.kode_mobil=daftar_mobil.kode_mobil) as stok from daftar_mobil inner join detail_mobil on daftar_mobil.kode_mobil = detail_mobil.kode_mobil group by kode_mobil;")
    mobil_data = cursor.fetchall()
    cursor.close()

    return render_template('mobil.html', mobil_data=mobil_data)


@app.route('/delete_mobil/<kode_mobil>', methods=['POST'])
def delete_mobil(kode_mobil):
    try:
        cursor = db.cursor()

        # Hapus data dari tabel detail_mobil
        delete_query_detail = "DELETE FROM detail_mobil WHERE kode_mobil = %s"
        cursor.execute(delete_query_detail, (kode_mobil,))

        # Hapus data dari tabel daftar_mobil
        delete_query_daftar = "DELETE FROM daftar_mobil WHERE kode_mobil = %s"
        cursor.execute(delete_query_daftar, (kode_mobil,))

        # Commit transaksi jika kedua query berhasil
        db.commit()
        cursor.close()
        flash('Mobil berhasil dihapus', 'success')
    except Exception as e:
        # Rollback transaksi jika terjadi kesalahan
        db.rollback()
        flash('Terjadi kesalahan saat menghapus mobil', 'error')
        print("Error:", e)

    return redirect(url_for('mobil'))


@app.route('/update_mobil/<kode_mobil>', methods=['GET', 'POST'])
def update_mobil(kode_mobil):
    if request.method == 'POST':
        plat_no = request.form['plat_no']
        merk = request.form['merk']
        sewa_per_hari = request.form['sewa_per_hari']
        status = request.form['status']
        bahan_bakar = request.form['bahan_bakar']
        gambar = request.files['gambar']
        gambar_filename = None

        # Simpan file gambar ke folder static/images jika ada file yang diunggah
        if gambar:
            gambar_filename = secure_filename(gambar.filename)
            gambar_path = os.path.join(app.config['UPLOAD_FOLDER'], gambar_filename)
            gambar.save(gambar_path)

        # Debug print untuk memastikan nilai status diterima
        print(f"Kode Mobil: {kode_mobil}, Plat No: {plat_no}, Merk: {merk}, Sewa Per Hari: {sewa_per_hari}, Status: {status}, Bahan Bakar: {bahan_bakar}, Gambar: {gambar_filename}")

        try:
            cursor = db.cursor()

            # Update query untuk tabel detail_mobil
            update_query_detail = """
            UPDATE detail_mobil
            SET plat_no=%s, sewa_per_hari=%s, status=%s
            WHERE kode_mobil=%s
            """
            cursor.execute(update_query_detail, (plat_no, sewa_per_hari, status, kode_mobil))

            # Update query untuk tabel daftar_mobil
            if gambar_filename:
                update_query_daftar = """
                UPDATE daftar_mobil
                SET merk=%s, bahan_bakar=%s, gambar=%s
                WHERE kode_mobil=%s
                """
                cursor.execute(update_query_daftar, (merk, bahan_bakar, gambar_filename, kode_mobil))
            else:
                update_query_daftar = """
                UPDATE daftar_mobil
                SET merk=%s, bahan_bakar=%s
                WHERE kode_mobil=%s
                """
                cursor.execute(update_query_daftar, (merk, bahan_bakar, kode_mobil))

            # Commit transaksi jika kedua query berhasil
            db.commit()
            cursor.close()
            flash('Mobil berhasil diperbarui', 'success')
        except Exception as e:
            # Rollback transaksi jika terjadi kesalahan
            db.rollback()
            flash('Terjadi kesalahan saat memperbarui mobil', 'error')
            print("Error:", e)

        return redirect(url_for('detail_mobil'))

    # Metode GET: mengambil data mobil yang akan diperbarui
    try:
        cursor = db.cursor()
        cursor.execute("""
        SELECT d.kode_mobil, d.plat_no, dm.merk, d.sewa_per_hari, d.status, dm.bahan_bakar, dm.gambar
        FROM detail_mobil d
        JOIN daftar_mobil dm ON d.kode_mobil = dm.kode_mobil
        WHERE d.kode_mobil = %s
        """, (kode_mobil,))
        mobil = cursor.fetchone()
        cursor.close()
    except Exception as e:
        flash('Terjadi kesalahan saat mengambil data mobil', 'error')
        print("Error:", e)
        return redirect(url_for('detail_mobil'))

    return render_template('update_mobil.html', mobil=mobil)

@app.route('/driver', methods=['GET'])
def driver():
        # Ambil semua data driver dari database
        cursor = db.cursor()
        cursor.execute("SELECT id_driver, name, alamat, phone, tahun_lahir, lisensi, sewa_per_hari, image FROM driver")
        drivers = cursor.fetchall()
        cursor.close()

        # Kirim data ke template
        return render_template('driver.html', drivers=drivers)

@app.route('/tambah_driver', methods=['GET', 'POST'])
def tambah_driver():
    if request.method == 'POST':
        # Ambil data dari form
        name = request.form['name']
        alamat = request.form['alamat']
        phone = request.form['phone']
        tahun_lahir = request.form['tahun_lahir']
        lisensi = request.form['lisensi']
        sewa_per_hari = request.form['sewa_per_hari']
        image = request.files['image']

        if image:
            # Simpan file dengan nama yang aman
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            try:
                cursor = db.cursor()
                cursor.execute("INSERT INTO driver (name, alamat, phone, tahun_lahir, lisensi, sewa_per_hari, image) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                               (name, alamat, phone, tahun_lahir, lisensi, sewa_per_hari, filename))
                db.commit()
                cursor.close()
                flash('Driver berhasil ditambahkan', 'success')
            except Exception as e:
                flash('Terjadi kesalahan saat menambahkan driver', 'error')
                print("Error:", e)

    return render_template('tambah_driver.html')


@app.route('/update_driver/<id_driver>', methods=['GET', 'POST'])
def update_driver(id_driver):
    cursor = db.cursor()
    if request.method == 'POST':
        name = request.form['name']
        alamat = request.form['alamat']
        phone = request.form['phone']
        umur_lahir = request.form['umur_lahir']
        lisensi = request.form['lisensi']
        sewa_per_hari = request.form['Sewa_per_hari']
        image = request.files['image']

        # Save new image if uploaded
        image_filename = None
        if image and image.filename != '':
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

        try:
            # Update driver data
            if image_filename:
                update_query = """
                UPDATE driver 
                SET name=%s, alamat=%s, phone=%s, tahun_lahir=%s, lisensi=%s, sewa_per_hari=%s, image=%s
                WHERE id_driver=%s
                """
                cursor.execute(update_query, (name, alamat, phone, umur_lahir, lisensi, sewa_per_hari, image_filename, id_driver))
            else:
                update_query = """
                UPDATE driver 
                SET name=%s, alamat=%s, phone=%s, tahun_lahir=%s, lisensi=%s, sewa_per_hari=%s
                WHERE id_driver=%s
                """
                cursor.execute(update_query, (name, alamat, phone, umur_lahir, lisensi, sewa_per_hari, id_driver))

            db.commit()
            flash('Driver berhasil diperbarui', 'success')
        except Exception as e:
            db.rollback()
            flash('Terjadi kesalahan saat memperbarui driver', 'error')
            print("Error:", e)

        return redirect(url_for('driver'))

    # Metode GET: mengambil data driver yang akan diperbarui
    try:
        cursor.execute("SELECT * FROM driver WHERE id_driver = %s", (id_driver,))
        driver = cursor.fetchone()
        cursor.close()
    except Exception as e:
        flash('Terjadi kesalahan saat mengambil data driver', 'error')
        print("Error:", e)
        return redirect(url_for('driver'))

    return render_template('update_driver.html', driver=driver)

@app.route('/delete_driver/<id_driver>', methods=['POST'])
def delete_driver(id_driver):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM driver WHERE id_driver = %s", (id_driver,))
        db.commit()
        flash('Driver berhasil dihapus', 'success')
    except Exception as e:
        db.rollback()
        flash('Terjadi kesalahan saat menghapus driver', 'error')
        print("Error:", e)
    return redirect(url_for('driver'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'id' not in session:
        flash('You need to login first.', 'error')
        return redirect(url_for('admin_login'))
    
    admin_id = session['id']

    cursor = db.cursor()
    cursor.execute("SELECT username, password FROM admin WHERE admin_id = %s", (admin_id,))
    admin = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        # Ambil data dari form
        username = request.form['username']
        password = request.form['password']

        try:
            cursor = db.cursor()
            cursor.execute("UPDATE admin SET username=%s, password=%s WHERE admin_id=%s",
                           (username, password, admin_id))
            db.commit()
            cursor.close()
            flash('Profile updated successfully', 'success')
            return render_template('profile.html', username = session['username'])
        except Exception as e:
            flash('Error updating profile', 'error')
            print("Error:", e)
        
    return render_template('profile.html', admin=admin, username = session['username'])

@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    mesage = ''
    if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            cursor = db.cursor()
            cursor.execute('SELECT * FROM pelanggan WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                session['loggedin'] = True
                session['id_pelanggan'] = user[0]
                session['email'] = user[2]
                mesage = 'Logged in successfully !'
                return redirect(url_for('daftar_mobil'))
            else:
                if email == "" or password =="":
                    mesage = 'email/password Kosong'
                else:
                    mesage = 'email/password Salah'
    return render_template('signin.html', mesage = mesage)
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nama = request.form.get('nama')
        email = request.form.get('email')
        password = request.form.get('password')

        if not nama or not email or not password:
            flash('Please fill out all fields')
            return redirect(url_for('signup'))

        cursor = db.cursor()
        # Check if the email already exists
        cursor.execute("SELECT * FROM pelanggan WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash('Email address already exists')
            return redirect(url_for('signup'))
        
        cursor = db.cursor()
        # Insert the new user into the database
        insert_query = "INSERT INTO pelanggan (nama, email, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (nama, email, password))
        db.commit()
        cursor.close()
        flash('Registration successful!','success')
        return redirect(url_for('signin'))
    
    return render_template('signup.html')

@app.route('/profileuser/', methods=['GET', 'POST'])
def profileuser():
    id_pelanggan = session.get('id_pelanggan')
    if not id_pelanggan:
        flash('User not logged in', 'error')
        return redirect(url_for('signin'))

    cursor = db.cursor()
    cursor.execute("SELECT * FROM pelanggan WHERE id_pelanggan = %s", (id_pelanggan,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

    return render_template('profileuser.html', user=user)
    

@app.route('/signout')
def signout():
    session.pop('loggedin', None)
    session.pop('email', None)
    id_pelanggan = session.get('id_pelanggan')
    if id_pelanggan!='' or id_pelanggan!=None:
        session['id_pelanggan'] = ''
    return redirect(url_for('signin'))

@app.route('/daftar_mobil/', methods=['GET', 'POST'])
def daftar_mobil():
    email = ''
    if request.method == 'POST':
        kode_mobil = request.form.get('kode_mobil')
        merk = request.form.get('merk')
        id_pelanggan = session['id_pelanggan']
        sewa_per_hari = request.form.get('sewa_per_hari')

        cursor = db.cursor()
        cursor.execute("INSERT INTO keranjang (kode_mobil,merk, mobil_per_hari, id_pelanggan) VALUES (%s, %s, %s, %s)", 
                               (kode_mobil, merk, sewa_per_hari, id_pelanggan))
        db.commit()
        cursor.close()
        flash('Registration successful!','success')
    cursor = db.cursor()
    cursor.execute("select id_driver, name from driver")
    drivers = cursor.fetchall()
    cursor.close()
    cursor = db.cursor()
    cursor.execute('SELECT daftar_mobil.kode_mobil,merk,bahan_bakar,gambar, detail_mobil.sewa_per_hari from daftar_mobil join detail_mobil on daftar_mobil.kode_mobil = detail_mobil.kode_mobil where detail_mobil.status="Ready" group by kode_mobil')
    daftar_mobil_landinguser = cursor.fetchall()
    if email == '':
        return render_template('daftar_mobil.html', landinguser = daftar_mobil_landinguser)
    return render_template('daftar_mobil.html', drivers = drivers, landinguser = daftar_mobil_landinguser, email = session['email'])

@app.route('/daftar_driver/', methods=['GET', 'POST'])
def daftar_driver():
    email = ''
    cursor = db.cursor()
    cursor.execute('SELECT * from driver')
    daftar_driver_landinguser = cursor.fetchall()
    if email == '':
        return render_template('daftar_driver.html', landinguser = daftar_driver_landinguser)
    return render_template('daftar_driver.html', landinguser = daftar_driver_landinguser, email = session['email'])

@app.route('/daftaradmin', methods=['GET', 'POST'])
def daftaradmin():
    return render_template('daftaradmin.html')

@app.route('/keranjang/', methods=['GET', 'POST'])
def keranjang():
    id_pelanggan = session.get('id_pelanggan')
    
    # Cek apakah pengguna telah login
    if not id_pelanggan:
        flash('Anda harus signin terlebih dahulu.', 'error')
        return redirect(url_for('signin'))

    if request.method == 'POST':
        id_driver = request.form.get('driver')
        id_order = request.form.get('id_order')

        if not id_driver or not id_order:
            flash('Data tidak lengkap.', 'error')
            return redirect(url_for('keranjang'))

        cursor = db.cursor()
        cursor.execute("SELECT * FROM driver WHERE id_driver = %s", (id_driver,))
        nilai = cursor.fetchone()
        if nilai:
            cursor.execute("""
                UPDATE keranjang 
                SET id_driver = %s, name = %s, driver_per_hari = %s 
                WHERE id_order = %s
            """, (id_driver, nilai[1], nilai[6], id_order))
            db.commit()
            flash('Driver berhasil ditambahkan!', 'success')
        else:
            flash('Driver tidak ditemukan.', 'error')
        cursor.close()

    cursor = db.cursor()
    cursor.execute('SELECT id_order, merk, mobil_per_hari, name, driver_per_hari FROM keranjang WHERE id_pelanggan = %s', (id_pelanggan,))
    item = cursor.fetchall()

    cursor.execute('SELECT id_driver, name, sewa_per_hari, lisensi FROM driver WHERE id_driver NOT IN (SELECT id_driver FROM keranjang WHERE id_pelanggan = %s)', (id_pelanggan,))
    drivers = cursor.fetchall()

    cursor.close()
    return render_template('keranjang.html', keranjang_item=item, drivers=drivers)

@app.route('/keranjang/hapus/<id_order>', methods=['GET'])
def hapus_data(id_order):
    cursor=db.cursor()
    cursor.execute('DELETE from keranjang where id_order=%s', (id_order,))
    db.commit()
    return redirect(url_for('keranjang'))

@app.route('/transaksi/', methods=['GET', 'POST'])
def transaksi():
    id_pelanggan = session.get('id_pelanggan')
    if not id_pelanggan:
        flash('Anda harus login terlebih dahulu.', 'error')
        return redirect(url_for('signin'))

    cursor = db.cursor()
    cursor.execute('SELECT transaksi.id_order, daftar_mobil.merk, driver.name, transaksi.tanggal_mulai,durasi,total, transaksi.alamat,status FROM transaksi join daftar_mobil on transaksi.kode_mobil=daftar_mobil.kode_mobil left join driver on transaksi.id_driver = driver.id_driver WHERE id_pelanggan = %s', (id_pelanggan,))
    item = cursor.fetchall()

    cursor.close()
    return render_template('transaksi.html', keranjang_item=item)

@app.route('/pesanan', methods=['GET', 'POST'])
def pesanan():
    id_pelanggan = session.get('id_pelanggan')
    cursor = db.cursor()
    if request.method == 'POST':
        tanggal_mulai = request.form.get('tanggal_mulai')
        alamat = request.form.get('alamat')
        cursor.execute('select * from keranjang where id_pelanggan=%s', (id_pelanggan,))
        isidata = cursor.fetchall()
        totalhari=0
        for kolom in isidata:
            durasi = request.form['durasi']
            durasi_int = int(durasi)
            totalhari = kolom[4]+kolom[7]
            cursor = db.cursor()
            cursor.execute("INSERT INTO transaksi (id_order, id_pelanggan, kode_mobil, id_driver, tanggal_mulai, durasi, total, alamat, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Menunggu Persetujuan')", 
                               (kolom[0], id_pelanggan, kolom[2], kolom[5], tanggal_mulai, durasi, totalhari * durasi_int, alamat, ))
            db.commit()
            cursor.execute('DELETE from keranjang where id_order=%s', (kolom[0],))
            #cursor.execute("SELECT total from transaksi where id_transaksi=%s", (kolom[0],))\
            random_number_identifier = random.randint(1,1000)
            totalpayment = (totalhari*durasi_int)+random_number_identifier
            print(totalpayment)
            cursor.close()
            durasi = 0
            flash('Registration successful!','success')
    return render_template('pesanan.html', totalpayment = totalpayment)


@app.route('/adminproses', methods=['GET', 'POST'])
def proses():
    cursor = db.cursor()
    cursor.execute('SELECT transaksi.id_transaksi,id_order, pelanggan.nama, daftar_mobil.merk, driver.name, transaksi.tanggal_mulai,durasi,total, transaksi.alamat, status FROM transaksi join pelanggan on transaksi.id_pelanggan=pelanggan.id_pelanggan join daftar_mobil on transaksi.kode_mobil = daftar_mobil.kode_mobil left join driver on transaksi.id_driver = driver.id_driver where transaksi.status = "Menunggu Persetujuan"')
    transaksis = cursor.fetchall()
    cursor.close()
    return render_template('adminproses.html', transaksis=transaksis)

@app.route('/proses_transaksi/<id_transaksi>', methods=['POST'])
def proses_transaksi(id_transaksi):
    cursor = db.cursor()
    try:
        cursor.execute('UPDATE transaksi SET status=%s WHERE id_transaksi=%s', ('Transaksi diproses', id_transaksi))
        db.commit()
        flash('Transaksi berhasil diproses', 'success')
    except Exception as e:
        db.rollback()
        flash('Terjadi kesalahan saat memproses transaksi', 'error')
        print("Error:", e)
    cursor.close()
    return redirect(url_for('proses'))

@app.route('/acc_transaksi/<id_transaksi>', methods=['POST'])
def acc_transaksi(id_transaksi):
    cursor = db.cursor()
    try:
        cursor.execute('UPDATE transaksi SET status=%s WHERE id_transaksi=%s', ('Transaksi berlangsung', id_transaksi))
        db.commit()
        flash('Transaksi berhasil disetujui', 'success')
    except Exception as e:
        db.rollback()
        flash('Terjadi kesalahan saat menyetujui transaksi', 'error')
        print("Error:", e)
    cursor.close()
    return redirect(url_for('proses'))
    
@app.route('/tolak_transaksi/<id_transaksi>', methods=['POST'])
def tolak_transaksi(id_transaksi):
    cursor = db.cursor()
    try:
        cursor.execute('UPDATE transaksi SET status=%s WHERE id_transaksi=%s', ('Transaksi ditolak', id_transaksi))
        db.commit()
        flash('Transaksi berhasil disetujui', 'success')
    except Exception as e:
        db.rollback()
        flash('Terjadi kesalahan saat menyetujui transaksi', 'error')
        print("Error:", e)
    cursor.close()
    return redirect(url_for('proses'))

@app.route('/transaksi_berlangsung', methods=['GET', 'POST'])
def transaksi_berlangsung():
    cursor = db.cursor()
    cursor.execute('SELECT transaksi.id_transaksi,id_order, pelanggan.nama, daftar_mobil.merk, driver.name, transaksi.tanggal_mulai,durasi,total,transaksi.alamat, status FROM transaksi join pelanggan on transaksi.id_pelanggan=pelanggan.id_pelanggan join daftar_mobil on transaksi.kode_mobil = daftar_mobil.kode_mobil left join driver on transaksi.id_driver = driver.id_driver where transaksi.status ="Transaksi berlangsung"')
    transaksis = cursor.fetchall()
    cursor.close()
    return render_template('transaksiberlangsung.html', transaksis=transaksis)

@app.route('/selesai_transaksi/<id_transaksi>', methods=['POST'])
def selesai_transaksi(id_transaksi):
    cursor = db.cursor()
    try:
        cursor.execute('UPDATE transaksi SET status=%s WHERE id_transaksi=%s', ('Transaksi selesai', id_transaksi))
        db.commit()
        flash('Transaksi berhasil disetujui', 'success')
    except Exception as e:
        db.rollback()
        flash('Terjadi kesalahan saat menyetujui transaksi', 'error')
        print("Error:", e)
    cursor.close()
    return redirect(url_for('transaksi_berlangsung'))

@app.route('/transaksi_selesai', methods=['GET', 'POST'])
def transaksi_selesai():
    cursor = db.cursor()
    cursor.execute('''
        SELECT transaksi.id_transaksi, id_order, pelanggan.nama, daftar_mobil.merk, 
               driver.name, transaksi.tanggal_mulai, durasi, total, transaksi.alamat, status 
        FROM transaksi 
        JOIN pelanggan ON transaksi.id_pelanggan = pelanggan.id_pelanggan 
        JOIN daftar_mobil ON transaksi.kode_mobil = daftar_mobil.kode_mobil 
        LEFT JOIN driver ON transaksi.id_driver = driver.id_driver 
        WHERE transaksi.status IN ("Transaksi selesai", "Transaksi ditolak")
    ''')
    transaksis = cursor.fetchall()
    cursor.close()

    # Jika POST request, ekspor data ke Excel
    if request.method == 'POST':
        # Buat workbook baru
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Transaksi Selesai"

        # Tambahkan header
        headers = [
            "ID Transaksi", "ID Order", "Nama Pelanggan", "Merk Mobil",
            "Nama Driver", "Tanggal Mulai", "Durasi (Hari)", "Total (Rp)", "Alamat", "Status"
        ]
        sheet.append(headers)

        # Tambahkan data transaksi
        for transaksi in transaksis:
            sheet.append(list(transaksi))

        # Simpan file ke buffer
        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        # Kirim file sebagai respons
        return Response(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment;filename=transaksi_selesai.xlsx"
            }
        )

    # Jika GET request, render halaman HTML
    return render_template('transaksiselesai.html', transaksis=transaksis)
if __name__ =='__main__':
    app.run(debug=True)

