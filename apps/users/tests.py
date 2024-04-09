from django.test import TestCase
from .models import Team,User

class UserTeamModelCreateTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(first_name='test name',last_name='last name test',
                                        email='test@test.com',birthdate='1992-05-25',
                                        username='testuser', password='testpassword')
        cls.team = Team.objects.create(team_name='Test Team')
        


    def testCreateUser(self):
        userdb=User.objects.filter(id=self.user.id).first()
        self.assertIsInstance(self.user, User)
        self.assertEqual(userdb.username,'testuser')
        self.assertEqual(userdb.email,'test@test.com')
        self.assertEqual(userdb.first_name,'test name')
        self.assertEqual(userdb.email,'test@test.com')
        self.assertEqual(userdb.birthdate.strftime('%Y-%m-%d'),'1992-05-25')
        self.assertEqual(userdb.check_password('testpassword'),True)
        
        self.assertEqual(userdb.is_admin,False)



    def testCreateTeam(self):
        teamdb=Team.objects.get(id=self.team.id)
        self.assertIsInstance(teamdb, Team)
        self.assertEqual(teamdb.team_name, 'Test Team')


    def testAssignUserToTeam(self):

        userdb = User.objects.get(id=self.user.id)
        userdb.team = self.team
        userdb.save()
        
   
        userdb2 = User.objects.get(id=self.user.id)
        self.assertEqual(userdb2.team, self.team)

    def testUserCreationWithTeam(self):

        team2 = Team.objects.create(team_name='Test Team2')
        
        # Crear un usuario y asignarlo al equipo
        user2 = User.objects.create_user(username='testuser2', email='test2@test.com',password='testpassword2', team=team2)
        user2db=User.objects.get(id=user2.id)
        # Verificar la asignación
        self.assertEqual(user2db.team, team2)
