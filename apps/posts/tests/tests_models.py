from django.test import TestCase
from apps.users.models import *
from ..factories import  *
from ..models import *
from django.db import IntegrityError

class test_PostModel(TestCase):

    @classmethod
    def setUpClass(cls):

        super().setUpClass()
        cls.user = User.objects.create_user(first_name='test author name',last_name='last name test',
                                        email='test@test.com',birthdate='1992-05-25',
                                        username='testuser', password='testpassword')
        team = Team.objects.create(team_name='Test Team')
        cls.user.team=team

        cls.post=PostFactory(author=cls.user)

        # team creations
        cls.teams=TeamFactory.create_batch(3)
        #users in teams creation
        cls.usersteam1=UserFactory.create_batch(3,team=cls.teams[0])
        cls.usersteam3=UserFactory(team=cls.teams[2])
        cls.usersteam2=UserFactory.create_batch(2,team=cls.teams[1])
        # post creation
        cls.postuser1team1=PostFactory.create_batch(3,author=cls.usersteam1[0])
        cls.postuser2team1=PostFactory(author=cls.usersteam1[1])

        cls.postuser1team2=PostFactory.create_batch(3,author=cls.usersteam2[0])
        cls.postuser2team2=PostFactory.create_batch(3,author=cls.usersteam2[1])

        # users in team 1= 3
        # users in team 2 = 2
        # users in team 3= 1
        #post in team 1 = 4
        #post in team  2 = 6
        #post in team 3 = 0
        # post in the other team=1
        #total post= 10

        #comments creation
        #coments from different team
        CommentFactory.create_batch(2,user=cls.usersteam2[0],post=cls.postuser1team1[0])
        CommentFactory(user=cls.usersteam1[0],post=cls.postuser1team1[0])
        CommentFactory(user=cls.usersteam1[1],post=cls.postuser1team1[0])

        #likes creation
        LikeFactory(user=cls.usersteam2[0],post=cls.postuser1team1[0])
        LikeFactory(user=cls.usersteam1[0],post=cls.postuser1team1[0])
        LikeFactory(user=cls.usersteam1[1],post=cls.postuser1team1[0])


   
    def testCreatePost(self):
        postf=PostFactory(author=self.user)
        postdb=Post.objects.filter(id=postf.id).first()
        self.assertEqual(postdb.title,postf.title)
        self.assertEqual(postdb.author,postf.author)
        self.assertEqual(postdb.timestamp,postf.timestamp)
        self.assertEqual(postdb.content,postf.content)
        postdb.delete()
        postdb=Post.objects.filter(id=postf.id).first()
        self.assertEqual(postdb,None)

    def testCreateComents(self):
        user2=UserFactory()
        comment=CommentFactory(post=self.post, user=user2)
        comendb=Comment.objects.filter(id=comment.id).first()
        self.assertEqual(comendb,comment)
        comendb.delete()
        comendb=Comment.objects.filter(id=comment.id).first()
        self.assertEqual(comendb,None)

    def testCreateLikes(self):
        user2=UserFactory()
        like=LikeFactory(post=self.post, user=user2)
        like_db=Like.objects.filter(id=like.id).first()
        self.assertEqual(like_db,like)
        like_db.delete()
        like_db=Like.objects.filter(id=like.id).first()
        self.assertEqual(like_db,None)
    
    def testShowPostbyTeam(self):
        usersinteam1=User.objects.filter(team=self.teams[0]).values_list('id',flat=True)
        self.assertEqual(usersinteam1.count(),3)
        postinteam1=Post.objects.filter(author__team=self.teams[0])
        self.assertEqual(postinteam1.count(),4)

    def testShowPostUser(self):
        self.assertEqual(Post.objects.filter(author=self.usersteam1[0]).count(),3)

    def testShowAllPost(self):
        self.assertEqual(Post.objects.all().count(),11)

    def testshowCommentsPost(self):
        self.assertEqual(Comment.objects.filter(post=self.postuser1team1[0]).count(),4)

    def testShowCommentsUser(self):
        self.assertEqual(Comment.objects.filter(user=self.usersteam1[0]).count(),1)
        self.assertEqual(Comment.objects.filter(user=self.usersteam1[1]).count(),1)
        self.assertEqual(Comment.objects.filter(user=self.usersteam2[0]).count(),2)

    def testShowLikePost(self):
        self.assertEqual(Like.objects.filter(post=self.postuser1team1[0]).count(),3)
    
    def testLikeExists(self):
        self.assertEqual(self.postuser1team1[0].like_exists(self.usersteam1[0].id),True)
        self.assertEqual(self.postuser1team1[0].like_exists(self.usersteam1[1].id),True)
        self.assertEqual(self.postuser1team1[0].like_exists(self.usersteam2[0].id),True)
        self.assertEqual(self.postuser1team1[0].like_exists(self.usersteam3.id),False)
        self.assertEqual(self.postuser1team1[0].like_exists(self.usersteam1[2].id),False)

    def testUniqueLikeperUser(self):
        with self.assertRaises(IntegrityError):
            LikeFactory(post=self.postuser1team1[0], user=self.usersteam1[0])



    def testDeletePostCommentLikes(self):
        postdb=Post.objects.filter(id=self.postuser1team1[0].id).first()
        idpost=postdb.id
        postdb.delete()
        self.assertEqual(Comment.objects.filter(post__id=idpost).count(),0)
        self.assertEqual(Like.objects.filter(post__id=idpost).count(),0)

    def testExceptp(self):
        self.assertEqual(self.post.exceptp,self.post.content[:200])
        

