# Import các thư viện cần thiết
import streamlit as st
import qrcode
from PIL import Image
import zipfile
import re  # Thêm thư viện regex
import os

# Set password
password = "daiphaphao"

# Nhập mật khẩu từ người dùng
entered_password = st.text_input("Nhập mật khẩu:", type="password")

# Kiểm tra mật khẩu
if entered_password == password:
    # Tiêu đề của ứng dụng
    st.title("QR Code Generator")

    # Text area để người dùng nhập đường link
    links = st.text_area("Nhập các đường link (mỗi dòng là một link):")

    # Chia các đường link thành list và loại bỏ các dòng trống hoặc không phải là đường link
    link_list = [line.strip() for line in links.split("\n") if line.strip() and re.match(r'^https?://', line)]

    # Kiểm tra xem có đường link hợp lệ không
    if not link_list:
        st.warning("Không có đường link hợp lệ. Vui lòng nhập lại.")
    else:
        # Duyệt qua từng đường link và tạo QR Code
        for i, link in enumerate(link_list):
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

            # Lấy tên file từ các ký tự hợp lệ trong đường link
            valid_chars = f"-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            filename = "".join(c if c in valid_chars else "_" for c in link)

            # Lưu ảnh với tên file hợp lệ
            img_path = f"qrcode_{i+1}_{filename}.png"
            img.save(img_path)

            # Hiển thị QR Code
            st.image(img, caption=f"Link: {link}", use_column_width=True)

        # Tạo nút để tải xuống QR Code
        if st.button("Tải xuống tất cả QR Codes"):
            zip_filename = "qrcodes.zip"

            with st.spinner("Đang tạo file ZIP..."):
                # Lưu từng QR Code vào file PNG và thêm vào ZIP
                with zipfile.ZipFile(zip_filename, "w") as zipf:
                    for i, link in enumerate(link_list):
                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4,
                        )
                        qr.add_data(link)
                        qr.make(fit=True)

                        img = qr.make_image(fill_color="black", back_color="white")
                        img = img.convert("RGB")

                        # Lấy tên file từ các ký tự hợp lệ trong đường link
                        filename = "".join(c if c in valid_chars else "_" for c in link)
                        img_path = f"qrcode_{i+1}_{filename}.png"

                        img.save(img_path)
                        zipf.write(img_path)

                        # Xóa ảnh sau khi thêm vào ZIP để tránh tạo nhiều ảnh lưu trên server
                        os.remove(img_path)

            # Hiển thị link để tải xuống file ZIP
            with open(zip_filename, "rb") as file:
                st.download_button(
                    label="Tải xuống ZIP",
                    data=file.read(),
                    file_name=zip_filename,
                    key="download_button",
                )

    # Hỏi bạn còn điều gì cần hỗ trợ không?
else:
    st.error("Mật khẩu không chính xác. Vui lòng thử lại.")
