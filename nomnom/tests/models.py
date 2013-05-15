from django.db import models

class Department(models.Model):
    name = models.CharField("Name", max_length=100)
    code = models.CharField("Code", max_length=10, unique=True)
    avg_gpa = models.FloatField("Average GPA", blank=True, null=True)
    
class Course(models.Model):
    name = models.CharField("Name", max_length=100)
    ext_id = models.CharField("External ID", max_length=10, unique=True)
    credits = models.IntegerField("Credits", blank=True, null=True)

class Instructor(models.Model):
    name = models.CharField("Name", max_length=100)
    title = models.CharField("Title", max_length=100)
    department = models.ForeignKey(Department)
    courses = models.ManyToManyField(Course)