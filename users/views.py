from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsUserOwner, IsSuperuserOrStaff
from users.serializers import UserSerializer, UserLimitedSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOwner, IsAuthenticated)


class UserListAPIView(ListAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.permission_classes == (IsSuperuserOrStaff,):
            return UserSerializer
        return UserLimitedSerializer


class UserCreateAPIView(CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
