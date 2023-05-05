# Проект YaMDb
**Проект YaMDb собирает отзывы пользователей на произведения.**
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Как запустить проект:
**Клонировать репозиторий и перейти в него в командной строке:**
```
git clone ...
cd api_yamdb
```
**Cоздать и активировать виртуальное окружение:**
```
python3 -m venv env
source env/bin/activate
```
**Установить зависимости из файла requirements.txt:**
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
**Выполнить миграции:**
```
python3 manage.py migrate
```
**Запустить команду импорта данных в БД:**
```
python3 manage.py import_data
```
**Запустить проект:**
```
python3 manage.py runserver
```
## Примеры запросов API (ниже представлен не полный список возможных запросов, подробнее информация представлена в документации к API по ссылке http://127.0.0.1:8000/redoc/):
### Запрос на получение списка произведений (GET):
```
/api/v1/titles/
```
**Пример ответа:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```
### Запрос на добавление жанра (POST):
```
/api/v1/genres/
```
```
{
  "name": "string",
  "slug": "string"
}
```
**Пример ответа:**
```
{
  "name": "string",
  "slug": "string"
}
```
### Запрос на получение списка отзывов к произведению (GET):
```
/api/v1/titles/{title_id}/reviews/
```
**Пример ответа:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
### Запрос на добавление отзыва к произведению (POST):
```
/api/v1/titles/{title_id}/reviews/
```
**Пример ответа:**
```
{
  "text": "string",
  "score": 1
}
```
### Запрос на получение списка всех комментариев к отзыву (GET):
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
**Пример ответа:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
### Запрос на удаление комментария к отзыву (DELETE):
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
***Авторы:***
*[Платон Попов](https://github.com/BetterCallTheAmbulance)
*[Элина Мустафаева](https://github.com/Elllym-em)
*[Кирилл Бовин](https://github.com/Kirill-Bovin/)
