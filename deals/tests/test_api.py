import json
from graphene_django.utils.testing import GraphQLTestCase
from ..models import Deal
from .deals_data import mock_data

class DealsQueriesTest(GraphQLTestCase):

    @classmethod
    def setUpTestData(cls):

        deals = mock_data

        for deal in deals:
            
            Deal.objects.create(
                title = deal['title'],
                dealID = deal['dealID'],
                storeID = deal['storeID'],
                salePrice = deal['salePrice'],
                normalPrice = deal['normalPrice'],
                savings = deal['savings'],
                steamRatingText = deal['steamRatingText'],
                releaseDate = deal['releaseDate'],
                dealRating = deal['dealRating'],
                thumb = deal['thumb']
            )
    
    # login not required
    def test_one_per_store(self):

        query_node = 'onePerStore'

        response = self.query(
            '''
                {
                    onePerStore {
                        title
                        storeID 
                        salePrice 
                        normalPrice
                        thumb
                    }
                }
            '''
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)

        self.assertIn('data', content)

        data = content['data']

        self.assertIn(query_node, data)
        self.assertLess(len(data[query_node]), 4)

        deals = data[query_node]
        
        self.assertEqual(deals[0]['title'], "Tumblestone")
        self.assertEqual(deals[1]['title'], "Freedom Force")
        self.assertEqual(deals[2]['title'], "Deus Ex: Human Revolution - Director's Cut")
        

    
    

