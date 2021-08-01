import json
from django.http import response
from graphene_django.utils.testing import GraphQLTestCase
from ..models import Deal
from .deals_data import mock_data
from django.contrib.auth.models import User
from graphql_jwt.shortcuts import get_token

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

        cls.user = User.objects.create(username='mockuser', password="mockpassword")
    
    
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

    def test_deal_by_id(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    dealById(id: "IML08yuF8VjsQwlgfgjNDDjw9WCHBN%2FmFAGNhmhlWF4%3D") {
        
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
                }
            ''',
            headers=headers
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)

        self.assertIn('data', content)
        self.assertIn('dealById', content['data'])

        deal = content['data']['dealById']

        self.assertIn('title', deal)
        self.assertEqual(deal['title'], "The Office Quest")

    def test_deals_with_start_0(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

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
            ''',
            headers=headers
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

    def test_deals_with_start_8(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

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
            ''',
            headers=headers
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
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

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
            ''',
            headers=headers
        )

        self.assertResponseHasErrors(response)

    def test_deals_filtered_by_store(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    deals(start: 0, storeID: "7"){
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
            ''',
            headers=headers
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

        for deal in deals:
            self.assertEqual(deal['storeID'], '7')

    def test_deals_filtered_by_store_with_invalid_store_id(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    deals(start: 0, storeID: "5"){
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
            ''',
            headers=headers
        )

        content = json.loads(response.content)
        self.assertEqual(content['data']['deals']['dealsList'], [])

    def test_deals_filtered_by_price_range(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    deals(start: 0, lowPrice: 1.99, highPrice: 5.0){
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
            ''',
            headers=headers
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        deals = content['data']['deals']['dealsList']

        self.assertEqual(len(deals), 7)

        self.assertEqual(deals[0]['dealID'], "mU%2FbH6z0MsHtcyqBBnv1C29aei%2FU0ZcsW0tNaZjC3xQ%3D")
        self.assertEqual(deals[1]['dealID'], "dJNCeHkZV3iaXZQFBSpYh3B2tz6ZuMvBaFpI6d1QYiU%3D")
        self.assertEqual(deals[2]['dealID'], "%2BriI1%2B63K5PCBDSW7YcjfrFIhgc0u2sIkmRpwojt8l4%3D")
        self.assertEqual(deals[3]['dealID'], "rfnxxA9yFZZ%2BFfxDGsRqLQQubn17Q8NB0SHOChnsL%2BI%3D")
        self.assertEqual(deals[4]['dealID'], "tzAVXMgjTwh5hk442e%2FDLgK57c%2FSv4XhH%2B67K3Xvk4k%3D")
        self.assertEqual(deals[5]['dealID'], "ICV0L0NmwniVHpc4NjfQsDO5gRILOIkqPz05jfxFtCM%3D")
        self.assertEqual(deals[6]['dealID'], "eKcwMzD%2Bsr2BhW%2BcIb%2FTR1mcNf49dlln2q3p1n1igkw%3D")

    def test_deals_filtered_by_price_range_with_invalid_range(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    deals(start: 0, lowPrice: 5.99, highPrice: 1.0){
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
            ''',
            headers=headers
        )

        content = json.loads(response.content)
        self.assertEqual(content['data']['deals']['dealsList'], [])

    def test_deals_sorted_by_price(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    deals(start: 0, sortBy: "price"){
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
            ''',
            headers=headers
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        deals = content['data']['deals']['dealsList']

        self.assertLessEqual(len(deals), 8)

        last_price = deals[0]['salePrice']

        for deal in deals[1:]:
            price = deal['salePrice']
            self.assertGreaterEqual(price, last_price)
            last_price = price

    def test_deals_sorted_by_savings(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    deals(start: 0, sortBy: "savings"){
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
            ''',
            headers=headers
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        deals = content['data']['deals']['dealsList']

        self.assertLessEqual(len(deals), 8)

        last_savings = deals[0]['savings']

        for deal in deals[1:]:
            savings = deal['savings']
            self.assertLessEqual(savings, last_savings)
            last_savings = savings

    def test_deals_sorted_by_deal_rating(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    deals(start: 0, sortBy: "dealRating"){
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
            ''',
            headers=headers
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        deals = content['data']['deals']['dealsList']

        self.assertLessEqual(len(deals), 8)

        last_rating = deals[0]['dealRating']

        for deal in deals[1:]:
            rating = deal['dealRating']
            self.assertLessEqual(rating, last_rating)
            last_rating = rating

    def test_deals_filtered_by_store_price_range_and_sorted_by_deal_rating(self):
        token   = get_token(self.user)
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        response = self.query(
            '''
                {
                    deals(start: 0, lowPrice: 1.99, highPrice: 5.0, storeID: "1", sortBy: "dealRating"){
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
            ''',
            headers=headers
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        deals = content['data']['deals']['dealsList']

        last_rating = deals[0]['dealRating']

        for deal in deals[1:]:
            self.assertEqual(deal['storeID'], '1')

            price = deal['salePrice']
            self.assertLessEqual(price, 5.0)
            self.assertGreaterEqual(price, 1.99)

            rating = deal['dealRating']
            self.assertLessEqual(rating, last_rating)
            last_rating = rating


    

