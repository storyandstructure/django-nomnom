from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Group, Permission
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile

# weird stuff for the models test
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading

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
		
		# The function returns a ValueError
		self.assertEqual(type(output), ValueError)
		
	def test_abort_on_m2m_does_not_exist(self):
		"""
		Quit early if an id for a m2m doesn't exist
		"""
		dir_name = os.path.dirname(__file__)
		f = open(os.path.join(dir_name, 'files/groups_with_bad_perms.csv'), "r")
		uploaded_file = SimpleUploadedFile('groups_with_bad_perms.csv', f.read())
		output = handle_uploaded_file(uploaded_file, 'auth', 'group')

        # No groups should have been added
 		self.assertEquals(Group.objects.all().count(), 0)
		
		# The function returns a ValueError
		self.assertEqual(output, "The following values do not exist in the model for the 'permissions' field: 400, 300")
		
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
		
class ModelsTest(TestCase):
	"""
	These tests require the existence of the models in nomnom/tests/models.py,
	hence they are separated from the others. Technique described here:
	http://stackoverflow.com/questions/502916/django-how-to-create-a-model-dynamically-just-for-testing
	"""
	
	def setUp(self):
		apps = list(settings.INSTALLED_APPS)
		apps.append('nomnom.tests')
		settings.INSTALLED_APPS = tuple(apps)
		loading.cache.loaded = False
		call_command('syncdb', verbosity=0)
		
		from nomnom.tests.models import Department, Instructor, Course
		self.department1 = Department(name="Intergalactic Exploration", code="INX")
		self.department1.save()
		self.instructor1 = Instructor(name="James Kirk", title="Capt.", department=self.department1)
		self.instructor1.save()
		self.course1 = Course(name="Photon-based Ballistics", ext_id="INX-324")
		self.course1.save()
		self.department2 = Department(name="Paranormal Investigation", code="PNV")
		self.department2.save()
		self.instructor2 = Instructor(name="Peter Venkman", title="Dr.", department=self.department2)
		self.instructor2.save()
		self.course2 = Course(name="Proton Pack Safety", ext_id="PNV-252")
		self.course2.save()
		self.course3 = Course(name="Spores, Molds, and Fungus", ext_id="PNV-112")
		self.course3.save()
		
	def test_export_fk_as_id(self):
		"""
		CSVs should (by default) export FKs as IDs, not titles
		"""
		from nomnom.tests.models import Instructor
		request_factory = RequestFactory()
		req = request_factory.get('/admin/test/instructor/')
				
		response = export_as_csv(modeladmin=self.instructor1.__class__, 
								request=req, 
								queryset=Instructor.objects.all(), 
								export_type="D")
				
		expected_response = 'department,title,id,name,courses\r\n1,Capt.,1,James Kirk,\r\n2,Dr.,2,Peter Venkman,'

		self.assertContains(response, expected_response)
		
	def test_upload_m2m_as_unique(self):
		"""
		Allow unique-field values in M2M columns in the CSV upload
		"""
		dir_name = os.path.dirname(__file__)
		f = open(os.path.join(dir_name, 'files/instructors.csv'), "r")
		uploaded_file = SimpleUploadedFile('instructors.csv', f.read())
		output = handle_uploaded_file(uploaded_file, 'tests', 'instructor')

		from nomnom.tests.models import Instructor, Course

        # 4 Instructors total
 		self.assertEquals(Instructor.objects.all().count(), 4)
		
		# Courses were properly attributed to Instructors
		courses = Course.objects.get(id__in=[2,3])
		spengler = Instructor.objects.get(id=3)
		self.assertQuerysetEqual(spangler.courses.all(), [repr(c) for c in courses], ordered=False)
		