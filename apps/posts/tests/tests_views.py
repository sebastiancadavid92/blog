from apps.posts.models import Post
from apps.users.models import User
from apps.permissions.models import PermissionCategoryPost
from apps.permissions.models import *
from django.contrib.sessions.models import Session
from rest_framework import status
from  rest_framework.test import APITestCase
from django.urls import reverse
import random

class PostCreationViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name='test name',last_name='last name test',
                                        email='test@test.com',birthdate='1992-05-25',
                                        username='testuser', password='testpassword')
        self.urllongin=reverse('login')#courd be also '/user/login/'
        self.urllogout=reverse('logout')
        self.urlcreatepost=reverse('postcreationlist')
        logindata={
            'username':'test@test.com',
            'password':'testpassword'
        }
        self.client.post(self.urllongin,logindata,format='json')
        self.data={ "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                "permission":{
                    "PUBLIC":"READ_ONLY",
                    "AUTHOR":"EDIT",
                    "TEAM":"NONE",
                    "AUTHENTICATED":"EDIT" }

                 }
        

    def testLogedUserCreatesaPost(self):
        response=self.client.post(self.urlcreatepost,self.data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def testUnloggedUserCreationPost(self):
        self.client.get(self.urllogout)
        response=self.client.post(self.urlcreatepost,self.data, format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def testAuthor(self):
        response=self.client.post(self.urlcreatepost,self.data,format='json')
        pdb=Post.objects.filter(author=self.user).count()
        self.assertEqual(pdb,1)

    def testPostCreationBadPermission(self):
       datab= { "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                "permission":{
                    "PUBLIC":"NOT A PERMISSION",
                    "AUTHOR":"EDIT",
                    "TEAM":"NONE",
                    "AUTHENTICATED":"EDIT" }

                 }
       response=self.client.post(self.urlcreatepost,datab,format='json')
       self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def testPostCreationBadPermission2(self):
       datab= { "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                "permission":{
                    "NOT A CATEGORY":"READ_ONLY",
                    "AUTHOR":"EDIT",
                    "TEAM":"NONE",
                    "AUTHENTICATED":"EDIT" }

                 }
       response=self.client.post(self.urlcreatepost,datab,format='json')
       self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def testPostCreationUncompletedPermission(self):
       datab= { "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                "permission":{
                    "AUTHOR":"EDIT",
                    "TEAM":"NONE",
                    "AUTHENTICATED":"EDIT" }

                 }
       response=self.client.post(self.urlcreatepost,datab,format='json')
       self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def testPostCreationWithEmptyPermission(self):
       datab= { "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                "permission":{
                    "PUBLIC":"",
                    "AUTHOR":"EDIT",
                    "TEAM":"NONE",
                    "AUTHENTICATED":"EDIT" }

                 }
       response=self.client.post(self.urlcreatepost,datab,format='json')
       self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def testPostCreationWithEmptyCategory(self):
       datab= { "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                "permission":{
                    "":"READ_ONLY",
                    "AUTHOR":"EDIT",
                    "TEAM":"NONE",
                    "AUTHENTICATED":"EDIT" }

                 }
       response=self.client.post(self.urlcreatepost,datab,format='json')
       self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def testPostCreationWithNoPermissions(self):
       datab= { "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                "permission":{}

                 }
       response=self.client.post(self.urlcreatepost,datab,format='json')
       self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def testPostCreationWithNoPermissions(self):
       datab= { "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",

                 }
       response=self.client.post(self.urlcreatepost,datab,format='json')
       self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def testPostCreationWithExtraCategory(self):
       datab= { "title":"Este es el titulo del post",
                "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                "permission":{
                    "PUBLIC":"READ_ONLY",
                    "AUTHOR":"EDIT",
                    "EXTRACATEG":"READ_ONLY",
                    "TEAM":"NONE",
                    "AUTHENTICATED":"EDIT" }

                 }
       response=self.client.post(self.urlcreatepost,datab,format='json')
       self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    




