from django.core.management.base import BaseCommand
from ...models import Deal

def make_records(deals_data):
    
    for deal in deals_data:
            
        Deal.objects.update_or_create(
            dealID = deal['dealID'],
            defaults = {
                'title': deal['title'],
                'storeID': deal['storeID'],
                'salePrice': deal['salePrice'],
                'normalPrice': deal['normalPrice'],
                'savings': deal['savings'],
                'steamRatingText': deal['steamRatingText'],
                'releaseDate': deal['releaseDate'],
                'dealRating': deal['dealRating'],
                'thumb': deal['thumb']
            }
        )

API_ENDPOINT = 'https://www.cheapshark.com/api/1.0/deals?storeID=1,7,11&sortBy=recent&pageSize=16'

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('fetch deals command ok')