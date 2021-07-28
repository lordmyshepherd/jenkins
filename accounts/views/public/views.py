from rest_framework                import generics, exceptions, permissions
from rest_framework.authentication import BaseAuthentication
from accounts.models               import User
from accounts.serializers          import UserSerializer

FEE_PER_COUNT = 1

# api/public/accounts/1 header = 13020000

class PublicUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_key = request.META.get('HTTP_AUTHORIZATION')
        print(f"auth_key : {auth_key}")
        self.validate_auth_key(auth_key)

        unit, password = auth_key[:4], auth_key[4:]

        if unit == '0000':
            raise exceptions.AuthenticationFailed('NOT_PUBLIC_USER')

        try:
            user = User.objects.get(unit = unit, password = password)
            return (user, None)

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('USER_DOES_NOT_EXIST')

    def validate_auth_key(self, auth_key):
        if not auth_key or len(auth_key) != 8:
            raise exceptions.AuthenticationFailed('INVALID_AUTH_KEY')

        try:
            int(auth_key)
        except ValueError:
            raise exceptions.AuthenticationFailed('INVALID_CHARACTER_IN_AUTH_KEY')

class IsPublicUserReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS and
            request.user.is_superuser and
            request.user.is_authenticated
        )

class PublicUserDetailView(generics.RetrieveAPIView):
    authentication_classes = [PublicUserAuthentication, ]
    permission_classes     = [IsPublicUserReadOnly, ]
    queryset = User.objects.prefetch_related("doorlog_set")
    serializer_class = UserSerializer
