from django.test import TestCase
from django.contrib.auth.models import Group

from nomnom.utils import handle_uploaded_file

import os

class UtilsTest(TestCase):
	
	def test_handle_uploaded_file(self):
		"""
		Test that Nomnom properly handles file uploads
		"""
		dir_name = os.path.dirname(__file__)
		handle_uploaded_file(os.path.join(dir_name, 'files/group.csv'))
	
		# self.assertExists(Groups.objects.get(id=1))
	
		group1 = Group.objects.get(id=1)
		self.assertEquals(group1.name, "Beatles")
	