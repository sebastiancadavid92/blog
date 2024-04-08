from django.test import TestCase
from .factory import *
class test_PermissionCategoryPos(TestCase):
     
    @classmethod
    def setUpClass(cls):
        cls.categorypublic=CategoryFactory()
# Create your tests here.
