import json
from django.http import response
from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class ApiTest(GraphQLTestCase):

  def test_user_creation_mutation(self):
    response = self.query(
            '''
            mutation {
                createUser(username: "fakeusername", password: "fakepassword") {
                    userCreationConfirm
                }
            }
            ''',
        )

    self.assertResponseNoErrors(response)

    content = json.loads(response.content)

    self.assertIn('userCreationConfirm', content['data']['createUser'])
    
    try:
      created_user = User.objects.get(username='fakeusername')
    except:
      self.fail('user not created')



  def test_user_creation_error_with_empty_username(self):
    response = self.query(
            '''
            mutation {
                createUser(username: "", password: "fakepassword") {
                    userCreationConfirm
                }
            }
            ''',
        )

    self.assertResponseHasErrors(response)
    self.assertEqual(len(User.objects.all()), 0)

  def test_user_creation_error_with_empty_password(self):
    response = self.query(
            '''
            mutation {
                createUser(username: "fakeusername", password: "") {
                    userCreationConfirm
                }
            }
            ''',
        )

    self.assertResponseHasErrors(response)
    self.assertEqual(len(User.objects.all()), 0)


  def test_user_creation_error_with_existing_username(self):

    response0 = self.query(
      '''
        mutation {
          createUser(username: "fakeusername", password: "fakepassword") {
            userCreationConfirm
          }
        }
      '''
    )

    self.assertResponseNoErrors(response0)

    response1 = self.query(
      '''
        mutation {
          createUser(username: "fakeusername", password: "fakepassword") {
            userCreationConfirm
          }
        }
      '''
    )

    self.assertResponseHasErrors(response1)

    # TODO check TransactionManagement error

    # usermodel = get_user_model()
    # self.assertEqual(len(usermodel.objects.all()), 1)



    