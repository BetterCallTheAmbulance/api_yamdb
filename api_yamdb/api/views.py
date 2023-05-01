from rest_framework.decorators import api_view, action

from rest_framework import status, viewsets, filters, mixins

from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.response import Response

from .serializers import (UserSerializer, SignUpSerializer,
                          JWTTokenSerializer,  ResponseSerializer)

from .utils import generate_confirmation_code_and_send_email

from rest_framework.permissions import IsAuthenticated

from .permissions import (IsAdminOrReadOnlyPermission, OnlyAdmin)

from users.models import User


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnlyPermission,)


class GenreViewSet(CreateListDestroyViewSet):
    permission_classes = (IsAdminOrReadOnlyPermission,)


class CategoryViewSet(CreateListDestroyViewSet):
    permission_classes = (IsAdminOrReadOnlyPermission,)


@api_view(['POST'])
def signup_function(request):
    """Функция для регистрации нового пользователя"""

    data = request.data
    resp_ser = ResponseSerializer(data=data)
    resp_ser.is_valid(raise_exception=True)
    username = resp_ser.validated_data['username']
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        generate_confirmation_code_and_send_email(
            serializer.validated_data['username'],
            serializer.validated_data['email']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = get_object_or_404(User, username=username)
    serializer = SignUpSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['email'] == user.email:
        serializer.save()
        generate_confirmation_code_and_send_email(
            serializer.validated_data['username'],
            serializer.validated_data['email']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        'Вы неверно указали почту!',
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def token_function(request):
    """Функция для получения JWT-токена"""

    serializer = JWTTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    if (user.confirmation_code == serializer.validated_data['confirmation'
                                                            '_code']):
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        return Response({'token': access_token}, status=status.HTTP_200_OK)
    return Response(
        'Неверный код подтверждения!',
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения, обновления и удаления информации
    о пользователях"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (OnlyAdmin,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=username', )
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPostPatchDeleteViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
