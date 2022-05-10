import time

from src.Discord import Discord
from src.captcha.CaptchaAntiCaptcha import CaptchaAntiCaptcha
from src.captcha.CaptchaCapmonster import CaptchaCapmonster
from src.emails.EmailGmailnator import EmailGmailnator
from src.emails.EmailKopeechka import EmailKopeechka
from src.emails.EmailTempGmail import EmailTempGmail
from src.sms.SmsSmsActivate import SmsSmsActivate
from src.sms.SmsSmsServiceOnline import SmsSmsServiceOnline
from src.utils.Generator import generateDOB, generatePassword, generateUsername


def create(capthaAPI, emailAPI, phoneAPI, proxy=None, username=None, verbose: bool = True, captcha_type='anticaptcha', email_type="kopeechka",
           sms_type="smsactivate", phverify: bool = True, avatar_imagpath=None):
    start = time.time()
    smsCode = phverify

    if email_type == 'kopeechka':
        accountEmail = EmailKopeechka(emailAPI)
    elif email_type == 'gmailnator':
        accountEmail = EmailGmailnator(emailAPI)
    else:
        accountEmail = EmailTempGmail(emailAPI)

    if verbose:
        print("Got E-Mail ->", accountEmail.email)

    if captcha_type == "anticaptcha":
        loginCaptcha = CaptchaAntiCaptcha('https://discord.com/login', '4c672d35-0701-42b2-88c3-78380b0db560', capthaAPI)
    else:
        loginCaptcha = CaptchaCapmonster('https://discord.com/login', '4c672d35-0701-42b2-88c3-78380b0db560', capthaAPI)

    if verbose:
        print("Requested captcha solve, task id ->", loginCaptcha.taskId)

    session = Discord(proxy, verbose)

    if verbose:
        print("Discord session created")

    if username is None:
        username = generateUsername()
    password = generatePassword()
    dob = generateDOB()

    if verbose:
        print("Waiting for captcha")
    captchaKey = loginCaptcha.waitForResult()

    if verbose:
        print("Sending register request")
    session.register(captchaKey, dob, accountEmail.email, password, username)

    if verbose:
        print("Performing account check")
    session.check()

    if verbose:
        print("Waiting for verification E-Mail")
    email_verification_link = accountEmail.waitForEmail()
    # print("link: ",email_verification_link)

    if captcha_type == "anticaptcha":
        emailCaptcha = CaptchaAntiCaptcha('https://discord.com/verify', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34', capthaAPI)
    else:
        emailCaptcha = CaptchaCapmonster('https://discord.com/verify', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34', capthaAPI)
    if verbose:
        print("Requested captcha solve, task id ->", emailCaptcha.taskId)

    email_verification_token = session.getEmailVerificationToken(email_verification_link)
    if verbose:
        print("Received E-Mail token")

    if verbose:
        print("Waiting for captcha")
    captchaKey = emailCaptcha.waitForResult()

    if verbose:
        print("Sending E-Mail verification request")
    session.verifyEmail(email_verification_token, captchaKey)

    if verbose:
        print("Performing online check")
    if (not session.beOnline()):
        Exception()

    if phverify:
        if verbose:
            print('-')

        if captcha_type == "anticaptcha":
            smsCaptcha = CaptchaAntiCaptcha('https://discord.com/channels/@me', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34', capthaAPI)
        else:
            smsCaptcha = CaptchaCapmonster('https://discord.com/channels/@me', 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34', capthaAPI)
        if verbose:
            print("Requested captcha Solve, task id ->", smsCaptcha.taskId)

        if sms_type == "smsactivate":
            phone = SmsSmsActivate(phoneAPI)
        else:
            phone = SmsSmsServiceOnline(phoneAPI)
        if verbose:
            print("Phone number -> +" + phone.number)

        if verbose:
            print("Waiting for captcha")
        captchaKey = smsCaptcha.waitForResult()

        if verbose:
            print("Requesting SMS from Discord")
        res = session.requestSms(captchaKey, phone.number)

        if res:
            if verbose:
                print("Waiting for SMS code")
            smsCode = phone.waitforcode()
            if smsCode is False:
                if verbose:
                    print("Phone verification failed. Dumping in token_fail.txt")
                    with open("token_fail.txt", 'a+') as phone_fail:
                        phone_fail.write(f'{session.email}:{session.password}:{session.token}:{proxy}\n')
                else:
                    print("SMS recieved")

        if smsCode:
            if verbose:
                print('-')

            if verbose:
                print("Received SMS ->", smsCode, "| Submitting to Discord..")
            session.submitSms(smsCode, phone.number)
            print("Phone verification successfull")

    if avatar_imagpath is not None:
        print("Uploading avatar")
        session.uploadAvatar(avatar_imagpath)

    if verbose:
        print("Performing account check")
    session.check()

    if phverify and smsCode:
        with open("tokens_phone.txt", 'a+') as phone_text:
            phone_text.write(f"{session.email}:{session.password}:{session.token}:{proxy}\n")
        print('Phone verified user written into file')
        # PUt in txt file  tokens_phone.txt
    else:

        with open("tokens_email.txt", 'a+') as email_text:
            email_text.write(f"{session.email}:{session.password}:{session.token}:{proxy}\n")
        print('Email verified user written into file')
        # PUt in txt file  tokens_email.txt

    end = time.time()
    if verbose:
        print("Took", round(end - start), "seconds")

    if verbose:
        print(session.email + ":" + session.password + " - " + session.token)

    return session
