from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

def gerar_pdf(imagem_np_array, descricao, logo_path="./Configurations/Data/LogoAche.png"):
    nome_pdf = f"./Configurations/Logs/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(nome_pdf, pagesize=A4)
    page_width, page_height = A4

    # Cabeçalho
    margin_top = 50
    spacing = 15
    c.drawString(50, page_height - margin_top,f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    c.drawString(50, page_height - margin_top - spacing, f"Descrição: {descricao}")
    c.drawImage(logo_path, page_width - 130, page_height - margin_top - 10, width=80, height=30, mask='auto')

    # Converte imagem OpenCV (BGR) para PIL (RGB)
    img_rgb = cv2.cvtColor(imagem_np_array, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(img_rgb)

    # Converte para BytesIO para inserir no PDF
    img_buffer = BytesIO()
    pil_image.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    image_reader = ImageReader(img_buffer)

    # Redimensiona e posiciona imagem no PDF
    img_width, img_height = pil_image.size
    max_width = page_width * 0.9
    max_height = page_height * 0.6
    scale = min(max_width / img_width, max_height / img_height)
    scaled_width = img_width * scale
    scaled_height = img_height * scale

    x = (page_width - scaled_width) / 2
    y = page_height - margin_top - spacing * 2 - 30 - scaled_height - 20

    c.drawImage(image_reader, x, y, width=scaled_width, height=scaled_height)
    c.save()

