from telethon.sync import TelegramClient

api_id = '24352980'
api_hash = 'de976ef6eeba9cbb57372e91024a20c7'

phone_number = '+6281529415468'
client_name = 'your_client_name'

# Membuat objek client
client = TelegramClient(client_name, api_id, api_hash)

# Menghubungkan ke server Telegram
client.connect()

# Memeriksa apakah perlu kata sandi untuk verifikasi dua langkah
if not client.is_user_authorized():
    # Meminta nomor telepon
    client.send_code_request(phone_number)

    # Memasukkan kode yang dikirim ke nomor telepon
    code = input('Masukkan kode yang dikirim ke nomor telepon: ')
    client.sign_in(phone_number, code)

    # Memasukkan kata sandi untuk verifikasi dua langkah
    password = input('Masukkan kata sandi untuk verifikasi dua langkah: ')
    client.sign_in(password=password)

# Melakukan operasi Telegram selanjutnya setelah terautentikasi
# ...

# Memutuskan koneksi
client.disconnect()
