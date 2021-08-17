import qrcode

from PIL import Image


def generate_qr(container_id: int) -> Image:
    url = f"https://placeholder.com/containers/{container_id}"
    qr = qrcode.QRCode(
        box_size=10,
        border=9
    )
    qr.add_data(url)
    qr.make()
    sticker = qr.make_image()
    return sticker
