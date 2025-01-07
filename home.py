import streamlit as st
import qrcode
from PIL import Image
import io
import pandas as pd
import os
from dotenv import load_dotenv

# Função para gerar uma imagem de código QR com um logo embutido como bytes
def generate_qr_with_logo(data, logo_path):
    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Cria a imagem do QR Code
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Abre a imagem do logo
    logo = Image.open(logo_path)

    # Redimensiona o logo para caber no QR Code
    qr_width, qr_height = qr_img.size
    logo_size = qr_width // 4
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Calcula a posição para colar o logo
    logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

    # Cola o logo no QR Code
    qr_img.paste(logo, logo_position, mask=logo)

    # Converte a imagem PIL para bytes
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()  # Retorna os bytes da imagem

load_dotenv()

management_url = os.getenv("MANAGEMENT_URL")
patient_url = os.getenv("PATIENTAPP_URL")

st.title("Códigos QR para Leitos Hospitalares")

st.write(f"[Gerencia]({management_url})")

logo_path = "alligator4.png"  # Substitua pelo caminho do seu logo

for bed_id in [101, 102, 103]:
    qr_data = f"{patient_url}/?bed_id={bed_id}"
    qr_image = generate_qr_with_logo(qr_data, logo_path)
    st.image(qr_image, caption=f"Leito {bed_id}", width=200)
    st.write(f"[Ir para Solicitações do Leito {bed_id}]({qr_data})")


