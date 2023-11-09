from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

            version : 3.1
youtube.com/channel/UCnknCgg_3pVXS27ThLpw3xQ
        """)

cpass = configparser.RawConfigParser()
cpass.read('config.data')

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
    client.send_code_request(+6281529415468)

    # Memasukkan kode yang dikirim ke nomor telepon
    code = input('Masukkan kode yang dikirim ke nomor telepon: ')
    client.sign_in(phone_number, code)

    # Memasukkan kata sandi untuk verifikasi dua langkah
    password = input('Masukkan kata sandi untuk verifikasi dua langkah: ')
    client.sign_in(password="password")

# Melakukan operasi Telegram selanjutnya setelah terautentikasi
# ...

# Memutuskan koneksi
client.disconnect()
 
os.system('clear')
banner()
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print(gr+'[+] Choose a group to scrape members :'+re)
i=0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+ g.title)
    i+=1
 
print('')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group=groups[int(g_index)]
 
print(gr+'[+] Fetching Members...')
time.sleep(1)
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)
 
print(gr+'[+] Saving In file...')
time.sleep(1)
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print(gr+'[+] Members scraped successfully.')
