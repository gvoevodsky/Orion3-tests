import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

master_ip = '192.168.0.223'
slave_ip = '192.168.0.222'
baserate = 88
pam = 32


def set_params(pam, baserate, channel='1', mode='Master'):
    driver.switch_to.frame('main')
    driver.find_element_by_css_selector("#toc > li:nth-child(1) > a").click()
    select = Select(driver.find_element_by_id("dsl1_master_mode"))
    if mode == 'Master':  # Mode chosing
        select.select_by_value("1")
    else:
        select.select_by_value("0")
    Select(driver.find_element_by_id("dsl1_ext")).select_by_value("1")  # Extended ON
    driver.find_element_by_id('dsl1_baserate').clear()
    driver.find_element_by_id('dsl1_baserate').send_keys(str(baserate))  # Set baserate
    select2 = Select(driver.find_element_by_id("dsl1_pam"))
    if pam == 32:
        select2.select_by_value("1")
    elif pam == 64:
        select2.select_by_value("4")
    elif pam == 128:
        select2.select_by_value("5")
    elif pam == 16:
        select2.select_by_value("0")
    elif pam == 8:
        select2.select_by_value("2")
    elif pam == 4:
        select2.select_by_value("3")
    else:
        print('wrong baserate!')
    savebutton = driver.find_element_by_css_selector('input[value="Save"]')
    savebutton.click()
    time.sleep(1)
    driver.switch_to.default_content()


def configuration_menu():
    driver.switch_to.frame('left')
    driver.find_element_by_css_selector("tbody > tr:nth-child(10) > td > a").click()
    driver.switch_to.default_content()


def set_payload_eth():
    driver.switch_to.frame('main')
    driver.find_element_by_css_selector('#toc > li:nth-child(3) > a').click()  # Switch to Payload
    payload_eth = driver.find_element_by_id('WAN')
    payload_e1_1 = driver.find_element_by_id('E1-1')
    payload_e1_2 = driver.find_element_by_id('E1-2')
    if payload_eth.get_attribute('checked') == "true":
        pass  # установка payload = eth
    else:
        payload_eth.click()
    if payload_e1_1.get_attribute('checked') == "true":
        payload_e1_1.click()  # установка payload - e1-1
    else:
        pass
    if payload_e1_2.get_attribute('checked') == "true":
        payload_e1_2.click()  # установка payload - e1-2
    else:
        pass
    savebutton = driver.find_element_by_css_selector('input[value="Save"]')
    savebutton.click()
    time.sleep(1)
    driver.switch_to.default_content()


def set_rstp_a_on():
    driver.switch_to.frame('main')
    driver.find_element_by_css_selector('#toc > li:nth-child(6) > a').click()
    Select(driver.find_element_by_id('rstp_pbvl_0')).select_by_value("enabled")  # rstp a on
    driver.find_element_by_css_selector('input[value="Save"]').click()
    driver.switch_to.default_content()


def check_dsl_connection():
    driver.switch_to.frame('left')
    driver.find_element_by_css_selector("tbody > tr:nth-child(3) > td > a").click()  # переход в DSL Status
    time.sleep(30)  # Ожидание установки DSL соединения
    driver.switch_to.default_content()
    driver.switch_to.frame('main')
    dsl_status = driver.find_element_by_css_selector("body > table > tbody > tr:nth-child(3) > td:nth-child(2)").text
    print(dsl_status)
    driver.switch_to.default_content()
    return dsl_status


def apply_confirm():
    driver.switch_to.frame('main')
    if driver.find_elements_by_css_selector('input[value="Apply All"]'):
        apply_button = driver.find_element_by_css_selector('input[value="Apply All"]')
        apply_button.click()
        time.sleep(3)
        driver.switch_to.alert.accept()
        time.sleep(3)
    else:
        pass
    if driver.find_elements_by_css_selector('input[value="Confirm"]'):
        confirm_button = driver.find_element_by_css_selector('input[value="Confirm"]')
        confirm_button.click()
        time.sleep(3)
        driver.switch_to.alert.accept()
        time.sleep(1)
    else:
        pass
    driver.switch_to.default_content()


def test_first():
    driver.get("http://" + master_ip)
    configuration_menu()
    set_payload_eth()
    set_rstp_a_on()
    set_params(pam, baserate)
    apply_confirm()
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://" + slave_ip)
    configuration_menu()
    set_payload_eth()
    set_rstp_a_on()
    set_params(pam, baserate, mode='Slave')
    apply_confirm()

    result = check_dsl_connection()
    if result == '1':
        print('test passed')
    elif result == '-':
        print('dsl is not working')
    else:
        print('test failed')
    driver.close()


def test_second():  # Не настраивает payload и rstp
    driver.get("http://" + master_ip)
    configuration_menu()
    set_params(pam, baserate)
    apply_confirm()
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://" + slave_ip)
    configuration_menu()
    set_params(pam, baserate, mode='Slave')
    apply_confirm()

    result = check_dsl_connection()
    if result == '1':
        print('test passed')
    elif result == '-':
        print('dsl is not working')
    else:
        print('test failed')
    driver.close()


if __name__ == '__main__':
    driver = webdriver.Chrome('C:\webdriverChrome\chromedriver.exe')
    driver.implicitly_wait(5)
    test_first()
