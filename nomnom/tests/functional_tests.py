from django_webtest import WebTest
from bs4 import BeautifulSoup


class NomnomTest(WebTest):

    def test_can_access_nomnom(self):
    # An administrator visits the admin site
        response = self.app.get('/admin/')
        soup = BeautifulSoup('<html>%s' % response.html)
        title = soup.find('title')
        self.assertEqual('Log in | Django site admin', title.text)

        # As an administrator, I can click the Import button so that I can
        # import files.
        user = self.app.get('/admin/auth/user')
        assert 'Import Users' in user.click('Import users')

        # As an administrator, I can click the Export button so that I can
        # export files.
        user = self.app.get('/admin/auth/user')
        assert 'Export Users' in user.click('Export users')

        self.fail('TODO')
