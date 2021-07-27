import graphene
from graphene.types import schema
import accounts.schema
import graphql_jwt

class RootQuery(graphene.ObjectType):
  helloQuery = graphene.String(default_value='Hello Query!')

class RootMutation(accounts.schema.Mutation, graphene.ObjectType):
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)