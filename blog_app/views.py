from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from blog_app.models import User , Blog
from general.models import Country
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .serializer import RegisterSerializer , CountrySerializer , UserSerializer , BlogSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status



class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self , request , *args , **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({
                'status' : 'success',
                'message' : 'User created successfully',
                'data': {
                    'id'  : user.id,
                    'username' : user.username
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status' : 'error',
            'message' : 'User creation failed',
            'errors' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country", "date_of_birth"]
    permission_classes = [IsAuthenticated]   

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status' : 'success',
                'message' : 'User created successfully',
                'data' : {
                    'id' : user.id,
                    'username' : user.username
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'error',
            'message' : 'User creation failed',
            'errors' : serializer.errors
        },status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial',False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,data = request.data , partial = partial)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'status': 'success',
                'message': 'User updated successfully.',
                'data': {
                    'id': user.id,
                    'username': user.username
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'User update failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'User deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)



class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["continent", "country"]
    permission_classes = [AllowAny]



class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["created_by", "created_at"]
    permission_classes = [IsAuthenticated] 
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class LogoutView(APIView):
    def post(self,request):
        token = RefreshToken(request.data["refresh"])
        token.blacklist()
        return Response({"message" : "Logged out successfully"})