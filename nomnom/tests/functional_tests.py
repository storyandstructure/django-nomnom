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
        
        # As a non-staff user, I cannot access nomnom's import page
        nomnom_auth_groups = self.app.get('/nomnom/auth/group/import/')
        self.assertContains(nomnom_auth_groups, text='id="login-form"', status_code=200)

        # As an administrator, I can click the Import button so that I can
        # import files.
        user = self.app.get('/admin/auth/user/', user="admin")
        assert 'Import Users' in user.click('Import users')

        # As an administrator, I can click the Export button so that I can
        # export files.
        # user = self.app.get('/admin/auth/user')
        # assert 'Export Users' in user.click('Export users')

        self.fail('TODO')
