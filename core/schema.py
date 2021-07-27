import graphene
from graphene.types import schema
import accounts.schema

class RootQuery(graphene.ObjectType):
  helloQuery = graphene.String(default_value='Hello Query!')

class RootMutation(accounts.schema.Mutation, graphene.ObjectType):
  helloMutation = graphene.String(default_value='Hello Mutation!')

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)