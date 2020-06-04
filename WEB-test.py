import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

masterip = '192.168.0.223'
slaveip = '192.168.0.222'
baserate = 89
pam = 32

driver = webdriver.Chrome('C:\webdriverChrome\chromedriver.exe')
driver.implicitly_wait(5)


def set_params(pam, baserate, channel = '1', ip = masterip, mode = 'Master'):
    driver.get("http://" + ip)
    driver.switch_to.frame('left')
    driver.find_element_by_css_selector("tbody > tr:nth-child(10) > td > a").click()
    driver.switch_to.default_content()
    driver.switch_to.frame('main')
    select = Select(driver.find_element_by_id("dsl1_master_mode"))
    if mode == 'Master':    #Mode chosing
        select.select_by_value("1")
    else: select.select_by_value("0")
    Select(driver.find_element_by_id("dsl1_ext")).select_by_value("1") #Extended ON
    driver.find_element_by_id('dsl1_baserate').clear()
    driver.find_element_by_id('dsl1_baserate').send_keys(str(baserate)) #Set baserate
    select2 = Select(driver.find_element_by_id("dsl1_pam"))
    if pam == 32: select2.select_by_value("1")
    elif pam == 64: select2.select_by_value("4")
    elif pam == 128: select2.select_by_value("5")
    elif pam == 16: select2.select_by_value("0")
    elif pam == 8: select2.select_by_value("2")
    elif pam == 4: select2.select_by_value("3")
    else: print('wrong baserate!')
    savebutton = driver.find_element_by_css_selector('input[value="Save"]')
    savebutton.click()
    time.sleep(1)
    driver.find_element_by_css_selector('#toc > li:nth-child(3) > a').click() #Switch to Payload
    payload_eth = driver.find_element_by_id('WAN')
    payload_e1_1 = driver.find_element_by_id('E1-1')
    payload_e1_2 = driver.find_element_by_id('E1-2')
    if payload_eth.get_attribute('checked') == "true": pass #установка payload = eth
    else: payload_eth.click()
    if payload_e1_1.get_attribute('checked') == "true": payload_e1_1.click() #установка payload - e1-1
    else: pass
    if payload_e1_2.get_attribute('checked') == "true": payload_e1_2.click() #установка payload - e1-2
    else: pass
    savebutton = driver.find_element_by_css_selector('input[value="Save"]')
    savebutton.click()
    time.sleep(10)
    driver.find_element_by_css_selector('#toc > li:nth-child(6) > a').click()
    Select(driver.find_element_by_id('rstp_pbvl_0')).select_by_value("enabled") #rstp a on
    driver.find_element_by_css_selector('input[value="Save"]').click()
    driver.switch_to.default_content()
    driver.switch_to.frame('main')

set_params(pam, baserate)
