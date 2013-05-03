from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import messages

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
		handle_uploaded_file(uploaded_file, 'auth', 'group')

        # ID given
		group1 = Group.objects.get(id=1)
		self.assertEquals(group1.name, "Beatles")

		# upload a couple Sites via CSV in the same manor as above
		# (to confirm that this solution works generically)
        # ID not given
		f2 = open(os.path.join(dir_name, 'files/sites.csv'), "r")
		uploaded_file = SimpleUploadedFile('sites.csv', f2.read())
		handle_uploaded_file(uploaded_file, 'sites', 'site')

		site1 = Site.objects.get(id=2)
		self.assertEquals(site1.domain, "nomnom.example.com")

		f3 = open(os.path.join(dir_name, 'files/groups_over.csv'), "r")
		uploaded_file = SimpleUploadedFile('groups.csv', f.read())
		handle_uploaded_file(uploaded_file, 'auth', 'group')

		uploaded_file = SimpleUploadedFile('groups_over.csv', f3.read())
		handle_uploaded_file(uploaded_file, 'auth', 'group')

        # ID overwrite
		group1 = Group.objects.get(id=1)
		self.assertEquals(group1.name, "The Beatles")

	def test_abort_on_model_error(self):
		"""
		If any line in the CSV upload will throw an error,
		commit no changes, redirect the user, and provide a helpful message
		"""
		dir_name = os.path.dirname(__file__)
		f = open(os.path.join(dir_name, 'files/groups_broken.csv'), "r")
		uploaded_file = SimpleUploadedFile('groups_broken.csv', f.read())
		output = handle_uploaded_file(uploaded_file, 'auth', 'group')

        # No groups should have been added
		self.assertEquals(Group.objects.all().count(), 0)

		# User was redirected
		self.assertEqual(type(output), 'ValidationError')
