from django.db import models

# Create your models here.
class Deal(models.Model):
    title = models.CharField(max_length=255, null=True)
    dealID = models.CharField(max_length=255, null=True)
    storeID = models.CharField(max_length=5, null=True)
    salePrice = models.FloatField(null=True)
    normalPrice = models.FloatField(null=True)
    savings = models.FloatField(null=True)
    steamRatingText = models.CharField(max_length=30, null=True)
    releaseDate = models.BigIntegerField(null=True)
    dealRating = models.FloatField(null=True)
    thumb = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title