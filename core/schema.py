import graphene
from graphene.types import schema

class RootQuery(graphene.ObjectType):
  helloQuery = graphene.String(default_value='Hello Query!')

class RootMutation(graphene.ObjectType):
  helloMutation = graphene.String(default_value='Hello Mutation!')

schema = graphene.Schema(query=RootQuery, mutation=RootMutation)