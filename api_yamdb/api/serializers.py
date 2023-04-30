import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class TitleListSerializer(serializers.ModelSerializer):
    genre = CategorySerializer(
        read_only=True,
        many=True,
    )
    category = GenreSerializer(
        read_only=True,
    )
    rating = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        fields = [
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        ]
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value
