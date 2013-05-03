from django_webtest import WebTest
from bs4 import BeautifulSoup

from django.contrib.admin.models import User


class NomnomTest(WebTest):

    fixtures = ['users.json',]

    def test_can_access_nomnom(self):
    	# An administrator visits the admin site
        response = self.app.get('/admin/')
        soup = BeautifulSoup('<html>%s' % response.html)
        title = soup.find('title')
        self.assertEqual('Log in | Django site admin', title.text)

        # As an administrator, I can click the Import button so that I can
        # import files.
        user = self.app.get('/admin/auth/user/', user="admin")
        assert 'NomNom Users' in user.click('NomNom users')

        # As an administrator, I can click the Export button so that I can
        # export files.
        # user = self.app.get('/admin/auth/user')
        # assert 'Export Users' in user.click('Export users')

        self.fail('TODO')
