from django.test import TestCase
from ..factories import *
from ..models import *
from apps.posts.factories import PostFactory
from django.db import IntegrityError
import re
class test_PermissionCategoryPost(TestCase):
     
    @classmethod
    def setUpClass(cls):
        super(test_PermissionCategoryPost,cls).setUpClass()
        CategoryFactory.reset_sequence()
        PermissionFactory.reset_sequence()
        cls.categories=CategoryFactory.create_batch(4)
        cls.permissions=PermissionFactory.create_batch(3)
        cls.post=PostFactory.create_batch(18)
        for i in range(0,18,1):
            for cate in cls.categories:

                if 0<=i<3:
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[2])
                elif 3<=i<6:
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[0])
                elif 6<=i<9:
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[1])
                elif 9<=i<12 and( cate.categoryname=='AUTHOR'or cate.categoryname=='PUBLIC'):
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[0])
                elif 9<=i<12 and cate.categoryname=='TEAM':
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[1])
                elif 9<=i<12  and cate.categoryname=='AUTHENTICATED':
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[2])
                elif 12<=i<15 and (cate.categoryname=='AUTHOR'or cate.categoryname=='PUBLIC'):
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[1])
                elif 12<=i<15 and cate.categoryname=='TEAM':
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[2])
                elif 12<=i<15  and cate.categoryname=='AUTHENTICATED':
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[0])
                elif 15<=i<=17   and (cate.categoryname=='AUTHOR'or cate.categoryname=='PUBLIC'):
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[2])
                elif 15<=i<=17 and cate.categoryname=='TEAM':
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[0])
                elif 15<=i<=17 and cate.categoryname=='AUTHENTICATED':
                    PermissionCategoryPostFactory.create(post=cls.post[i],category=cate, permission=cls.permissions[1])

    def testCreateCatgories(self):
        self.assertIsInstance(self.categories[0],Category)

    def testCreatePermission(self):
        self.assertIsInstance(self.permissions[0],Permission)

    def testCreatePermissionCategoryPost(self):
        self.assertEqual(PermissionCategoryPost.objects.all().count(),18*4)
        self.assertEqual(Category.objects.all().count(),4)
        self.assertEqual(Permission.objects.all().count(),3)
    
    def testNotAllowedMoreThanTwoPermissionsPerCategory(self):
        post=PostFactory.create()
        with self.assertRaises(IntegrityError):
            PermissionCategoryPostFactory(post=post, category=self.categories[0], permission=self.permissions[0])
            PermissionCategoryPostFactory(post=post, category=self.categories[0], permission=self.permissions[1])

    def testShowpermissioncategorypost(self):
        postsauthornone = Post.objects.filter(postinverse__category__categoryname='AUTHOR',postinverse__permission__permissionname='NONE')
        postreamread=Post.objects.filter(postinverse__category__categoryname='TEAM',
                                            postinverse__permission__permissionname='READ_ONLY')
        self.assertEqual((postreamread.union(postsauthornone)).count(),3*3) 
    
    def testDeletePermissionCategorybyDeletingaPost(self):
        postdb=Post.objects.filter(id=self.post[0].id)
        postdb.delete()
        self.assertEqual(PermissionCategoryPost.objects.all().count(),17*4)
        self.assertEqual(Permission.objects.all().count(),3)
        self.assertEqual(Category.objects.all().count(),4)

    def testStrPermissionMethod(self):
        permission=PermissionFactory(permissionname='EDIT')  
        self.assertEqual(permission.__str__(),'EDIT')

    def testStrCategoryMethod(self):
        cate=CategoryFactory(categoryname='PUBLIC')      
        
        self.assertEqual(cate.__str__(),'PUBLIC')

    def testStrPosPermissionCategorytMethod(self):
        post=PostFactory(title='title post') 
        cate=CategoryFactory(categoryname='PUBLIC')
        permission=PermissionFactory(permissionname='EDIT')         
        cpp=PermissionCategoryPostFactory(category=cate,post=post,permission=permission)
        pattern = r'^\d+->PUBLIC=EDIT$'
        self.assertIsNotNone(re.match(pattern,cpp.__str__()))
    
# Create your tests here.
