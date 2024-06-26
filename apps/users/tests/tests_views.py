from apps.users.models import User,Team
from django.contrib.sessions.models import Session
from rest_framework import status
from  rest_framework.test import APITestCase
from django.urls import reverse
class AutenticacionAPITestCase(APITestCase):
    def setUp(self):
        self.team=Team.objects.create(team_name='DEFAULT')
        self.user = User.objects.create(first_name='test name',last_name='last name test',
                                        email='test@test.com',birthdate='1992-05-25',
                                        username='testuser', password='testpassword',team=self.team)
        self.urllongin=reverse('login')#courd be also '/user/login/'
        self.urllogout=reverse('logout')

    def testLogin(self):
         
        data = {'username': 'test@test.com', 'password': 'testpassword'}
        response = self.client.post(self.urllongin, data, format='json')
        sessio=Session.objects.filter(session_key=response.cookies['sessionid'].value).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertIsNotNone(response.cookies['csrftoken'].value)
        self.assertIsNotNone(Session.objects.filter(session_key=response.cookies['sessionid'].value))
        
    def testBadLogin(self):
        data={'username':'','password':'123'}
        response = self.client.post(self.urllongin, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    def testBadLogin2(self):
        data={'username':'test@test.com','password':''}
        response = self.client.post(self.urllongin, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
    
    def testBadLogin3(self):
        data={'username':'','password':''}
        response = self.client.post(self.urllongin, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 


    def testLoginBadData(self):

        data = {'username': 'badtest@test.com', 'password': 'testpassword'}
        response = self.client.post(self.urllongin, data, format='json')
        self.assertIsNotNone(response.data['error'])
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
       

    def testDoubleLoginIn(self):
        data = {'username': 'test@test.com', 'password': 'testpassword'}
        self.client.post(self.urllongin, data, format='json')
        self.client.post(self.urllongin, data, format='json')
        self.assertEqual(Session.objects.all().count(),1)
  

    def testLogout(self):
        data = {'username': 'test@test.com', 'password': 'testpassword'}
        self.client.post(self.urllongin, data, format='json')
        response=self.client.get(self.urllogout)
        self.assertIsNotNone(response.data['message'])
        self.assertIsNone(Session.objects.all().first())
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def testLogoutunLoggedUser(self):
        response=self.client.get(self.urllogout)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)




class RegistrationAPITestCase(APITestCase):
    def setUp(self):
        self.urllongin=reverse('login')
        self.urllogout=reverse('logout')
        self.urlregister=reverse('register')
        self.team=Team.objects.create(team_name='DEFAULT')

        self.userdata={
            "username":"username",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team"
        }
    def test_RegisterUser(self):
        response=self.client.post(self.urlregister,self.userdata,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIsNotNone(User.objects.get(username=self.userdata['username']))
        self.assertEqual(response.data['is_admin'],False)
        
    def test_RegisterExistingUser(self):
        self.client.post(self.urlregister,self.userdata,format='json')
        response=self.client.post(self.urlregister,self.userdata,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_RegisterUserBadData(self):
        userb=self.userdata
        userb.pop('username')
        userb.pop('first_name')
        userb.pop('email')
        userb.pop('last_name')
        userb.pop('password')
        userb.pop('passwordconfirmation')
        response=self.client.post(self.urlregister,userb,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data['username'],list)
        self.assertIsInstance(response.data['email'],list)
        self.assertIsInstance(response.data['password'],list)
        self.assertIsInstance(response.data['passwordconfirmation'],list)
        self.assertNotIn('last_name',response.data)

    def testResgisterUserBadFname(self):
        userdata={
            "username":"username2",
            "first_name":"first name@1",
            "last_name":"last name",
            "email":"test@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team"
        }
        response=self.client.post(self.urlregister,userdata,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def testResgisterUserBadLname(self):
        userdata={
            "username":"username2",
            "first_name":"first name",
            "last_name":"last name@#",
            "email":"test@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team"
        }
        response=self.client.post(self.urlregister,userdata,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def testResgisterUserBirthdate(self):
        userdata={
            "username":"username2",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team",
            "birthdate":"2222-10-10"
        }
        response=self.client.post(self.urlregister,userdata,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def testResgisterUserNoPassowrd(self):
        userdata={
            "username":"username2",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test@mail.com",
            "password":"",
            "passwordconfirmation":"hgu",
            "team":"test team",
  
        }
        response=self.client.post(self.urlregister,userdata,format='json')   
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def testResgisterUserNoMatchesPassowrd(self):
        userdata={
            "username":"username2",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test@mail.com",
            "password":"aseasd",
            "passwordconfirmation":"faseq",
            "team":"test team",
        }
        response=self.client.post(self.urlregister,userdata,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)




    def test_IsAdminGiven(self):
        self.userdata['is_admin']='True'
        response=self.client.post(self.urlregister,self.userdata,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username=self.userdata['username']).first().is_admin,True)

    def test_EmailNameValidation(self):
        self.userdata['email']='notanemail.com'
        self.userdata['first_name']='no-a-name'
        response=self.client.post(self.urlregister,self.userdata,format='json')
        self.assertIsInstance(response.data['first_name'],list)
        self.assertIsInstance(response.data['email'],list)
        
    def test_LoggedUserRegistering(self):

        user = User.objects.create(first_name='test name',last_name='last name test',
                                        email='test@test.com',birthdate='1992-05-25',
                                        username='testuser', password='testpassword',team=self.team)
        datalogin = {'username': 'test@test.com', 'password': 'testpassword'}
        responselogin = self.client.post(self.urllongin, datalogin, format='json')
        self.assertEqual(responselogin.status_code,status.HTTP_200_OK)
        response2=self.client.post(self.urlregister,self.userdata,headers={'X-CSRFToken':responselogin.cookies['csrftoken'].value},format='json')
        self.assertEqual(response2.status_code,status.HTTP_403_FORBIDDEN)
        response3=self.client.post(self.urlregister,self.userdata,headers=responselogin.headers,format='json')
        self.assertEqual(response3.status_code,status.HTTP_403_FORBIDDEN)


