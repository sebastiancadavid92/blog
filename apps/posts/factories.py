import factory
from apps.users.models import User,Team
from .models import Post,Like,Comment


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    team_name = factory.sequence(lambda n: "Team #%s" % n)
    


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username =factory.sequence(lambda n: "Team #%s" % n)
    email = factory.Faker('email')
    first_name=factory.Faker('name')
    is_admin=False

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title=factory.Faker('sentence', nb_words=4)
    author=factory.SubFactory(UserFactory)
    content= factory.Faker('text')




class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Like


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
           
    content=factory.Faker('text')