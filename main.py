# -*- coding: utf-8 -*-
# https://github.com/mybdye 🌟

import os
import ssl
import time
import urllib

import requests
from helium import *
#from selenium import webdriver
import undetected_chromedriver as webdriver

from selenium.webdriver.common.by import By

# 关闭证书验证
ssl._create_default_https_context = ssl._create_unverified_context

try:
    USER_ID = os.environ['USER_ID']
except:
    # 本地调试用
    USER_ID = ''

try:
    PASS_WD = os.environ['PASS_WD']
except:
    # 本地调试用
    PASS_WD = ''

try:
    BARK_KEY = os.environ['BARK_KEY']
except:
    # 本地调试用
    BARK_KEY = ''

try:
    TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
except:
    # 本地调试用
    TG_BOT_TOKEN = ''

try:
    TG_USER_ID = os.environ['TG_USER_ID']
except:
    # 本地调试用
    TG_USER_ID = ''

audioFile = '\\audio.mp3'
imgFile = '\\capture.png'
urlLogin = 'https://hax.co.id/login'
urlRenew = 'https://hax.co.id/vps-renew/'
urlInfo = 'https://hax.co.id/vps-info'


def switchToWindowSpeechToText():
    print('- switch to window Speech to Text')
    if Window('Speech to Text').exists():
        switch_to('Speech to Text')
    else:
        # Selenium open a new window
        driver = get_driver()
        driver.execute_script('''window.open('https://speech-to-text-demo.ng.bluemix.net/',"_blank")''')
        switch_to('Speech to Text')


def speechToText():
    # switchToWindowSpeechToText()
    driver = get_driver()
    driver.execute_script('''window.open('https://speech-to-text-demo.ng.bluemix.net/',"_blank")''')
    switch_to('Speech to Text')
    # # 向下滚动
    scroll_down(num_pixels=400)
    text = ''
    i = 0
    while text == '':
        i = i + 1
        if i > 3:
            print('*** speechToText issue! ***')
            break
        attach_file(os.getcwd() + audioFile, 'Upload Audio File')
        print('- waiting for transcribe')
        time.sleep(6)
        textlist = find_all(S('.tab-panels--tab-content'))
        text = [key.web_element.text for key in textlist][0]
        print('- get text:', text)
    driver.close()
    return text

def getaudiolink():
    global block
    print('- audio file link searching...')
    if Text('Alternatively, download audio as MP3').exists() or Text('或者以 MP3 格式下载音频').exists():
        block = False
        try:
            src = Link('Alternatively, download audio as MP3').href
        except:
            src = Link('或者以 MP3 格式下载音频').href
        print('- get src:', src)
        
        # 下载音频文件
        urllib.request.urlretrieve(src, os.getcwd() + audioFile)
        time.sleep(4)
        text = speechToText()
        print('- waiting for switch to hax window')

        # 切回第一个 tab
        driver = get_driver()
        driver.switch_to.window(driver.window_handles[0])
        # time.sleep(3)
        wait_until(S('#audio-response').exists)
        print('- fill audio response')
        write(text, into=S('#audio-response'))
        # time.sleep(3)
        wait_until(S('#recaptcha-verify-button').exists)
        print('- click recaptcha verify button')
        click(S('#recaptcha-verify-button'))
        time.sleep(3)
        if Text('Multiple correct solutions required - please solve more.').exists() or Text(
                '需要提供多个正确答案 - 请回答更多问题。').exists():
            print('*** Multiple correct solutions required - please solve more. ***')
            getaudiolink()
        time.sleep(1)

    elif Text('Try again later').exists() or Text('稍后重试').exists():
        textblock = S('.rc-doscaptcha-body-text').web_element.text
        print(textblock)
        body = ' *** 💣 Possibly blocked by google! ***\n' + textblock
        push(body)
        block = True
    else:
        print('*** audio download element not found,return to func renew ***')
        screenshot() # debug
        refresh()
        login()
        #renewVPS()

def reCAPTCHA():
    global block
    print('- click checkbox')
    click(S('.recaptcha-checkbox-borderAnimation'))
    time.sleep(3)
    while S('#recaptcha-audio-button').exists():
        print('- audio button found')
        click(S('#recaptcha-audio-button'))
        time.sleep(3)
        getaudiolink()
    return block


def login():
    print('- login')
    time.sleep(5)
    # if S('@username').exists() is False:
    #     go_to(urlLogin)
    #     login()
    if Window().title == 'Just a moment...':
        # debug for submit issue
        print('*** cloudflare detection ***')
        time.sleep(7)
        print('- title after:', Window().title)
        
    wait_until(Text('Login to Hax.co.id').exists)
    # else:
    print('- fill user id')
    if USER_ID == '':
        print('*** USER_ID is empty ***')
        kill_browser()
    else:
        write(USER_ID, into=S('@username'))
    print('- fill password')
    if PASS_WD == '':
        print('*** PASS_WD is empty ***')
        kill_browser()
    else:
        write(PASS_WD, into=S('@password'))

    if Text('reCAPTCHA').exists():
        # if S('#recaptcha-token').exists():
        print('- reCAPTCHA found!')
        block = reCAPTCHA()
        if block:
            print('*** Possibly blocked by google! ***')
            kill_broowser()
        else:
            submit()
    else:
        print('- reCAPTCHA not found!')
        submit()


