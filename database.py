import sqlite3
from datetime import datetime
import pandas as pd

def connect_db():
    return sqlite3.connect('data_chi_tieu.db')

def khoi_tao_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS giao_dich 
                          (ngay TEXT, loai TEXT, tien REAL, ghi_chu TEXT, phuong_thuc TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user 
                          (ten TEXT, ngan_sach REAL, tuoi INTEGER, nghe_nghiep TEXT, muc_tieu REAL, mat_khau TEXT)''')
        
        cursor.execute("SELECT COUNT(*) FROM user")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", 
                           ('237729', 10000000, 20, 'Sinh viên', 5000000, '1234'))
        conn.commit()

def lay_user_full():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user LIMIT 1")
        return cursor.fetchone()

def cap_nhat_user_nang_cao(ten, ns, tuoi, cv, mt, mk):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE user SET ten=?, ngan_sach=?, tuoi=?, nghe_nghiep=?, muc_tieu=?, mat_khau=?", 
                       (ten, ns, tuoi, cv, mt, mk))
        conn.commit()

def lay_danh_sach_thang_full():
    return [f"{str(i).zfill(2)}/2026" for i in range(1, 13)]

def lay_thong_ke_thang(thang_nam):
    with connect_db() as conn:
        cursor = conn.cursor()
        m, y = thang_nam.split('/')
        cursor.execute("SELECT SUM(tien) FROM giao_dich WHERE strftime('%m', ngay) = ? AND strftime('%Y', ngay) = ?", (m, y))
        res = cursor.fetchone()
        return res[0] or 0

def lay_thong_ke_tong():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(tien), MAX(tien) FROM giao_dich")
        res = cursor.fetchone()
        return (res[0] or 0, res[1] or 0)

def luu_du_lieu(loai, tien, note, pt):
    ngay = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO giao_dich VALUES (?,?,?,?,?)", (ngay, loai, tien, note, pt))
        conn.commit()

# --- TÍNH NĂNG MỚI BỔ SUNG ---

def xoa_giao_dich(ngay_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM giao_dich WHERE ngay=?", (ngay_id,))
        conn.commit()

def tim_kiem_giao_dich(thang_nam, tu_khoa=""):
    with connect_db() as conn:
        cursor = conn.cursor()
        m, y = thang_nam.split('/')
        query = "SELECT * FROM giao_dich WHERE strftime('%m', ngay) = ? AND strftime('%Y', ngay) = ?"
        params = [m, y]
        if tu_khoa:
            query += " AND (ghi_chu LIKE ? OR loai LIKE ?)"
            params.extend([f'%{tu_khoa}%', f'%{tu_khoa}%'])
        query += " ORDER BY ngay DESC"
        cursor.execute(query, params)
        return cursor.fetchall()

def xuat_bao_cao_excel(thang_nam):
    data = tim_kiem_giao_dich(thang_nam)
    if not data: return None
    df = pd.DataFrame(data, columns=['Ngày Giờ', 'Hạng Mục', 'Số Tiền', 'Ghi Chú', 'Phương Thức'])
    filename = f"Bao_Cao_{thang_nam.replace('/', '_')}.xlsx"
    df.to_excel(filename, index=False)
    return filename