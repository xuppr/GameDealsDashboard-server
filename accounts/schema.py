from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    userCreationConfirm = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        if len(username) < 1 or len(password) < 1:
            raise Exception('username or password cannot be empty')

        try:
            # user = get_user_model()(
            #     username=username,
            # )
            # user.set_password(password)
            # user.save()
            # model = get_user_model()
            
            user = User.objects.create_user(username=username, password=password)
            user.save()

            return CreateUser(userCreationConfirm='User ' + username + ' created')

        except:
            raise Exception('user not created')

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.AbstractType):
    whoami = graphene.String()

    @login_required
    def resolve_whoami(root, info):
        return info.context.user.username