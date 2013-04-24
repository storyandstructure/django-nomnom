from django_webtest import WebTest
from bs4 import BeautifulSoup

class NomnomTest(WebTest):

    def test_can_access_nomnom(self):
		# An administrator visits the admin site
		response = self.app.get('/admin/')
		soup = BeautifulSoup('<html>%s' % response.html)
		title = soup.find('title')
		self.assertEqual('Log in | Django site admin', title.text)
		
		self.fail('TODO')

# class NomnomRemoteTest(NomnomTest):
# 	
# 	live_server_url = 'http://localhost:8888'
# 	
# 	def setUp(self):
# 		caps = webdriver.DesiredCapabilities.FIREFOX
# 		self.browser = webdriver.Remote(
# 			command_executor='http://192.168.0.187:4444/wd/hub',
# 		    desired_capabilities=caps)
# 		self.browser.implicitly_wait(3)