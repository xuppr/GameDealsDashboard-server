from django.db import models
from django.db.models import fields
import graphene
from graphene_django import DjangoObjectType
from .models import Deal
#debug
from .tests.deals_data import mock_data

DEALS_PER_QUERY = 8

class FreeDeal(DjangoObjectType):
    class Meta:
        model = Deal
        fields = ("title", 'storeID', 'salePrice', 'normalPrice', 'thumb')

class FullDeal(DjangoObjectType):
    class Meta:
        model = Deal

class FullDealGroup(graphene.ObjectType):
    deals_list = graphene.List(FullDeal)
    is_end = graphene.Boolean(default_value=False)

class Query(graphene.ObjectType):
    one_per_store = graphene.List(FreeDeal)
    deals = graphene.Field(FullDealGroup, start=graphene.Int())

    #debug
    # create_records = graphene.String()

    def resolve_one_per_store(root, info):
        steam_deal = Deal.objects.filter(storeID='1').first()
        gog_deal = Deal.objects.filter(storeID='7').first()
        humble_deal = Deal.objects.filter(storeID='11').first()

        return [steam_deal, gog_deal, humble_deal]

    def resolve_deals(root, info, start):

        deals_count = Deal.objects.count()

        if start >= deals_count:
            raise Exception('Start index out of bound')
        
        end_index = start + DEALS_PER_QUERY
        
        is_end = False

        all_deals = Deal.objects.all()
        
        if end_index >= deals_count:
            is_end = True
            deals_list = all_deals[start:]

        else:
            deals_list = all_deals[start:end_index]

        return FullDealGroup(deals_list=deals_list, is_end=is_end)


    #debug
    # def resolve_create_records(root, info):
    #     deals = mock_data

    #     for deal in deals:
            
    #         Deal.objects.update_or_create(
    #             title = deal['title'],
    #             dealID = deal['dealID'],
    #             storeID = deal['storeID'],
    #             salePrice = deal['salePrice'],
    #             normalPrice = deal['normalPrice'],
    #             savings = deal['savings'],
    #             steamRatingText = deal['steamRatingText'],
    #             releaseDate = deal['releaseDate'],
    #             dealRating = deal['dealRating'],
    #             thumb = deal['thumb']
    #         )

    #     return 'Records created'