class PostGetViewTest(APITestCase):
    def setUp(self):

        self.userdata={
            "username":"username",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team"
        }
        self.logindata={
            'username':"test@mail.com",
            'password':'123'
        }

        self.urlregister=reverse('register')                                    
        self.urllongin=reverse('login')
        self.urllogout=reverse('logout')
        self.urlcreatepost=reverse('postcreationlist')
        self.client.post(self.urlregister,self.userdata,format='json')
        self.client.post(self.urllongin,self.logindata,format='json')
   

        self.postpublicedit={ "title":"publicnone",
                    "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                    "permission":{
                        "PUBLIC":"EDIT",
                        "AUTHOR":"NONE",
                        "TEAM":"NONE",
                        "AUTHENTICATED":"NONE"
                    }}
        self.postauthedit={ "title":"publicnone",
                    "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                    "permission":{
                        "PUBLIC":"NONE",
                        "AUTHOR":"EDIT",
                        "TEAM":"NONE",
                        "AUTHENTICATED":"NONE" }

                    }
        self.postteamedit={ "title":"publicnone",
                    "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                    "permission":{
                        "PUBLIC":"NONE",
                        "AUTHOR":"NONE",
                        "TEAM":"EDIT",
                        "AUTHENTICATED":"NONE" }

                    }
        self.postauthenedit={ "title":"publicnone",
                    "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                    "permission":{
                        "PUBLIC":"NONE",
                        "AUTHOR":"NONE",
                        "TEAM":"NONE",
                        "AUTHENTICATED":"EDIT" }
                    }
        self.postnopermission={ "title":"publicnone",
                    "content":"este es todo el contenido que tiene el post, se supone que debe tener mas de 200 caracteres para poder ver como funciona el metodo exctp pero no creo que logre alcanzar ese numero. o si? seguiere escribiendo y espero que si lo alcance . sino pues luego probare el metodo excpt de otra forma ",
                    "permission":{
                        "PUBLIC":"NONE",
                        "AUTHOR":"NONE",
                        "TEAM":"NONE",
                        "AUTHENTICATED":"NONE" }
                    }
        self.idpublic=self.client.post(self.urlcreatepost,self.postpublicedit,format='json').data.get('id')
        self.idauth=self.client.post(self.urlcreatepost,self.postauthedit,format='json').data.get('id')
        self.idteam=self.client.post(self.urlcreatepost,self.postteamedit,format='json').data.get('id')
        self.idauthen=self.client.post(self.urlcreatepost,self.postauthenedit,format='json').data.get('id')
        self.nopermid=self.client.post(self.urlcreatepost,self.postnopermission,format='json').data.get('id')

    def testPostGetPermission(self):

        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idteam}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idauthen}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        self.client.get(self.urllogout)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idteam}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idauthen}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        userdata2={
            "username":"username2",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test2@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            
        }

        self.client.post(self.urlregister,userdata2,format='json')
        self.client.post(self.urllongin,{"username":"test2@mail.com","password":"123",},format='json')
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idteam}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idauthen}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

        self.client.get(self.urllogout)
        userdata3={
            "username":"username3",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test3@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team"
            
        }

        self.client.post(self.urlregister,userdata3,format='json')
        self.client.post(self.urllongin,{"username":"test3@mail.com","password":"123",},format='json')
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idteam}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idauthen}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def testPostDeletePermission(self):

        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idteam}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauthen}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def testPostDeletePermission2(self):

        self.client.get(self.urllogout)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idteam}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauthen}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def testPostDeletePermission3(self):
        self.client.get(self.urllogout)
        userdata2={
            "username":"username2",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test2@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            
        }

        self.client.post(self.urlregister,userdata2,format='json')
        self.client.post(self.urllongin,{"username":"test2@mail.com","password":"123",},format='json')
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idteam}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauthen}))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def testPostDeletePermission4(self):
        self.client.get(self.urllogout)
        userdata3={
            "username":"username3",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test3@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team"
            
        }

        self.client.post(self.urlregister,userdata3,format='json')
        self.client.post(self.urllongin,{"username":"test3@mail.com","password":"123",},format='json')
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idteam}))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauthen}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def testDeleteDeletedPost(self):
        self.assertEqual(PermissionCategoryPost.objects.all().count(),20)
        self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        response=self.client.delete(reverse('getdeletepost',kwargs={'pk':self.idauth}))
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(PermissionCategoryPost.objects.filter(post__id=self.idauth).count(),0)
        self.assertEqual(PermissionCategoryPost.objects.all().count(),16)
  
    def testUpdatePost(self):
        postupdate={ "title":"updated tittle",
                    "content":"updated content",
                    "permission":{
                        "PUBLIC":"READ_ONLY",
                        "AUTHOR":"READ_ONLY",
                        "TEAM":"READ_ONLY",
                        "AUTHENTICATED":"READ_ONLY" }

                    }
        response=self.client.patch(reverse('getdeletepost',kwargs={'pk':self.idauth}),data=postupdate,format='json')
        self.assertEqual(response.data.get('permission'),postupdate.get('permission'))
        self.assertEqual(response.data.get('title'),postupdate.get('title'))
        self.assertEqual(response.data.get('content'),postupdate.get('content'))

    def testAdminReadAnoPermissionPost(self):
        self.client.get(self.urllogout)
        useradmindata={
            "username":"username3",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test3@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"teamadmin",
            "is_admin":"True"
        }
        self.client.post(self.urlregister,useradmindata,format='json')
        self.client.post(self.urllongin,{"username":"test3@mail.com","password":"123",},format='json')
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.nopermid}))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def testAdminEditdAnoPermissionPost(self):
        self.client.get(self.urllogout)
        useradmindata={
            "username":"username3",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test3@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"teamadmin",
            "is_admin":"True"
        }
        self.client.post(self.urlregister,useradmindata,format='json')
        self.client.post(self.urllongin,{"username":"test3@mail.com","password":"123",},format='json')

        postupdate={ "title":"updated tittle",
                    "content":"updated content",
                    "permission":{
                        "PUBLIC":"READ_ONLY",
                        "AUTHOR":"READ_ONLY",
                        "TEAM":"READ_ONLY",
                        "AUTHENTICATED":"READ_ONLY" }

                    }
        response=self.client.patch(reverse('getdeletepost',kwargs={'pk':self.nopermid}),data=postupdate,format='json')
        self.assertEqual(response.data.get('permission'),postupdate.get('permission'))
        self.assertEqual(response.data.get('title'),postupdate.get('title'))
        self.assertEqual(response.data.get('content'),postupdate.get('content'))
        

