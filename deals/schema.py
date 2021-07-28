from django.db import models
from django.db.models import fields
import graphene
from graphene_django import DjangoObjectType
from .models import Deal

class FreeDeal(DjangoObjectType):
    class Meta:
        model = Deal
        fields = ("title", 'storeID', 'salePrice', 'normalPrice', 'thumb')

class FullDeal(DjangoObjectType):
    class Meta:
        model = Deal

class Query(graphene.ObjectType):
    one_per_store = graphene.List(FreeDeal)

    def resolve_one_per_store(root, info):
        steam_deal = Deal.objects.filter(storeID='1').first()
        gog_deal = Deal.objects.filter(storeID='7').first()
        humble_deal = Deal.objects.filter(storeID='11').first()

        return [steam_deal, gog_deal, humble_deal]
