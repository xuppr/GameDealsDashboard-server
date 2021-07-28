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


def to_full_deal_group(deals_list, start, deals_group_size):
    deals_count = len(deals_list)

    if start >= deals_count:
        raise Exception('Start index out of bound')

    end_index = start + deals_group_size

    is_end = False

    if end_index >= deals_count:
        is_end = True
        out_list = deals_list[start:]

    else:
        out_list = deals_list[start:end_index]

    return FullDealGroup(deals_list=out_list, is_end=is_end)



class Query(graphene.ObjectType):
    one_per_store = graphene.List(FreeDeal)
    deals = graphene.Field(FullDealGroup, start=graphene.Int())
    deals_filtered_by_store = graphene.Field(FullDealGroup, start=graphene.Int(), storeID=graphene.String())

    #debug
    # create_records = graphene.String()

    def resolve_one_per_store(root, info):
        steam_deal = Deal.objects.filter(storeID='1').first()
        gog_deal = Deal.objects.filter(storeID='7').first()
        humble_deal = Deal.objects.filter(storeID='11').first()

        return [steam_deal, gog_deal, humble_deal]

    def resolve_deals(root, info, start):
        deals_list = Deal.objects.all()
        return to_full_deal_group(deals_list, start, DEALS_PER_QUERY)

    def resolve_deals_filtered_by_store(root, info, start, storeID):

        if storeID not in ['1', '7', '11']:
            raise Exception('Invalid Store')
        
        deals_list = Deal.objects.filter(storeID=storeID)

        return to_full_deal_group(deals_list, start, DEALS_PER_QUERY)


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