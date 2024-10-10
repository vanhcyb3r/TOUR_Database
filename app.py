from flask import Flask, render_template, request, redirect
import mysql.connector


app = Flask(__name__)

# Hàm kết nối với MySQL
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='quanlytourdulich',
        user='root',  # Tên người dùng MySQL của bạn
        password='15082003Aa'
    )
    return connection

# Trang chủ, hiển thị danh sách tour
@app.route('/')
def index():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Tour")
    tours = cursor.fetchall()
    connection.close()
    return render_template('index.html', tours=tours)

# Thêm tour
@app.route('/them-tour', methods=['POST'])
def them_tour():
    ten_tour = request.form['ten_tour']
    noi_xuat_phat = request.form['noi_xuat_phat']
    noi_den = request.form['noi_den']
    ngay_xuat_phat = request.form['ngay_xuat_phat']
    gia_tour = request.form['gia_tour']
    so_luong_ve = request.form['so_luong_ve']

    connection = create_connection()
    cursor = connection.cursor()
    sql_query = """
        INSERT INTO Tour (ten_tour, noi_xuat_phat, noi_den, ngay_xuat_phat, gia_tour, so_luong_ve)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_query, (ten_tour, noi_xuat_phat, noi_den, ngay_xuat_phat, gia_tour, so_luong_ve))
    connection.commit()
    connection.close()

    return redirect('/')

# Sửa tour (hiển thị giao diện sửa)
@app.route('/sua-tour/<int:ma_tour>', methods=['GET', 'POST'])
def sua_tour(ma_tour):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        ten_tour = request.form['ten_tour']
        noi_xuat_phat = request.form['noi_xuat_phat']
        noi_den = request.form['noi_den']
        ngay_xuat_phat = request.form['ngay_xuat_phat']
        gia_tour = request.form['gia_tour']
        so_luong_ve = request.form['so_luong_ve']

        sql_query = """
            UPDATE Tour
            SET ten_tour=%s, noi_xuat_phat=%s, noi_den=%s, ngay_xuat_phat=%s, gia_tour=%s, so_luong_ve=%s
            WHERE ma_tour=%s
        """
        cursor.execute(sql_query, (ten_tour, noi_xuat_phat, noi_den, ngay_xuat_phat, gia_tour, so_luong_ve, ma_tour))
        connection.commit()
        connection.close()

        return redirect('/')

    cursor.execute("SELECT * FROM Tour WHERE ma_tour = %s", (ma_tour,))
    tour = cursor.fetchone()
    connection.close()

    return render_template('edit.html', tour=tour)

# Xóa tour
@app.route('/xoa-tour/<int:ma_tour>')
def xoa_tour(ma_tour):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Tour WHERE ma_tour = %s", (ma_tour,))
    connection.commit()
    connection.close()

    return redirect('/')

@app.route('/danh-sach', methods=['GET'])
def danh_sach_tour():
    ten_tour = request.args.get('ten_tour', '')

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    # Nếu có yêu cầu tìm kiếm, sử dụng LIKE để tìm theo tên
    if ten_tour:
        query = "SELECT * FROM Tour WHERE ten_tour LIKE %s"
        cursor.execute(query, ('%' + ten_tour + '%',))
    else:
        query = "SELECT * FROM Tour"
        cursor.execute(query)

    tours = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('list.html', tours=tours)
if __name__ == '__main__':
    app.run(debug=True)
