import qrcode
from io import BytesIO
from PIL import Image

def generate_custom_qr(data: str, fill_color: str = "black", back_color: str = "white", logo_bytes: bytes = None) -> BytesIO:
    """Rangli va logotipli QR kod yaratish"""
    # Logo qo'shilganda xato tuzatish darajasini (H - 30%) maksimal qilamiz
    qr = qrcode.QRCode(
        version=5, 
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    # Agar foydalanuvchi logo yuklagan bo'lsa
    if logo_bytes:
        logo = Image.open(BytesIO(logo_bytes)).convert("RGBA")
        
        # Logoni QR kodning 25% o'lchamiga moslash
        basewidth = img.size[0] // 4
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
        
        # Logoni markazga joylashtirish
        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, logo)

    stream = BytesIO()
    img.save(stream, format="PNG")
    stream.seek(0)
    return stream               