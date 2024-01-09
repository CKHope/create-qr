# Import các thư viện cần thiết
import streamlit as st
import qrcode
from PIL import Image
import zipfile

# Set password
password = "daiphaphao"

# Nhập mật khẩu từ người dùng
entered_password = st.text_input("Nhập mật khẩu:", type="password")

# Kiểm tra mật khẩu
if entered_password == password:
    # Tiêu đề của ứng dụng
    st.title("QR Code Generator")

    # Text area để người dùng nhập đường link
    links = st.text_area("Nhập các đường link(mỗi dòng là một link):")

    # Chia các đường link thành list
    link_list = links.split("\n")

    # Duyệt qua từng đường link và tạo QR Code
    for link in link_list:
        if link:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)

            # Tạo hình ảnh QR Code
            img = qr.make_image(fill_color="black", back_color="white")

            # Chuyển đổi ảnh thành định dạng RGB
            img = img.convert("RGB")

            # Hiển thị QR Code
            st.image(img, caption=f"Link: {link}", use_column_width=True)

    # Tạo nút để tải xuống QR Code
    if st.button("Tải xuống tất cả QR Codes"):
        zip_filename = "qrcodes.zip"

        with st.spinner("Đang tạo file ZIP..."):
            # Lưu từng QR Code vào file PNG và thêm vào ZIP
            with zipfile.ZipFile(zip_filename, "w") as zipf:
                for i, link in enumerate(link_list):
                    if link:
                        qr.add_data(link)
                        img = qr.make_image(fill_color="black", back_color="white")
                        img = img.convert("RGB")
                        img.save(f"qrcode_{i+1}.png")
                        zipf.write(f"qrcode_{i+1}.png")

        # Hiển thị link để tải xuống file ZIP
        st.success(f"[Tải xuống ZIP]({zip_filename})")

    # Hỏi bạn còn điều gì cần hỗ trợ không?
else:
    st.error("Mật khẩu không chính xác. Vui lòng thử lại.")
