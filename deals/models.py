from django.db import models

# Create your models here.
class Deal(models.Model):
    title = models.CharField(max_length=255, null=True)
    dealID = models.CharField(max_length=255, null=True)
    storeID = models.CharField(max_length=5, null=True)
    salePrice = models.CharField(max_length=255, null=True)
    normalPrice = models.CharField(max_length=255, null=True)
    savings = models.CharField(max_length=25, null=True)
    steamRatingText = models.CharField(max_length=30, null=True)
    releaseDate = models.BigIntegerField(null=True)
    dealRating = models.CharField(max_length=5, null=True)
    thumb = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title