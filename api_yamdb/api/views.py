from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitleListSerializer, TitleCreateSerializer
from .filters import TitleFilter


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('name', 'year',)

    def get_queryset(self):
        return Title.objects.all().annotate(
            rating=Avg('reviews__score')
        )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleCreateSerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