class PostListViewTest(APITestCase):
         
    def setUp(self):

        self.urlregister=reverse('register')                                    
        self.urllongin=reverse('login')
        self.urllogout=reverse('logout')
        self.urlcreatepost=reverse('postcreationlist')


        userdata={
                "username":"username",
                "first_name":"first name",
                "last_name":"last name",
                "email":"test@mail.com",
                "password":"123",
                "passwordconfirmation":"123",
                "team":"team1"
            }
        self.client.post(self.urlregister, userdata,format='json')

        self.logindata1={
                'username':"test@mail.com",
                'password':'123'
            }
        userdata={
                "username":"username2",
                "first_name":"first name",
                "last_name":"last name",
                "email":"test2@mail.com",
                "password":"123",
                "passwordconfirmation":"123",
                "team":"team1"
            }
        self.client.post(self.urlregister,userdata,format='json')

        self.logindata2={
                'username':"test2@mail.com",
                'password':'123'
            }

        userdata={
                "username":"username3",
                "first_name":"first name",
                "last_name":"last name",
                "email":"test3@mail.com",
                "password":"123",
                "passwordconfirmation":"123",
                "team":"team2"
            }
        self.client.post(self.urlregister,userdata,format='json')
            

        self.logindata3={
                'username':"test3@mail.com",
                'password':'123'
            }

        self.client.post(self.urllongin,self.logindata1,format='json')

        self.permission=['EDIT','READ_ONLY','NONE']

        for i in range(100):
            datapost={ "title":"title"+str(i),
                    "content":"content",
                    "permission":{
                        "PUBLIC":self.permission[random.randint(0, 2)],
                        "AUTHOR":self.permission[random.randint(0, 2)],
                        "TEAM":self.permission[random.randint(0, 2)],
                        "AUTHENTICATED":self.permission[random.randint(0, 2)]
                        
                        }
                    }
            self.client.post(self.urlcreatepost,datapost,format='json')




    def testAuthorList(self):
        response=self.client.get(self.urlcreatepost,format='json')
        total=Post.objects.filter(postinverse__category__categoryname='AUTHOR',postinverse__permission__permissionname__in=['EDIT','READ_ONLY']).count()
        self.assertEqual(total,response.data.get('count'))

    def testTeamlist(self):
        self.client.get(self.urllogout)
        self.client.post(self.urllongin,self.logindata2)
        response=self.client.get(self.urlcreatepost,format='json')
        total=Post.objects.filter(postinverse__category__categoryname='TEAM',postinverse__permission__permissionname__in=['EDIT','READ_ONLY']).count()
        self.assertEqual(total,response.data.get('count'))
    
    def testAuthenticatedlist(self):
        self.client.get(self.urllogout)
        self.client.post(self.urllongin,self.logindata3)
        response=self.client.get(self.urlcreatepost,format='json')
        total=Post.objects.filter(postinverse__category__categoryname='AUTHENTICATED',postinverse__permission__permissionname__in=['EDIT','READ_ONLY']).count()
        self.assertEqual(total,response.data.get('count'))

    def testPubliclist(self):
        self.client.get(self.urllogout)
        response=self.client.get(self.urlcreatepost,format='json')
        total=Post.objects.filter(postinverse__category__categoryname='PUBLIC',postinverse__permission__permissionname__in=['EDIT','READ_ONLY']).count()
        self.assertEqual(total,response.data.get('count'))

    def testAdminList(self):
        self.client.get(self.urllogout)
        userdata={
            "username":"username5",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test5@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team",
            "is_admin":"True"
        }
        logindata={
            'username':"test5@mail.com",
            'password':'123'
        }
        self.client.post(self.urlregister,userdata,format='json')
        self.client.post(self.urllongin,logindata,format='json')
        response=self.client.get(self.urlcreatepost,format='json')
        total=Post.objects.all().count()
        self.assertEqual(total,response.data.get('count'))

    def testEmptylistPublic(self):
        self.client.get(self.urllogout)
        Post.objects.filter(postinverse__category__categoryname='PUBLIC',postinverse__permission__permissionname__in=['EDIT','READ_ONLY']).delete()
        response=self.client.get(self.urlcreatepost,format='json')
        self.assertEqual(response.data,{})
        self.assertIsNone(response.data.get('count'))

    def testEmptylistAuthenticated(self):
        self.client.get(self.urllogout)
        self.client.post(self.urllongin,self.logindata3)
        Post.objects.filter(postinverse__category__categoryname='AUTHENTICATED',postinverse__permission__permissionname__in=['EDIT','READ_ONLY']).delete()
        response=self.client.get(self.urlcreatepost,format='json')
        self.assertEqual(response.data,{})
        self.assertIsNone(response.data.get('count'))
    
    def testEmptylistAdmin(self):
        self.client.get(self.urllogout)
        userdata={
            "username":"username5",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test5@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team",
            "is_admin":"True"
        }
        logindata={
            'username':"test5@mail.com",
            'password':'123'
        }
        self.client.post(self.urlregister,userdata,format='json')
        self.client.post(self.urllongin,logindata,format='json')
        Post.objects.all().delete()
        response=self.client.get(self.urlcreatepost,format='json')
        self.assertEqual(response.data,{})
        self.assertIsNone(response.data.get('count'))
        

        
        

                    
             

    


