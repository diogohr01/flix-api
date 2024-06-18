from movies.models import Movie
from rest_framework import serializers
from genres.models import Genre
from actors.models import Actor
from actors.serializers import ActorNameSerializer
from django.db.models import Avg


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    genre = serializers.PrimaryKeyRelatedField(
        queryset = Genre.objects.all()
    )
    release_date = serializers.DateField()
    actors = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
    )
    resume = serializers.CharField()
    
    
    
        
class MovieModelSerializer(serializers.ModelSerializer):
    actors = ActorNameSerializer(many=True)
    genre = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'title','rate','genre', 'release_date', 'actors', 'resume']
        
    

    def validate_release_date(self, value):
        if value.year < 1900:
            raise serializers.ValidationError('A data de lançamento não pode ser anterior a 1900.')
        return value

    def validate_resume(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('Resumo não deve ser maior do que 500 caracteres.')
        return value

    def get_genre(self, obj):
        return obj.genre.name if obj.genre else None
    
    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        if rate:
            return round(rate, 1)
        return None
        '''
        reviews = obj.reviews.all()
        if reviews:
            sum_reviews = 0
            for review in reviews:
                sum_reviews += review.stars
                reviews_count = reviews.count()
            return round(float(sum_reviews / reviews_count), 1)
        
        return None      
    '''


    