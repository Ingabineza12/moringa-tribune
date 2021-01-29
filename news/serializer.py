from rest_framework import serializers
from .models import Article
# from .models import MoringaMerch

# if you do with Article model

# from .models import Article

# class MerchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MoringaMerch
#         fields = ('name', 'description', 'price')


# class MerchSerializer(serializers.ModelSerializer):
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','title', 'post', 'pub_date')
