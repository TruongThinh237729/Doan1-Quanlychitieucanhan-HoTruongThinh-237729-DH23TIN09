# DoAn_ChiTieu
# 💰 Trợ Lý Tài Chính Cá Nhân Tích Hợp AI (AI-Powered Personal Finance Tracker)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Pandas](https://img.shields.io/badge/Data-Pandas-green)

Đồ án ứng dụng Desktop quản lý chi tiêu cá nhân thông minh, được viết bằng ngôn ngữ Python. Ứng dụng không chỉ giúp người dùng ghi chép thu chi hằng ngày mà còn đóng vai trò như một **Trợ lý tài chính (AI Advisor)**, tự động phân tích dữ liệu, cảnh báo rủi ro và đưa ra lời khuyên cá nhân hóa dựa trên độ tuổi, nghề nghiệp và mục tiêu tiết kiệm.

---

## ✨ Tính năng nổi bật

* **🔐 Bảo mật & Cá nhân hóa:** Hệ thống đăng nhập an toàn. Quản lý hồ sơ cá nhân chi tiết (Tuổi, Nghề nghiệp, Ngân sách tháng, Mục tiêu tiết kiệm).
* **📊 Bảng điều khiển trực quan (Dashboard):** Thống kê tổng quan dòng tiền theo thời gian thực. Tự động vẽ biểu đồ tròn (Pie Chart) phân bổ chi tiêu bằng `matplotlib`.
* **🧠 Trợ lý Tư vấn AI & Cảnh báo thông minh:**
    * Tự động cảnh báo (Popup) khi nhập khoản tiền lớn (> 5.000.000đ) hoặc khi giao dịch mới làm vượt ngân sách tháng.
    * Thuật toán phân tích tỷ lệ chi tiêu kết hợp với hồ sơ người dùng để tự động sinh ra các báo cáo đánh giá, định hướng tài chính và trích dẫn châm ngôn truyền cảm hứng.
* **🔍 Quản lý & Tìm kiếm linh hoạt:** Lọc giao dịch theo từng tháng, tìm kiếm nhanh theo từ khóa ghi chú, hỗ trợ xóa/sửa giao dịch.
* **📥 Xuất báo cáo Excel:** Tích hợp `pandas` cho phép kết xuất toàn bộ lịch sử giao dịch trong tháng ra tệp `.xlsx` chỉ với 1 cú click chuột.
* **🎨 Giao diện Modern UI (Dark Mode):** Thiết kế tối giản, hiện đại với thanh điều hướng Sidebar, màu sắc trực quan mang lại trải nghiệm người dùng (UX) mượt mà.

---

## 💻 Công nghệ sử dụng

* **Ngôn ngữ chính:** Python 3
* **Giao diện (GUI):** `customtkinter` (Modern UI)
* **Cơ sở dữ liệu:** `sqlite3` (Lưu trữ cục bộ an toàn, truy xuất nhanh)
* **Xử lý dữ liệu & Báo cáo:** `pandas`, `openpyxl` (Xuất Excel)
* **Trực quan hóa:** `matplotlib` (Vẽ biểu đồ)
* **Âm thanh:** `winsound` (Phản hồi âm thanh hệ thống Windows)

---

## 📸 Ảnh chụp màn hình (Screenshots)

> **Lưu ý cho tác giả:** Hãy upload ảnh giao diện phần mềm của bạn vào thư mục repo và thay thế các đường link bên dưới.

| Màn hình Đăng nhập | Bảng điều khiển (Dashboard) |
| :---: | :---: |
| ![Login](link_anh_login_cua_ban.png) | ![Dashboard](link_anh_dashboard_cua_ban.png) |

| Trợ lý Tư vấn AI | Kết xuất Excel |
| :---: | :---: |
| ![AI Advisor](link_anh_ai_cua_ban.png) | ![Excel Export](link_anh_excel_cua_ban.png) |

---

## ⚙️ Hướng dẫn cài đặt và sử dụng

### 1. Yêu cầu hệ thống
Đảm bảo máy tính của bạn đã cài đặt Python 3.8 trở lên.

### 2. Cài đặt các thư viện cần thiết
Mở Terminal / Command Prompt và chạy lệnh sau để cài đặt các thư viện phụ thuộc:
```bash
pip install customtkinter pandas matplotlib openpyxl
