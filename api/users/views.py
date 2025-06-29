from .models import CustomUser
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import generics, permissions
from .permissions import IsAdmin
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        print(f'self.request.user.id: {self.request.user.id} role: {self.request.user.role} is_staff: {self.request.user.is_staff}')
        return CustomUser.objects.filter(id=self.request.user.id)
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        })