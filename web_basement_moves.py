from selenium.webdriver.support.ui import Select
import time
import logs


def close_browser(device):
    device.driver.close()


def get_url(device):
    device.open_url()


def set_params(device, pam, baserate, channel='1', mode='Master'):
    device.driver.switch_to.frame('main')
    device.driver.find_element_by_css_selector("#toc > li:nth-child(1) > a").click()
    select = Select(device.driver.find_element_by_id("dsl1_master_mode"))
    if mode == 'Master':  # Mode chosing
        select.select_by_value("1")
    else:
        select.select_by_value("0")
    Select(device.driver.find_element_by_id("dsl1_ext")).select_by_value("1")  # Extended ON
    device.driver.find_element_by_id('dsl1_baserate').clear()
    device.driver.find_element_by_id('dsl1_baserate').send_keys(str(baserate))  # Set baserate
    select2 = Select(device.driver.find_element_by_id("dsl1_pam"))
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
    savebutton = device.driver.find_element_by_css_selector('input[value="Save"]')
    savebutton.click()
    time.sleep(1)
    device.driver.switch_to.default_content()


def configuration_menu(device):
    device.driver.switch_to.frame('left')
    device.driver.find_element_by_css_selector("tbody > tr:nth-child(10) > td > a").click()
    device.driver.switch_to.default_content()


def set_payload_eth(device):
    device.driver.switch_to.frame('main')
    device.driver.find_element_by_css_selector('#toc > li:nth-child(3) > a').click()  # Switch to Payload
    payload_eth = device.driver.find_element_by_id('WAN')
    payload_e1_1 = device.driver.find_element_by_id('E1-1')
    payload_e1_2 = device.driver.find_element_by_id('E1-2')
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
    savebutton = device.driver.find_element_by_css_selector('input[value="Save"]')
    savebutton.click()
    time.sleep(1)
    device.driver.switch_to.default_content()


def set_rstp_a_on(driver):
    driver.switch_to.frame('main')
    driver.find_element_by_css_selector('#toc > li:nth-child(6) > a').click()
    Select(driver.find_element_by_id('rstp_pbvl_0')).select_by_value("enabled")  # rstp a on
    driver.find_element_by_css_selector('input[value="Save"]').click()
    driver.switch_to.default_content()


def check_dsl_connection(device):
    device.driver.switch_to.frame('left')
    device.driver.find_element_by_css_selector("tbody > tr:nth-child(3) > td > a").click()  # переход в DSL Status
    device.driver.switch_to.default_content()
    device.driver.switch_to.frame('main')
    dsl_status = device.driver.find_element_by_css_selector("body > table > tbody > tr:nth-child(3) > td:nth-child(2)").text
    device.driver.switch_to.default_content()
    close_browser(device)
    return dsl_status


def apply_confirm(device):
    device.driver.switch_to.frame('main')
    if device.driver.find_elements_by_css_selector('input[value="Apply All"]'):
        apply_button = device.driver.find_element_by_css_selector('input[value="Apply All"]')
        apply_button.click()
        time.sleep(1)
        device.driver.switch_to.alert.accept()
        time.sleep(1)
    else:
        pass
    if device.driver.find_elements_by_css_selector('input[value="Confirm"]'):
        confirm_button = device.driver.find_element_by_css_selector('input[value="Confirm"]')
        confirm_button.click()
        time.sleep(1)
        device.driver.switch_to.alert.accept()
        time.sleep(1)
    else:
        pass
    device.driver.switch_to.default_content()


trash = '''
def test_first(driver, pam, baserate, channel='1'):
    driver.get("http://" + master_ip)
    configuration_menu(driver)
    set_payload_eth(driver)
    set_rstp_a_on(driver)
    set_params(driver, pam, baserate)
    apply_confirm(driver)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://" + slave_ip)
    configuration_menu(driver)
    set_payload_eth(driver)
    set_rstp_a_on(driver)
    set_params(pam, baserate, mode='Slave')
    apply_confirm(driver)

    result = check_dsl_connection()
    if result == '1':
        print('test passed')
    elif result == '-':
        print('dsl is not working')
    else:
        print('test failed')
    driver.close()


def test_second(driver, pam, baserate, channel='1'):  # Не настраивает payload и rstp
    driver.get("http://" + master_ip)
    configuration_menu(driver)
    set_params(driver, pam, baserate)
    apply_confirm(driver)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://" + slave_ip)
    configuration_menu(driver)
    set_params(driver, pam, baserate, mode='Slave')
    apply_confirm(driver)

    result = check_dsl_connection(driver)
    if result == '1':
        print('test passed')
    elif result == '-':
        print('dsl is not working')
    else:
        print('test failed')
    driver.close() '''
