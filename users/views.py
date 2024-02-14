from rest_framework.views import APIView
from .models import Profile,User
from TripRecords.models import User_Packages 
from django.contrib.auth import get_user_model,login,logout
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from .serializers import (RegisterSerializer,
                          LoginSerializer,
                          ProfileSerializer,
                          UserPackagesSerializer,
                          #UserPackageSerializer,
                          ALLPackagesSerializer)
from .validations import custom_validation,validate_email,validate_password
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from packages.models import Packages
from django.contrib.auth import authenticate
from .permissions import IsAthunticated_Obj
from rest_framework.parsers import MultiPartParser, FormParser
from .jwt_token import GenerateUserTokens


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class=RegisterSerializer
    def post(self,request):
        clean_data=custom_validation(request.data)
        clean_data=request.data
        print(clean_data)
        serializer= RegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.create(clean_data)
            if user:
                return Response({'messeage':'USER is created'},status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    """Login view for both admin and user"""
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        
        assert validate_email(data)
        assert validate_password(data)
        
        serializer = LoginSerializer(data=data)
        print(data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = authenticate(username=data['email'], password=data['password'])
                if user:
                    login(user)
                    if user.is_superuser and kwargs.get('type') == 'admin':
                        
                        token = GenerateUserTokens().generate_user_tokens(user)
                        return Response(
                            {
                                'message': 'Admin logged in',
                                'token': token
                            }, status=status.HTTP_200_OK)
                    elif not user.is_superuser and kwargs.get('type') == 'user':
                        token = GenerateUserTokens().generate_user_tokens(user)
                        return Response(
                            {
                                'message': 'User logged in',
                                'token': token
                            }, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': "You are not allowed"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdateView(APIView):
    permissions_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]
    parser_classes=[MultiPartParser,FormParser]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        profile = request.user.profile_obj
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        profile = request.user.profile_obj
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddUserPackage(generics.CreateAPIView):
    #queryset = User_Packages.objects.all()
    serializer_class = UserPackagesSerializer
    permission_classes = [IsAthunticated_Obj]

    def perform_create(self,serializer):
        package_id = self.kwargs['package']
        package = Packages.objects.filter(package_id=package_id).first()
        serializer.save(user=self.request.user,package=package)
        return Response(serializer.data)



class UserPackagesList(generics.ListAPIView):
    """purchased list by user"""
    permission_classes = [IsAthunticated_Obj]
    serializer_class = UserPackagesSerializer

    def get_queryset(self):
        return self.request.user.deals.all()

class UserPackageDestroy(generics.DestroyAPIView):
    permission_class=[IsAthunticated_Obj]
    serializer_class=UserPackagesSerializer
    lookup_kwargs=['deal_id']
    def get_queryset(self):
        return self.request.user.deals.all()

    #def destroy(self, request, *args, **kwargs):
    #    instance = 
    #   self.perform_destroy(instance)
    #    return Response(status=status.HTTP_204_NO_CONTENT)


class UserPackageViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    permission_classes = (IsAthunticated_Obj,)
    filter_backends=[filters.SearchFilter]
    search_fields=['^package_name']
    

    def get_queryset(self):
        return self.request.user.deals.all()
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = UserPackagesSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self, request,pk=None):
        queryset = User_Packages.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserPackagesSerializer(user)
        return Response(serializer.data)
    

class AllUserPackageViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users. ADMIN
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = User_Packages.objects.all()
    serializer_class=ALLPackagesSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['^package_name']
    
    def list(self,request):    
        queryset = User_Packages.objects.all()  # Adjusted to use local variable
        serializer = ALLPackagesSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request,pk=None):
        #queryset = User_Packages.objects.all()
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = ALLPackagesSerializer(user)
        return Response(serializer.data)
         
         
    

        
    