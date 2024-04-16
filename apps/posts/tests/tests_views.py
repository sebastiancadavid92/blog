from apps.posts.models import Post
from apps.users.models import User
from apps.permissions.models import *
from django.contrib.sessions.models import Session
from rest_framework import status
from  rest_framework.test import APITestCase
from django.urls import reverse

class PostCreationViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(first_name='test name',last_name='last name test',
                                        email='test@test.com',birthdate='1992-05-25',
                                        username='testuser', password='testpassword')
        self.urllongin=reverse('login')#courd be also '/user/login/'
        self.urllogout=reverse('logout')
        self.urlcreatepost=reverse('postcreation')
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
        self.urlcreatepost=reverse('postcreation')
        self.client.post(self.urlregister,self.userdata,format='json')
        ra=self.client.post(self.urllongin,self.logindata,format='json')

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
        self.idpublic=self.client.post(self.urlcreatepost,self.postpublicedit,format='json').data.get('id')
        self.client.post(self.urlcreatepost,self.postauthedit,format='json')
        self.client.post(self.urlcreatepost,self.postteamedit,format='json')
        self.client.post(self.urlcreatepost,self.postauthenedit,format='json')

    def testPostGet(self):
        response=self.client.get(reverse('getdeletepost',kwargs={'pk':self.idpublic}))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

