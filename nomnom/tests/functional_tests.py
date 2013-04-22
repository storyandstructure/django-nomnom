import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class NonomTest(unittest.TestCase):

    def setUp(self):
        caps = webdriver.DesiredCapabilities.FIREFOX
        self.browser = webdriver.Remote(
                command_executor='http://192.168.0.187:4444/wd/hub',
                desired_capabilities=caps)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    # As an administrator, I can go to /admin/ so that I can login.
    def test_can_go_to_admin_url(self):
        self.browser.get('http://localhost:8888/admin')
        self.assertIn('Log in', self.browser.title)

    # As an administrator, I can login so that I enter the admin site.
    def test_can_login_admin_site(self):
        self.fail('TODO')

    # As an administrator, I can access the NomNom interface so that I can
    # import or export data
    #assert 'Django' in browser.title
    #browser.get('http://localhost:8888')
    def test_can_access_nomnom(self):
        self.fail('TODO')

if __name__ == '__main__':
    unittest.main()