def submit():
    print('- submit')
    # 向下滚动，有时候提示找不到按钮（被其他控件cover）
    scroll_down(num_pixels=500)
    click('Submit')
    print('- submit clicked')
    time.sleep(2)

    if Window().title == 'Just a moment...':
        # debug for submit issue
        print('*** cloudflare detection ***')
        time.sleep(7)
        print('- title after:', Window().title)

    try:
        wait_until(Text('Please correct your captcha!.').exists)
        print('*** Network issue maybe, reCAPTCHA load fail! ***')
        go_to(urlLogin)
        time.sleep(2)
        login()
    except:
        pass
    try:
        wait_until(Text('Invalid').exists)
        print('*** Invalid Username / Password ! ***')
    except:
        pass
    try:
        wait_until(Text('VPS Information').exists)
        print('- VPS Information found!')
        renewVPS()
    except:
        print('- title:', Window().title)
        screenshot() # debug
        body = ' *** 💣 some error in func submit!, stop running ***'
        # login()
        #push(body)
        print(body)
        kill_browser()

def screenshot(): # debug
    driver = get_driver()
    driver.get_screenshot_as_file(os.getcwd() + imgFile)
    print('- screenshot done')
    driver.execute_script('''window.open('http://mjjzp.cf/',"_blank")''')
    switch_to('白嫖图床')
    driver.find_element(By.ID, 'image').send_keys(os.getcwd()+imgFile)
    time.sleep(4)
    click('上传')
    wait_until(Text('完成').exists)
    print('- upload done')
    # textList = find_all(S('#code-url'))
    # result = [key.web_element.text for key in textList][0]
    result = S('#code-url').web_element.text
    print('*** capture src:', result)


def renewVPS():
    global block
    print('- renew VPS')
    go_to(urlRenew)
    time.sleep(1)
    # 向下滚动
    scroll_down(num_pixels=900)
    time.sleep(1)
    if S('#web_address').exists():
        print('- fill web address')
        write('hax.co.id', into=S('#web_address'))
        # 过 CAPTCHA
        captcha = funcCAPTCHA()
        print('- fill captcha result')
        write(captcha, into=S('@captcha'))
        print('- check agreement')
        click(S('@agreement'))
        if Text('reCAPTCHA').exists():
            print('- reCAPTCHA found!')
            block = reCAPTCHA()
            if block:
                textList = find_all(S('.rc-doscaptcha-body-text'))
                result = [key.web_element.text for key in textList][0]
                print('*** Possibly blocked by google! ***')
                print(result)
                body = '*** Possibly blocked by google! ***'
                # renewVPS()
                push(body)
                kill_browser()
            else:
                # 向下滚动
                scroll_down(num_pixels=200)
                click('Renew VPS')
        else:
            print('- reCAPTCHA not found!')
            click('Renew VPS')
        body = extendResult()
        if 'renewed' in body:
            body = '🎉 ' + body
        print('- extend result:', body)
        push(body)
        time.sleep(2)
        #kill_browser()
    else:
        #renewVPS()
        #kill_browser()
        print('- else')


def extendResult():
    print('- waiting for extend result response')
    time.sleep(10)
    if S('#response').exists():
        textList = find_all(S('#response'))
        result = [key.web_element.text for key in textList][0]
    else:
        renewVPS()
    return result


def push(body):
    print('- waiting for push result')
    # bark push
    if BARK_KEY == '':
        print('*** No BARK_KEY ***')
    else:
        barkurl = 'https://api.day.app/' + BARK_KEY
        title = 'HaxExtend'
        rq_bark = requests.get(url=f'{barkurl}/{title}/{body}?isArchive=1')
        if rq_bark.status_code == 200:
            print('- bark push Done!')
        else:
            print('*** bark push fail! ***', rq_bark.content.decode('utf-8'))

    # tg push
    if TG_BOT_TOKEN == '' or TG_USER_ID == '':
        print('*** No TG_BOT_TOKEN or TG_USER_ID ***')
    else:
        body = 'HaxExtend\n\n' + body
        server = 'https://api.telegram.org'
        tgurl = server + '/bot' + TG_BOT_TOKEN + '/sendMessage'
        rq_tg = requests.post(tgurl, data={'chat_id': TG_USER_ID, 'text': body}, headers={
            'Content-Type': 'application/x-www-form-urlencoded'})
        if rq_tg.status_code == 200:
            print('- tg push Done!')
        else:
            print('*** tg push fail! ***', rq_tg.content.decode('utf-8'))

    print('- finish!')


def funcCAPTCHA():
    print('- do CAPTCHA')
    divList = find_all(S('.col-sm-3'))
    # 取计算方法
    method = [key.web_element.text for key in divList][0][0]
    # Helium 下没有好的方法拿到两个小图片的 src，切换到 selenium
    driver = get_driver()
    number1 = int(
        driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][
            0])
    number2 = int(
        driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][
            0])

    if method == '+':
        captcha_result = number1 + number2
    elif method == '-':
        # 应该没有 但还是写了
        captcha_result = number1 - number2
    elif method == 'X':
        captcha_result = number1 * number2
    elif method == '/':
        # 应该没有 但还是写了
        captcha_result = number1 / number2

    print('- captcha result:', number1, method, number2, '=', captcha_result)
    return captcha_result

block = False
print('- Hax loading...')

#start_chrome(url=urlLogin)
# # 向下滚动
# scroll_down(num_pixels=550)
if __name__ == "__main__":
    webdriver.TARGET_VERSION = 99
    driver = webdriver.Chrome()
    #driver.get(url)
    set_driver(driver)
    get_driver()
    go_to(urlLogin)
    print('- title:', Window().title)
    login()
