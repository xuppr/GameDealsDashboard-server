import json
from django.http import response
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
        

    # login required

    def test_deals_with_start_0(self):

        response = self.query(
            '''
                {
                    deals(start: 0) {
                        dealsList {
                            title
                            storeID
                            salePrice
                            normalPrice
                            thumb
                            dealID
                            savings
                            steamRatingText
                            releaseDate
                            dealRating
                        }
                        isEnd
                    }
                }
            '''
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)

        self.assertIn('data', content)
        self.assertIn('deals', content['data'])
        self.assertIn('dealsList', content['data']['deals'])
        self.assertIn('isEnd', content['data']['deals'])

        deals = content['data']['deals']['dealsList']

        self.assertLessEqual(len(deals), 8)

        isEnd = content['data']['deals']['isEnd']
        self.assertFalse(isEnd)

    def test_deals_with_start_7(self):
        response = self.query(
            '''
                {
                    deals(start: 8) {
                        dealsList {
                            title
                            storeID
                            salePrice
                            normalPrice
                            thumb
                            dealID
                            savings
                            steamRatingText
                            releaseDate
                            dealRating
                        }
                        isEnd
                    }
                }
            '''
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)

        self.assertIn('data', content)
        self.assertIn('deals', content['data'])
        self.assertIn('dealsList', content['data']['deals'])
        self.assertIn('isEnd', content['data']['deals'])

        deals = content['data']['deals']['dealsList']

        self.assertLessEqual(len(deals), 8)

        isEnd = content['data']['deals']['isEnd']
        self.assertTrue(isEnd)

    def test_deals_with_start_out_of_bound(self):
        response = self.query(
            '''
                {
                    deals(start: 17) {
                        dealsList {
                            title
                            storeID
                            salePrice
                            normalPrice
                            thumb
                            dealID
                            savings
                            steamRatingText
                            releaseDate
                            dealRating
                        }
                        isEnd
                    }
                }
            '''
        )

        self.assertResponseHasErrors(response)

    def test_deals_filtered_by_store(self):
        response = self.query(
            '''
                {
                    dealsFilteredByStore(start: 0, storeID: "7"){
                        dealsList {
                            title
                            storeID
                            salePrice
                            normalPrice
                            thumb
                            dealID
                            savings
                            steamRatingText
                            releaseDate
                            dealRating
                        }
                        isEnd
                    }
                }
            '''
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)

        self.assertIn('data', content)
        self.assertIn('dealsFilteredByStore', content['data'])
        self.assertIn('dealsList', content['data']['dealsFilteredByStore'])
        self.assertIn('isEnd', content['data']['dealsFilteredByStore'])

        deals = content['data']['dealsFilteredByStore']['dealsList']

        self.assertLessEqual(len(deals), 8)

        isEnd = content['data']['dealsFilteredByStore']['isEnd']
        self.assertTrue(isEnd)

        for deal in deals:
            self.assertEqual(deal['storeID'], '7')

    def test_deals_filtered_by_store_with_invalid_store_id(self):
        response = self.query(
            '''
                {
                    deals_filtered_by_store(start: 0, storeID: "5"){
                        dealsList {
                            title
                            storeID
                            salePrice
                            normalPrice
                            thumb
                            dealID
                            savings
                            steamRatingText
                            releaseDate
                            dealRating
                        }
                        isEnd
                    }
                }
            '''
        )

        self.assertResponseHasErrors(response)

    def test_deals_filtered_by_price_range(self):
        pass

    def test_deals_sorted_by_price(self):
        pass

    def test_deals_sorted_by_savings(self):
        pass

    def test_deals_sorted_by_deal_rating(self):
        pass
    

