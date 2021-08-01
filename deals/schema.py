from django.db import models
from django.db.models import fields
import graphene
from graphql_jwt.decorators import login_required
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



class Query(graphene.AbstractType):
    one_per_store = graphene.List(FreeDeal)
    deal_by_id = graphene.Field(FullDeal, id = graphene.String())
    # deals = graphene.Field(FullDealGroup, start=graphene.Int())

    deals = graphene.Field(
        FullDealGroup, 
        start = graphene.Int(),
        storeID = graphene.String(),
        low_price = graphene.Float(),
        high_price = graphene.Float(),
        sort_by = graphene.String()
    )

    #debug
    # create_records = graphene.String()

    def resolve_one_per_store(root, info):
        steam_deal = Deal.objects.filter(storeID='1').first()
        gog_deal = Deal.objects.filter(storeID='7').first()
        humble_deal = Deal.objects.filter(storeID='11').first()

        return [steam_deal, gog_deal, humble_deal]

    @login_required
    def resolve_deal_by_id(root, info, id):
        deal = Deal.objects.get(dealID = id)

        return deal

    # @login_required
    # def resolve_deals(root, info, start):
    #     deals_list = Deal.objects.all()

    #     return to_full_deal_group(deals_list, start, DEALS_PER_QUERY)

    @login_required
    def resolve_deals(
        root, 
        info, 
        start, 
        storeID = 'default', 
        low_price = -1, 
        high_price = -1, 
        sort_by = 'default'):

        deals_list = Deal.objects.all()

        if storeID != 'default':
            deals_list = deals_list.filter(storeID = storeID)
        
        if high_price > -1:
            deals_list = deals_list.filter(salePrice__range=[low_price, high_price])

        if sort_by == 'price':
            deals_list = deals_list.order_by('salePrice')
        
        elif sort_by in ['savings', 'dealRating']:
            deals_list = deals_list.order_by('-' + sort_by)

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