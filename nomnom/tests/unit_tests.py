from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Group, Permission
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from nomnom.utils import handle_uploaded_file
from nomnom.actions import export_as_csv

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

        # ID not given
		group1 = Group.objects.get(id=1)
		self.assertEquals(group1.name, "Beatles")

		# upload a couple Sites via CSV in the same manor as above
		# (to confirm that this solution works generically)
        # ID not given
		f2 = open(os.path.join(dir_name, 'files/sites.csv'), "r")
		uploaded_file2 = SimpleUploadedFile('sites.csv', f2.read())
		handle_uploaded_file(uploaded_file2, 'sites', 'site')

		site1 = Site.objects.get(id=2)
		self.assertEquals(site1.domain, "nomnom.example.com")

		# overwrite some existing models with a new upload
		f3 = open(os.path.join(dir_name, 'files/groups_over.csv'), "r")
		uploaded_file3 = SimpleUploadedFile('groups_over.csv', f3.read())
		handle_uploaded_file(uploaded_file3, 'auth', 'group')

        # ID overwrite
		group1_again = Group.objects.get(id=1)
		self.assertEquals(group1_again.name, "The Beatles")

	def test_handle_uploaded_file_m2m(self):
		"""
		Test that Nomnom properly handles file uploads
		"""
		dir_name = os.path.dirname(__file__)
		f = open(os.path.join(dir_name, 'files/groups_with_perms.csv'), "r")
		uploaded_file = SimpleUploadedFile('groups_with_perms.csv', f.read())
		handle_uploaded_file(uploaded_file, 'auth', 'group')

		group1 = Group.objects.get(id=1)
		
		perms = Permission.objects.filter(id__in=[1,2])

 		self.assertQuerysetEqual(group1.permissions.all(), [repr(p) for p in perms], ordered=False)
		
		
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
		
		# The function returns a ValidationError
		self.assertEqual(type(output), ValidationError)
		
	def test_export_as_csv(self):
		"""
		Download a CSV with all of the fields in a model. ForeignKeys are
		ID's (for now), and ManyToManys are a quoted comma separated list
		"""
		permission1 = Permission.objects.get(id=1)
		permission2 = Permission.objects.get(id=2)
		group1 = Group(name="Group 1")
		group1.save()
		group1.permissions.add(permission1)
		group1.permissions.add(permission2)
		group2 = Group(name="Group 2")
		group2.save()
		group2.permissions.add(permission1)
		
		# test request
		request_factory = RequestFactory()
		req = request_factory.get('/admin/auth/user/')
				
		response = export_as_csv(modeladmin=group1.__class__, 
								request=req, 
								queryset=Group.objects.all(), 
								export_type="D")
		
		expected_response = 'id,name,permissions\r\n1,Group 1,"1,2,"\r\n2,Group 2,"1,"'

		self.assertContains(response, expected_response)	
		