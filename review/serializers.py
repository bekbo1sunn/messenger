from rest_framework.serializers import ModelSerializer
from .models import Comment, Favorite, Rating


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user',)

    def validate(self, attrs):
        super().validate(attrs)
        attrs["user"] = self.context["request"].user
        return attrs
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = { 
            "id": instance.user.id,
            "email": instance.user.email
            }
        return rep 


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        exclude = ('user',)

    def validate(self, attrs):
        super().validate(attrs)
        attrs["user"] = self.context["request"].user
        return attrs
    
    def to_representation(self, instance):
        from post.serializers import PostSerializer

        rep = super().to_representation(instance)
        rep['post'] = PostSerializer(instance.post).data
        return rep
        

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        exclude = ('user',)

    def validate(self, attrs):
        super().validate(attrs)
        attrs["user"] = self.context["request"].user
        return attrs
    
    def create(self, validated_data):
        value = validated_data.pop("value")
        obj, created = Rating.objects.update_or_create(**validated_data, defaults={"value":value})
        return obj