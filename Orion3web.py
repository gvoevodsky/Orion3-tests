from selenium import webdriver


class WebAdapter:
    '''
    Parameters is list of ip address, port and
    '''

    def __init__(self, parameters):
        # self.method = parameters[0]
        self.protocol = parameters[1]
        self.ip = parameters[2]
        self.port = parameters[3]
        self.browser = parameters[4].capitalize()

    def open_browser(self):
        driver_init = getattr(webdriver, self.browser)
        self.driver = driver_init(f'.\drivers\{self.browser}\driver.exe')
        self.driver.implicitly_wait(1)
        return self.driver

    def open_url(self):
        self.open_browser()
        print(f'opening {self.protocol}:{self.ip}:{self.port}')
        self.driver.get(f'{self.protocol}:{self.ip}:{self.port}')

    def close_browser(self):
        self.driver.close()


if __name__ == '__main__':
    io_adapter = WebAdapter(['web', 'http', '//192.168.1.10', '80', 'cHrOmE'])
    print(io_adapter, 'selftest')
    io_adapter.open_url()

