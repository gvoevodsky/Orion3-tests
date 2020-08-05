from selenium import webdriver


class WebAdapter:
    '''
    Parameters is list of ip address, port and
    '''
    def __init__(self, parameters):
        self.ip = parameters[1]
        self.port = parameters[2]
        self.browser = parameters[3].capitalize()

    def open_browser(self):
        driver_init = getattr(webdriver, self.browser)
        self.driver = driver_init()
        #self.driver = driver_init(f'.\drivers\{self.browser}\driver.exe')
        return self.driver

    def open_url(self):
        self.driver.get(f'{self.ip}:{self.port}')


if __name__ == '__main__':
    io_adapter = WebAdapter(['web', 'http://192.168.1.10', '80', 'cHrOmE'])
    print(io_adapter, 'selftest')
    io_adapter.open_browser()
    io_adapter.open_url()


#    driver = webdriver.Chrome('C:\webdriverChrome\chromedriver.exe')
#   driver.implicitly_wait(5)
#   test_first()
