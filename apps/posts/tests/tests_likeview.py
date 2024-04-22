from apps.posts.models import Post,Like
from apps.users.models import User
from apps.permissions.models import *
from rest_framework import status
from  rest_framework.test import APITestCase

from django.urls import reverse
import random

class LikeCreationDeletionViewTest(APITestCase):
    def setUp(self):
        
        self.urlregister=reverse('register')                                    
        self.urllongin=reverse('login')
        self.urllogout=reverse('logout')
        self.urlcreatepost=reverse('postcreationlist')
        self.permission=['EDIT','READ_ONLY','NONE']

        for i in range(2):
            data={ 
            "username":"username"+str(i),
            "first_name":"first name",
            "last_name":"last name",
            "email":"test"+str(i)+"@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team1" ,   
        }
            self.client.post(self.urlregister,data=data,format='json')

        data={ 
            "username":"username4",
            "first_name":"first name",
            "last_name":"last name",
            "email":"test4@mail.com",
            "password":"123",
            "passwordconfirmation":"123",
            "team":"test team2" ,
            "is_admin":"True"   
        }
        self.client.post(self.urlregister,data=data,format='json')

        data={ 
                "username":"test1@mail.com",
                "password":"123"
            }
        self.client.post(self.urllongin,data=data,format='json')

        datapost={ "title":"title 1 autho 1",
                    "content":"content",
                    "permission":{
                        "PUBLIC":self.permission[1],
                        "AUTHOR":self.permission[1],
                        "TEAM":self.permission[1],
                        "AUTHENTICATED":self.permission[1]
                        }
                    }
        self.client.post(self.urlcreatepost,datapost,format='json')
        self.client.get(self.urllogout,data=data,format='json')
        
    def testLikeCreation(self):
        data={
                "username":"test1@mail.com",
                "password":"123"
            }
        self.client.post(self.urllongin,data=data,format='json')        
        post_id=Post.objects.first().id
        url=f'/post/{post_id}/like/'
        response=self.client.post(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        cont=Like.objects.all().count()
        self.assertEqual(cont,1)
        
    def testCantDoubleLike(self):
        data={
                "username":"test1@mail.com",
                "password":"123"
            }
        self.client.post(self.urllongin,data=data,format='json')        
        post_id=Post.objects.first().id
        url=f'/post/{post_id}/like/'
        self.client.post(url,format='json')
        response=self.client.post(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        
    def testCantLikeWithNoPermisisons(self):
        data={
                "username":"test1@mail.com",
                "password":"123"
            }
        self.client.post(self.urllongin,data=data,format='json')
        datapost={ "title":"post no permissions",
                    "content":"content",
                    "permission":{
                        "PUBLIC":self.permission[2],
                        "AUTHOR":self.permission[2],
                        "TEAM":self.permission[2],
                        "AUTHENTICATED":self.permission[2]
                        }
                    }
        self.client.post(self.urlcreatepost,datapost,format='json')
        post_id=Post.objects.filter(title="post no permissions").first().id
        url=f'/post/{post_id}/like/'
        response=self.client.post(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
    def testDeleteLike(self):
        data={
                "username":"test1@mail.com",
                "password":"123"
            }
        self.client.post(self.urllongin,data=data,format='json')        
        post_id=Post.objects.first().id
        url=f'/post/{post_id}/like/'
        self.client.post(url,format='json')
        like_id=Like.objects.all().first().id
        url=f'/post/{post_id}/like/{like_id}/'
        response=self.client.delete(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT) 
        
    def testDeleteLikeDoestExist(self):
        data={
                "username":"test1@mail.com",
                "password":"123"
            }
        self.client.post(self.urllongin,data=data,format='json')        
        post_id=Post.objects.first().id
        url=f'/post/{post_id}/like/1/'
        self.assertEqual(Like.objects.all().count(),0)
        response=self.client.delete(url,format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND) 
        
class LikeListPaginationViewTest(APITestCase):
    
    def setUp(self):

        self.urlregister=reverse('register')                                    
        self.urllongin=reverse('login')
        self.urllogout=reverse('logout')
        self.urlcreatepost=reverse('postcreationlist')
        self.permission=['EDIT','READ_ONLY','NONE']


        userdata={
                "username":"username1",
                "first_name":"first name",
                "last_name":"last name",
                "email":"test1@mail.com",
                "password":"123",
                "passwordconfirmation":"123",
                "team":"team1"
            }
        self.client.post(self.urlregister, userdata,format='json')
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
        
        datalogin={
                "username":"test1@mail.com",
                "password":"123",
        }
        self.client.post(self.urllongin,datalogin,format='json')
        datapost={ "title":"post no permissions",
                    "content":"content",
                    "permission":{
                        "PUBLIC":self.permission[0],
                        "AUTHOR":self.permission[0],
                        "TEAM":self.permission[0],
                        "AUTHENTICATED":self.permission[0]
                        }
                    }
        self.client.post(self.urlcreatepost,datapost,format='json')
        postid=Post.objects.all().first().id
        url=f'/post/{postid}/like/'
        for i in range(4,25):
            self.client.get(self.urllogout, format='json')
            userdata={
                "username":"username"+str(i),
                "first_name":"first name",
                "last_name":"last name",
                "email":"test"+str(i)+"@mail.com",
                "password":"123",
                "passwordconfirmation":"123",
                "team":"team2"
            }
            datalogin={
                "username":"test"+str(i)+"@mail.com",
                "password":"123",
                
                
            }
            self.client.post(self.urlregister,userdata,format='json')
            self.client.post(self.urllongin,datalogin,format='json')
            self.client.post(url,format='json')
       
        self.urllistlike=reverse('listlikes')
        self.post=Post.objects.all().first()
        self.client.get(self.urllogout, format='json')
        
    def testLikelistforAuthor(self):
        datalogin={
                "username":"test1@mail.com",
                "password":"123",
        }
        self.client.post(self.urllongin,datalogin,format='json')
        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),21)
        postupdate={ "title":"updated tittle",
                    "content":"updated content",
                    "permission":{
                        "PUBLIC":"READ_ONLY",
                        "AUTHOR":"NONE",
                        "TEAM":"READ_ONLY",
                        "AUTHENTICATED":"READ_ONLY" }

                    }
        response=self.client.patch(reverse('getdeletepost',kwargs={'pk':self.post.id}),data=postupdate,format='json')
        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),0)

        
    def testLikelistforAuthenticated(self):
        datalogin={
                "username":"test3@mail.com",
                "password":"123",
        }
        self.client.post(self.urllongin,datalogin,format='json')
        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),21)
        postupdate={ "title":"updated tittle",
                    "content":"updated content",
                    "permission":{
                        "PUBLIC":"READ_ONLY",
                        "AUTHOR":"EDIT",
                        "TEAM":"EDIT",
                        "AUTHENTICATED":"NONE" }

                    }
        response=self.client.patch(reverse('getdeletepost',kwargs={'pk':self.post.id}),data=postupdate,format='json')
        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),0)
    
    def testLikelistforTeam(self):
        datalogin={
                "username":"test2@mail.com",
                "password":"123",
        }
        self.client.post(self.urllongin,datalogin,format='json')
        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),21)
        postupdate={ "title":"updated tittle",
                    "content":"updated content",
                    "permission":{
                        "PUBLIC":"READ_ONLY",
                        "AUTHOR":"EDIT",
                        "TEAM":"NONE",
                        "AUTHENTICATED":"READ_ONLY" }

                    }
        response=self.client.patch(reverse('getdeletepost',kwargs={'pk':self.post.id}),data=postupdate,format='json')
        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),0)
        
    def testLikelistforPublic(self):

        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),21)
        postupdate={ "title":"updated tittle",
                    "content":"updated content",
                    "permission":{
                        "PUBLIC":"NONE",
                        "AUTHOR":"EDIT",
                        "TEAM":"EDIT",
                        "AUTHENTICATED":"READ_ONLY" }

                    }
        response=self.client.patch(reverse('getdeletepost',kwargs={'pk':self.post.id}),data=postupdate,format='json')
        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),0)
        
    def testLikePagination(self):
        datalogin={
                "username":"test1@mail.com",
                "password":"123",
        }
        self.client.post(self.urllongin,datalogin,format='json')
        response=self.client.get(self.urllistlike,format='json')
        self.assertEqual(response.data.get('count'),21)
        self.assertEqual(len(response.data['results']),20)
        self.assertEqual(response.data['next'],'http://testserver/likes/?page=2')
        self.assertEqual(response.data['current'],1)
        self.assertEqual(response.data['num_pages'],2)
        response=self.client.get(response.data['next'],format='json')
        self.assertEqual(response.data['previous'],'http://testserver/likes/')
        self.assertEqual(response.data['current'],2)
        self.assertEqual(len(response.data['results']),1)
        
    def testLikeFilterbyPost(self):
        datalogin={
                "username":"test1@mail.com",
                "password":"123",
        }
        self.client.post(self.urllongin,datalogin,format='json')
        url=self.urllistlike+"?post="+str(self.post.id)##+"&user="+str(7)
        response=self.client.get(url,format='json')
        self.assertEqual(response.data['count'],21)
        url=self.urllistlike+"?post="+str(22) # unexisting post
        response=self.client.get(url,format='json')
        self.assertEqual(response.data['count'],0)
            
    def testLikeFilterbyUser(self):
        datalogin={
                "username":"test1@mail.com",
                "password":"123",
        }
        
        self.client.post(self.urllongin,datalogin,format='json')
        user=User.objects.all()[5]
        url=self.urllistlike+"?user="+str(user.id)##+"&user="+str(7)
        response=self.client.get(url,format='json')
        self.assertEqual(response.data['count'],1)
        url=self.urllistlike+"?user="+str(2222) # unexisting user
        response=self.client.get(url,format='json')
        self.assertEqual(response.data['count'],0)
    def testLikeFilterbyUserandPost(self):
        datalogin={
                "username":"test1@mail.com",
                "password":"123",
        }
        self.client.post(self.urllongin,datalogin,format='json')
        user5=User.objects.all()[5]
        url=self.urllistlike+"?user="+str(user5.id)+"&post="+str(self.post.id)
        response=self.client.get(url,format='json')
        self.assertEqual(response.data['count'],1)
        url=self.urllistlike+"?user="+str(User.objects.all()[0].id)+"&post="+str(self.post.id) # existing user didnt comment the post
        response=self.client.get(url,format='json')
        self.assertEqual(response.data['count'],1)
        url=self.urllistlike+"?user="+str(22222)+"&post="+str(self.post.id) # unexisting with existing post
        response=self.client.get(url,format='json')
        self.assertEqual(response.data['count'],0)
        url=self.urllistlike+"?user="+str(user.id)+"&post="+str(100) # unexisting post with existing user who has a like in a different post
        response=self.client.get(url,format='json')
        self.assertEqual(response.data['count'],0)