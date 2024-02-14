from django.shortcuts import render

# Create your views here.

def hello(request):
    return render(request,"askdjf")


from .models import User_Packages
from .serializers import UserPackageSerializer
from rest_framework import generics,permissions
from packages.models import Packages
from users.models import User
from rest_framework.response import Response
from users.permissions import IsAthunticated_Obj


class AddUserPackage(generics.CreateAPIView):
    #queryset = User_Packages.objects.all()
    serializer_class = UserPackageSerializer
    permission_classes = [IsAthunticated_Obj]#permissions.IsAuthenticated]

    def perform_create(self,serializer):
        package_id = self.kwargs['package']
        package = Packages.objects.filter(package_id=package_id).first()
        serializer.save(user=self.request.user,package=package)
        return Response(serializer.data)

#class UserPackageUpdate(generics.ListAPIView):