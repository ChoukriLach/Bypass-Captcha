import requests
from time import sleep


def solve(captcha_api_key, site_key, url):
    session = requests.Session()

    res = session.post(f"http://2captcha.com/in.php"
                       f"?key={captcha_api_key}"
                       f"&method=userrecaptcha"
                       f"&googlekey={site_key}"
                       f"&pageurl={url}")

    print(f'2Captcha result: {res.text}')
    if res.text == 'ERROR_ZERO_BALANCE':
        return 'ERROR_ZERO_BALANCE'
    
    try:
        captcha_id = res.text.split('|')[1]
    except:
        return "ERROR"

    recaptcha_answer = session.get(
        "http://2captcha.com/res.php?key={}&action=get&id={}".format(captcha_api_key, captcha_id)).text

    print(f"Solving ref captcha...")
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        print(f"Recaptcha answer: {recaptcha_answer}, need to wait till solving Captcha. Retrying to solve captcha...")
        recaptcha_answer = session.get(
            "http://2captcha.com/res.php?key={}&action=get&id={}".format(captcha_api_key, captcha_id)).text
        if recaptcha_answer == 'ERROR_CAPTCHA_UNSOLVABLE':
            return 'ERROR_CAPTCHA_UNSOLVABLE'\

        sleep(1)

    recaptcha_answer = recaptcha_answer.split('|')[1]
    return recaptcha_answer

def solve_recaptcha(driver, action):
    print(f'Try to solve with 2Captcha.com')

    recaptcha = driver.find_element_by_css_selector('.g-recaptcha-etsy')
    googlekey = recaptcha.get_attribute('data-sitekey')
    pageurl = driver.current_url

    while True:
        res = solve('f00f46948afa78060ad1eaf83e50224a', googlekey, pageurl)

        if res == 'ERROR_CAPTCHA_UNSOLVABLE' or res == 'ERROR':
            print("Captcha unsolved")
            driver.get(driver.current_url)
            sleep(1/1000)
        else:
            print(f"Captcha solved")
            g_recaptcha_response = driver.find_element_by_css_selector('.g-recaptcha-response')
            driver.execute_script("arguments[0].style.display = 'block';", g_recaptcha_response)
            sleep(1)

            driver.execute_script(f'arguments[0].innerHTML="{res}";', g_recaptcha_response)
            sleep(1)

            action.move_to_element_with_offset(driver.find_element_by_css_selector('.overlay-trigger'), 1, 1)
            action.click()
            action.perform()
            sleep(1)

            driver.find_element_by_css_selector('#app-agree-tou').click()
            sleep(1)

            driver.find_element_by_css_selector('#app-submit').click()
            sleep(1)

            return
