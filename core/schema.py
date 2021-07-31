import graphene
from graphene.types import schema
import accounts.schema, deals.schema
import graphql_jwt

class Query(deals.schema.Query, accounts.schema.Query, graphene.ObjectType):
  pass

class Mutation(accounts.schema.Mutation, graphene.ObjectType):
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)