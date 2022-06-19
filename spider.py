from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from captcha_solver import solve_recaptcha

PATH = ChromeDriverManager().install()
options = ChromeOptions() 
options.add_argument("user-data-dir=C:\\Users\\2000g\\AppData\\Local\\Google\\Chrome\\User Data")
driver = Chrome(executable_path=PATH, chrome_options=options)
action = ActionChains(driver)

driver.get('https://www.etsy.com/developers/register')

name = 'testing-app'
description = 'this is just an app for testing'

driver.find_element_by_css_selector('#app-name').send_keys(name)
driver.find_element_by_css_selector('#app-approval-description').send_keys(description)

for elem in driver.find_elements_by_css_selector('.wt-mb-xs-2+ .wt-radio label'):
    elem.click()

for elem in driver.find_elements_by_css_selector('.wt-mb-xs-2+ .wt-checkbox label'):
    elem.click()

solve_recaptcha(driver, action)
