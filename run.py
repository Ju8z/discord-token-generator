import os
import pickle
import random
import time

from src import create

user_dat = "user.dat"

if ("%s" % user_dat) not in os.listdir():
    with open("%s" % user_dat, "wb+") as dat:
        pickle.dump([0, 0], dat)
    name_count = 0
    image_count = 0
else:
    with open("%s" % user_dat, "rb+") as dat:
        data = pickle.load(dat)
        name_count = data[0]
        image_count = data[1]

print(name_count, image_count)
with open('proxy.txt') as f:
    proxies = f.readlines()

#  ----------------------------------------------------------- Config -----------------------------------------------------------

# Captcha API-------------------
anticaptcha = 'e406ba428792cc378b71b2ca6fc65192'
capmonster = '550f0f9c61d50154036b42ba57eb2b97'
captcha_type = 'capmonster'  # Set which captcha api to use

# Email API-------------------
kopeechka = '0afcf16125ff8cee395f24f341158dee'
gmailnator = '28d36f41b7msh30398bd1d7ed3b8p1b924fjsnddc67ade2aa7'
tempgmail = '28d36f41b7msh30398bd1d7ed3b8p1b924fjsnddc67ade2aa7'
email_type = 'tempgmail'  # Set which email api to use

# Sms API-------------------
smsactivate = '964529e413Ad07d3f7510ce0A334d5f6'
smsserviceonline = '393c2f31f49a68d5630cb28277da67c0'
sms_type = 'smsserviceonline'  # Set which sms api to use

phoneVerification = False  # enable or disable phone verification after email was confirmed
random_names = True  # if true generate random names, if false takes names from the name.txt file
upload_avatar = True  # if true uploads avatar from the avatar folder, else does nothing
createAmount = 10  # how many tokens will be created

# --------------------------------------------------------- End of Config ---------------------------------------------------------


captchas = {'anticaptcha': anticaptcha, 'capmonster': capmonster}
phone_apis = {'smsactivate': smsactivate, 'smsserviceonline': smsserviceonline}
email_apis = {'kopeechka': kopeechka, 'gmailnator': gmailnator, 'tempgmail': tempgmail}

names = images = []

if upload_avatar:
    images = os.listdir("src/avatar")

with open("names.txt", 'r+') as name_file:
    name = name_file.readlines()


def createAccount():
    global proxies, image_count, name_count

    proxy = proxies[random.randint(0, len(proxies) - 1)] if len(proxies) != 0 else None
    time.sleep(2)
    global name_count, image_count
    try:

        user = names[name_count] if not random_names and len(names) != 0 and name_count <= len(names) else None
        img_path = "avatar/" + images[image_count] if (upload_avatar and len(images) != 0 and image_count <= len(images)) else None

        print(img_path)

        create(capthaAPI=captchas[captcha_type],
               username=user,
               emailAPI=email_apis[email_type],
               phoneAPI=phone_apis[sms_type],
               proxy=proxy,
               captcha_type=captcha_type,
               email_type=email_type,
               sms_type=sms_type,
               phverify=phoneVerification,
               avatar_imagpath=img_path
               )
    except Exception as e:
        print(e)
        if proxy is not None:
            proxies.remove(proxy)
        if len(proxies) == 0:
            with open('proxy.txt') as f:
                proxies = f.readlines()

        print("Error occurred... Retrying in 10s")
        time.sleep(10)

        return createAccount()

    else:
        if user is not None and not random_names:
            name_count += 1
        if img_path is not None and upload_avatar:
            image_count += 1

        with open("%s" % user_dat, "rb+") as dat:
            dat.seek(0)
            pickle.dump([name_count, image_count], dat)


for i in range(createAmount):
    createAccount()
