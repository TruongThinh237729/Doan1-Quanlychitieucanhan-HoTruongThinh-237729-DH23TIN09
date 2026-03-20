import customtkinter as ctk
import database as db
from styles import *
from tkinter import messagebox
import winsound
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import random

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login):
        super().__init__(parent, fg_color=COLOR_BG)
        self.on_login = on_login
        self.box = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=25, width=420, height=580)
        self.box.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.box, text="🔐", font=("Segoe UI", 85)).pack(pady=(30, 10))
        ctk.CTkLabel(self.box, text="XÁC THỰC TÀI KHOẢN", font=("Segoe UI", 28, "bold"), text_color=COLOR_ACCENT).pack(pady=5)
        
        self.user_entry = ctk.CTkEntry(self.box, placeholder_text="Tên đăng nhập...", width=320, height=55, 
                                       font=("Segoe UI", 18, "bold"), text_color=COLOR_NUMBER,
                                       fg_color=COLOR_ENTRY_BG, border_color=COLOR_ACCENT)
        self.user_entry.pack(pady=15)
        
        self.pass_entry = ctk.CTkEntry(self.box, placeholder_text="Mật khẩu...", width=320, height=55, 
                                       font=("Segoe UI", 18, "bold"), text_color=COLOR_NUMBER,
                                       show="*", fg_color=COLOR_ENTRY_BG, border_color=COLOR_ACCENT)
        self.pass_entry.pack(pady=15)
        
        ctk.CTkButton(self.box, text="ĐĂNG NHẬP HỆ THỐNG", fg_color=COLOR_ACCENT, hover_color="#7C3AED",
                       width=320, height=60, font=("Segoe UI", 18, "bold"), command=self.check_login).pack(pady=25)

    def check_login(self):
        u = db.lay_user_full()
        if self.user_entry.get().strip().lower() == u[0].lower() and self.pass_entry.get() == str(u[5]):
            winsound.PlaySound("SystemExit", winsound.SND_ASYNC)
            self.on_login()
        else:
            messagebox.showerror("Thất bại", "Sai thông tin đăng nhập!")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        db.khoi_tao_db()
        self.title("TRỢ LÝ TÀI CHÍNH")
        self.geometry("1400x950")
        self.configure(fg_color=COLOR_BG)
        self.login_screen = LoginScreen(self, self.show_main_app)
        self.login_screen.pack(fill="both", expand=True)

    def show_main_app(self):
        self.login_screen.pack_forget()
        self.sidebar = ctk.CTkFrame(self, width=280, fg_color=COLOR_SIDEBAR, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="💖 QUẢN LÝ CHI TIÊU", font=("Segoe UI", 32, "bold"), text_color=COLOR_ACCENT).pack(pady=50)
        
        nav = [("🏠 TRANG CHỦ", "home"), 
               ("💸 NHẬP CHI TIÊU", "add"), 
               ("📊 THỐNG KÊ", "stats"), 
               ("🎀 HỒ SƠ CỦA BẠN", "profile"),
               ("🤖 TƯ VẤN AI", "ai")]
               
        for t, p in nav:
            ctk.CTkButton(self.sidebar, text=t, fg_color="transparent", anchor="w", height=60, 
                          font=("Segoe UI", 16, "bold"), command=lambda x=p: self.show_page(x)).pack(fill="x", padx=20, pady=5)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="right", fill="both", expand=True, padx=45, pady=40)
        
        self.pages = {
            "home": ctk.CTkScrollableFrame(self.container, fg_color="transparent"),
            "add": ctk.CTkFrame(self.container, fg_color=COLOR_CARD, corner_radius=25),
            "stats": ctk.CTkFrame(self.container, fg_color="transparent"),
            "profile": ctk.CTkScrollableFrame(self.container, fg_color=COLOR_CARD, corner_radius=25),
            "ai": ctk.CTkFrame(self.container, fg_color=COLOR_CARD, corner_radius=25)
        }
        self.init_pages()
        self.show_page("home")

    def init_pages(self):
        self.build_home(self.pages["home"])
        self.build_add(self.pages["add"])
        self.build_stats(self.pages["stats"])
        self.build_profile(self.pages["profile"])
        self.build_ai(self.pages["ai"])

    def show_page(self, page_id):
        for p in self.pages.values(): p.pack_forget()
        self.pages[page_id].pack(fill="both", expand=True)
        if page_id == "home": self.refresh_dashboard()
        if page_id == "stats": self.refresh_stats_page()

    # --- TRANG CHỦ ---
    def build_home(self, parent):
        self.lbl_hi = ctk.CTkLabel(parent, text="Chào bạn yêu,", font=("Segoe UI", 24), text_color="#CBD5E1")
        self.lbl_hi.pack(anchor="w")
        self.lbl_user = ctk.CTkLabel(parent, text="", font=("Segoe UI", 55, "bold"), text_color=COLOR_ACCENT)
        self.lbl_user.pack(anchor="w", pady=(0, 30))

        card_f = ctk.CTkFrame(parent, fg_color="transparent")
        card_f.pack(fill="x")
        self.card_tong = self.create_card(card_f, "🛒 TỔNG CHI TIÊU", COLOR_ACCENT, 0)
        self.card_max = self.create_card(card_f, "💎 GIAO DỊCH LỚN NHẤT", COLOR_NUMBER, 1)
        card_f.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(parent, text="🕒 GIAO DỊCH GẦN ĐÂY", font=("Segoe UI", 20, "bold"), text_color=COLOR_SUCCESS).pack(anchor="w", pady=(20, 10))
        self.home_list = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=20)
        self.home_list.pack(fill="x")

        self.chart_box = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=25, height=400)
        self.chart_box.pack(fill="x", pady=30)

    def create_card(self, master, title, color, col):
        f = ctk.CTkFrame(master, fg_color=COLOR_CARD, corner_radius=30, height=180)
        f.grid(row=0, column=col, padx=15, sticky="nsew")
        ctk.CTkLabel(f, text=title, font=("Segoe UI", 16, "bold"), text_color=color).pack(pady=15)
        lbl = ctk.CTkLabel(f, text="0 ₫", font=("Consolas", 40, "bold"), text_color=COLOR_TEXT)
        lbl.pack(pady=5)
        f.lbl = lbl
        return f

    def refresh_dashboard(self):
        u = db.lay_user_full()
        tong, max_v = db.lay_thong_ke_tong()
        self.lbl_user.configure(text=f"{u[0].upper()}")
        self.card_tong.lbl.configure(text=f"{int(tong):,} ₫".replace(",", "."))
        self.card_max.lbl.configure(text=f"{int(max_v):,} ₫".replace(",", "."))
        
        for w in self.home_list.winfo_children(): w.destroy()
        data = db.tim_kiem_giao_dich(datetime.now().strftime("%m/%Y"))[:5]
        for h in data:
            r = ctk.CTkFrame(self.home_list, fg_color="transparent")
            r.pack(fill="x", pady=2, padx=10)
            ctk.CTkLabel(r, text=f"{h[1]} - {h[3]}", text_color="white").pack(side="left")
            ctk.CTkLabel(r, text=f"{int(h[2]):,} ₫", text_color=COLOR_SUCCESS, font=("Consolas", 14, "bold")).pack(side="right")
        
        self.update_chart()

    def update_chart(self):
        for w in self.chart_box.winfo_children(): w.destroy()
        data = db.tim_kiem_giao_dich(datetime.now().strftime("%m/%Y"))
        if not data: return
        df = pd.DataFrame(data, columns=['Ngay', 'Loai', 'Tien', 'Note', 'PT'])
        ds = df.groupby('Loai')['Tien'].sum()
        fig, ax = plt.subplots(figsize=(5, 3), facecolor=COLOR_CARD)
        ax.pie(ds, labels=ds.index, autopct='%1.1f%%', textprops={'color':"w"}, colors=['#FB7185', '#F472B6', '#2DD4BF', '#FDE047'])
        FigureCanvasTkAgg(fig, master=self.chart_box).get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    # --- TRANG THỐNG KÊ ---
    def build_stats(self, parent):
        ctk.CTkLabel(parent, text="📊 CHI TIÊU CÁ NHÂN 2026", font=("Segoe UI", 32, "bold"), text_color=COLOR_SUCCESS).pack(pady=20)
        
        ctrl = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=15)
        ctrl.pack(fill="x", padx=10, pady=10)
        
        self.month_cb = ctk.CTkComboBox(ctrl, values=db.lay_danh_sach_thang_full(), width=140, command=lambda x: self.refresh_stats_page())
        self.month_cb.set(datetime.now().strftime("%m/%Y"))
        self.month_cb.pack(side="left", padx=10, pady=15)
        
        self.search_in = ctk.CTkEntry(ctrl, placeholder_text="🔍 Tìm ghi chú...", width=200)
        self.search_in.pack(side="left", padx=10)
        self.search_in.bind("<KeyRelease>", lambda e: self.refresh_stats_page())
        
        ctk.CTkButton(ctrl, text="📥 XUẤT EXCEL", fg_color="#10B981", width=120, command=self.export_excel).pack(side="left", padx=10)

        self.lbl_stat_total = ctk.CTkLabel(ctrl, text="0 ₫", font=("Consolas", 22, "bold"), text_color=COLOR_NUMBER)
        self.lbl_stat_total.pack(side="right", padx=30)

        self.stat_scroll = ctk.CTkScrollableFrame(parent, fg_color=COLOR_CARD, corner_radius=20)
        self.stat_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_stats_page(self):
        for w in self.stat_scroll.winfo_children(): w.destroy()
        sel = self.month_cb.get()
        tk = self.search_in.get()
        data = db.tim_kiem_giao_dich(sel, tk)
        total = sum(i[2] for i in data)
        self.lbl_stat_total.configure(text=f"Tổng: {int(total):,} ₫".replace(",", "."))
        
        for h in data:
            r = ctk.CTkFrame(self.stat_scroll, fg_color="#1E293B", height=60)
            r.pack(fill="x", pady=2, padx=5)
            ctk.CTkLabel(r, text=h[0].split(' ')[0], font=("Consolas", 14), text_color=COLOR_NUMBER, width=90).pack(side="left", padx=10)
            ctk.CTkLabel(r, text=h[1], font=("Segoe UI", 14, "bold"), text_color=COLOR_ACCENT, width=90).pack(side="left")
            ctk.CTkLabel(r, text=f"➜ {h[3]}", font=("Segoe UI", 14), text_color="white", anchor="w", width=250).pack(side="left", padx=10)
            ctk.CTkLabel(r, text=f"{int(h[2]):,} ₫".replace(",", "."), font=("Consolas", 16, "bold"), text_color=COLOR_SUCCESS).pack(side="left", padx=15)
            
            ctk.CTkButton(r, text="🗑️", width=40, fg_color="#E11D48", command=lambda x=h[0]: self.confirm_delete(x)).pack(side="right", padx=10)

    def confirm_delete(self, id_ngay):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa khoản chi này?"):
            db.xoa_giao_dich(id_ngay)
            self.refresh_stats_page()
            self.refresh_dashboard()

    def export_excel(self):
        fname = db.xuat_bao_cao_excel(self.month_cb.get())
        if fname: messagebox.showinfo("Thành công", f"Đã xuất file: {fname}")

    # --- TRANG NHẬP ---
    def build_add(self, parent):
        ctk.CTkLabel(parent, text="📝 GHI CHÉP CHI TIÊU", font=("Segoe UI", 32, "bold"), text_color=COLOR_ACCENT).pack(pady=40)
        self.i_loai = ctk.CTkOptionMenu(parent, values=["Ăn uống", "Đi lại", "Mua sắm", "Học tập", "Khác"], width=400, height=50)
        self.i_loai.pack(pady=10)
        self.i_tien = ctk.CTkEntry(parent, placeholder_text="Số tiền (₫)...", width=400, height=50, font=("Consolas", 18))
        self.i_tien.pack(pady=10)
        self.i_note = ctk.CTkEntry(parent, placeholder_text="Bạn đã chi cho việc gì?...", width=400, height=50)
        self.i_note.pack(pady=10)
        self.i_pt = ctk.CTkSegmentedButton(parent, values=["Tiền mặt", "Thẻ", "Momo"], width=400, height=50)
        self.i_pt.set("Tiền mặt"); self.i_pt.pack(pady=20)
        ctk.CTkButton(parent, text="XÁC NHẬN LƯU", fg_color=COLOR_ACCENT, font=("Segoe UI", 18, "bold"), height=60, width=300, command=self.save_tx).pack(pady=20)

    def save_tx(self):
        t_raw = self.i_tien.get()
        note = self.i_note.get()
        
        if not t_raw or not note:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ tiền và ghi chú!")
            return
        if not t_raw.isdigit() or float(t_raw) <= 0:
            messagebox.showwarning("Lỗi", "Số tiền phải là số dương!")
            return

        tien = float(t_raw)

        if tien > 5000000:
            if not messagebox.askyesno("AI Cảnh báo", f"Số tiền {int(tien):,} ₫ là rất lớn. Bạn chắc chứ?"):
                return

        u = db.lay_user_full()
        try:
            da_tieu = db.lay_thong_ke_thang(datetime.now().strftime("%m/%Y"))
            if da_tieu is None: da_tieu = 0
        except:
            da_tieu = 0
            
        if (da_tieu + tien) > u[1]:
            messagebox.showwarning("AI Cảnh báo", "Khoản chi này sẽ khiến bạn VƯỢT ngân sách tháng!")

        db.luu_du_lieu(self.i_loai.get(), tien, note, self.i_pt.get())
        self.i_tien.delete(0, 'end'); self.i_note.delete(0, 'end')
        messagebox.showinfo("Thành công", "Dữ liệu đã được lưu!"); self.show_page("home")

    # --- TRANG HỒ SƠ ---
    def build_profile(self, parent):
        u = db.lay_user_full()
        ctk.CTkLabel(parent, text="🎀 THIẾT LẬP TÀI KHOẢN", font=("Segoe UI", 30, "bold"), text_color="#8B5CF6").pack(pady=30)
        self.e_ten = self.create_in(parent, "Tên người dùng:", u[0])
        self.e_mk = self.create_in(parent, "Mật khẩu mới:", u[5])
        self.e_ns = self.create_in(parent, "Ngân sách tháng:", int(u[1]))
        self.e_tuoi = self.create_in(parent, "Tuổi:", u[2])
        self.e_cv = self.create_in(parent, "Nghề nghiệp:", u[3])
        self.e_mt = self.create_in(parent, "Mục tiêu tiết kiệm:", int(u[4]))
        ctk.CTkButton(parent, text="LƯU THAY ĐỔI HỆ THỐNG", fg_color="#8B5CF6", hover_color="#7C3AED", font=("Segoe UI", 18, "bold"), 
                       height=60, width=400, command=self.update_user).pack(pady=40)

    def create_in(self, master, label, val):
        f = ctk.CTkFrame(master, fg_color="transparent"); f.pack(pady=10)
        ctk.CTkLabel(f, text=label, width=220, anchor="w", font=("Segoe UI", 16, "bold"), text_color="#FDA4AF").pack(side="left")
        e = ctk.CTkEntry(f, width=350, height=45); e.insert(0, str(val)); e.pack(side="left", padx=20)
        return e

    def update_user(self):
        db.cap_nhat_user_nang_cao(self.e_ten.get(), float(self.e_ns.get()), int(self.e_tuoi.get()), 
                                 self.e_cv.get(), float(self.e_mt.get()), self.e_mk.get())
        messagebox.showinfo("Thông báo", "Cập nhật thành công!"); self.show_page("home")

    # --- TRANG TƯ VẤN AI ---
    def build_ai(self, parent):
        ctk.CTkLabel(parent, text="🤖 TRỢ LÝ TÀI CHÍNH AI", font=("Segoe UI", 32, "bold"), text_color="#8B5CF6").pack(pady=(30, 10))
        ctk.CTkLabel(parent, text="Hệ thống thuật toán phân tích thói quen và đưa ra lời khuyên cá nhân hóa", font=("Segoe UI", 16), text_color="#94A3B8").pack(pady=(0, 20))
        
        self.ai_textbox = ctk.CTkTextbox(parent, font=("Segoe UI", 18), wrap="word", corner_radius=15, 
                                         fg_color="#1E293B", text_color="white", border_width=1, border_color="#8B5CF6")
        self.ai_textbox.pack(fill="both", expand=True, padx=40, pady=20)
        self.ai_textbox.insert("0.0", "Xin chào! Nhấn nút bên dưới để AI bắt đầu quét dữ liệu chi tiêu tháng này của bạn...\n")
        self.ai_textbox.configure(state="disabled")

        ctk.CTkButton(parent, text="✨ PHÂN TÍCH VÀ ĐƯA RA LỜI KHUYÊN", fg_color="#8B5CF6", hover_color="#7C3AED", 
                      font=("Segoe UI", 18, "bold"), height=60, width=400, command=self.generate_ai_advice).pack(pady=(0, 30))

    def generate_ai_advice(self):
        self.ai_textbox.configure(state="normal")
        self.ai_textbox.delete("0.0", "end")
        self.ai_textbox.insert("end", "⏳ Đang phân tích dữ liệu hệ thống...\n")
        self.update() 

        u = db.lay_user_full()
        ten, ngan_sach, tuoi, nghe_nghiep, muc_tieu = u[0], float(u[1]), int(u[2]), u[3], float(u[4])
        
        try:
            da_tieu = db.lay_thong_ke_thang(datetime.now().strftime("%m/%Y"))
            if da_tieu is None: da_tieu = 0
        except:
            da_tieu = 0

        phan_tram = (da_tieu / ngan_sach) * 100 if ngan_sach > 0 else 0
        
        loi_khuyen = f"📊 BÁO CÁO PHÂN TÍCH TÀI CHÍNH CHO {ten.upper()}:\n"
        loi_khuyen += "-" * 50 + "\n\n"
        
        loi_khuyen += f"1️⃣ Tình trạng ngân sách tháng này:\n"
        loi_khuyen += f"• Ngân sách cho phép: {int(ngan_sach):,} ₫\n"
        loi_khuyen += f"• Bạn đã tiêu: {int(da_tieu):,} ₫ ({phan_tram:.1f}%)\n"
        
        if phan_tram == 0:
            loi_khuyen += "💡 Đánh giá: Bạn chưa có khoản chi nào trong tháng này. Hãy tiếp tục duy trì thói quen ghi chép nhé!\n\n"
        elif phan_tram < 50:
            loi_khuyen += "💡 Đánh giá: Rất tuyệt vời! Bạn quản lý tiền rất tốt và đang đi đúng hướng.\n\n"
        elif phan_tram < 80:
            loi_khuyen += "⚠️ Đánh giá: Bạn đã tiêu quá nửa ngân sách. Hãy chú ý các khoản chi lặt vặt từ giờ đến cuối tháng.\n\n"
        elif phan_tram <= 100:
            loi_khuyen += "🚨 CẢNH BÁO: Bạn sắp hết ngân sách! Hãy ngừng ngay các khoản mua sắm không thực sự cần thiết.\n\n"
        else:
            loi_khuyen += "⛔ BÁO ĐỘNG ĐỎ: Bạn đã CHI VƯỢT ngân sách! Hãy xem xét lại ngay thói quen chi tiêu của mình.\n\n"

        loi_khuyen += f"2️⃣ Tư vấn cá nhân hóa (Dựa trên nghề nghiệp '{nghe_nghiep}' và độ tuổi {tuoi}):\n"
        
        if tuoi < 25:
            loi_khuyen += "• Ở độ tuổi trẻ, bạn nên tập trung đầu tư vào học tập và phát triển kỹ năng (mua sách, khóa học) thay vì chỉ mua sắm tiêu sản.\n"
        elif 25 <= tuoi <= 35:
            loi_khuyen += "• Đây là giai đoạn vàng để tích lũy tài sản. Hãy xem xét phân bổ 20% thu nhập vào các quỹ đầu tư an toàn.\n"
        else:
            loi_khuyen += "• Ưu tiên xây dựng quỹ dự phòng y tế và hưu trí để đảm bảo an toàn tài chính dài hạn.\n"

        loi_khuyen += f"\n3️⃣ Đánh giá mục tiêu tiết kiệm ({int(muc_tieu):,} ₫):\n"
        if muc_tieu <= 0:
            loi_khuyen += "• Hiện tại bạn chưa thiết lập mục tiêu tiết kiệm. Người thành công luôn 'trả cho mình trước'. Hãy vào phần Hồ sơ để cập nhật mục tiêu nhé!\n"
        else:
            if da_tieu >= ngan_sach:
                loi_khuyen += "• Rất tiếc, với đà chi tiêu hiện tại, bạn sẽ khó đạt được mục tiêu tiết kiệm. Hãy cắt giảm 15% các khoản 'Ăn uống ngoài' và 'Mua sắm'.\n"
            else:
                loi_khuyen += f"• Tuyệt vời! Nếu giữ vững phong độ, bạn hoàn toàn có thể đạt được mục tiêu {int(muc_tieu):,} ₫ một cách dễ dàng.\n"

        loi_khuyen += "\n📌 Châm ngôn tài chính hôm nay:\n"
        quotes = [
            "Đừng tiết kiệm những gì còn lại sau khi chi tiêu, hãy chi tiêu những gì còn lại sau khi tiết kiệm. - Warren Buffett",
            "Sự giàu có không phải là có nhiều tiền, mà là có nhiều lựa chọn.",
            "Kẻ thù lớn nhất của sự tự do tài chính là thói quen chi tiêu bốc đồng.",
            "Biết quản lý 1 triệu đồng thì mới có cơ hội sở hữu 1 tỷ đồng."
        ]
        loi_khuyen += f"\"{random.choice(quotes)}\""

        self.ai_textbox.delete("0.0", "end")
        self.ai_textbox.insert("end", loi_khuyen)
        self.ai_textbox.configure(state="disabled") 
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)

if __name__ == "__main__":
    App().mainloop()
