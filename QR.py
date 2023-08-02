import qrcode
import datetime
from io import BytesIO

async def generate_qrcode(data):
    # Устанавливаем срок действия QR-кода в 1 минуту
    expiration_date = datetime.datetime.now() + datetime.timedelta(minutes=1)

    # Создаем объект QR-кода
    qr = qrcode.QRCode(
        version=1,  # Размер QR-кода
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Коррекция ошибок
        box_size=10,  # Размер одного пикселя QR-кода
        border=4  # Толщина границы QR-кода
    )

    # Добавляем данные в QR-код (в данном случае, строку с текущей датой и временем)
    qr.add_data(str(data) + ',' + expiration_date.strftime('%Y-%m-%d %H:%M:%S'))
    qr.make(fit=True)

    # Создаем изображение QR-кода
    img = qr.make_image(fill_color="black", back_color="white")

    # Сохраняем QR-код как изображение
    bio = BytesIO()
    img.save(bio, format='PNG')
    bio.seek(0)
    return bio