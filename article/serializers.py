from rest_framework import serializers
from .models import Post, Rating
from rest_framework import serializers
from django.db.models import Avg
from .models import Post, Rating

class PostSerializer(serializers.ModelSerializer):
    ratings_count = serializers.IntegerField(source='ratings.count', read_only=True)
    average_score = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField() 

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'ratings_count', 'average_score', 'user_rating']

    def get_average_score(self, obj):
        average = obj.ratings.aggregate(Avg('score'))['score__avg']
        return average if average else 0

    def get_user_rating(self, obj):
        # Get the request user from the serializer context
        user = self.context.get('request').user
        if user.is_authenticated:
            # Try to get the user's rating for this post
            rating = obj.ratings.filter(user=user).first()
            if rating:
                return rating.score
        return None


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'post', 'user', 'score']
        read_only_fields = ['user']


    def validate_score(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("Score must be between 0 and 5.")
        return value