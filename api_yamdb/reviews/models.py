from django.db import models


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
    )
    year = models.IntegerField(
        'Год выпуска',
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
