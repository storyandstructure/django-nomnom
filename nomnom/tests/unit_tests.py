from django.test import TestCase
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile

from nomnom.utils import handle_uploaded_file

import os

class UtilsTest(TestCase):
	
	def test_handle_uploaded_file(self):
		"""
		Test that Nomnom properly handles file uploads
		"""
		dir_name = os.path.dirname(__file__)
		f = open(os.path.join(dir_name, 'files/groups.csv'), "r")
		uploaded_file = SimpleUploadedFile('groups.csv', f.read())
		handle_uploaded_file(uploaded_file, 'auth', 'groups')
		
		group1 = Group.objects.get(id=1)
		self.assertEquals(group1.name, "Beatles")
	