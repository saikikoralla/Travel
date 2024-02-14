from rest_framework import generics, viewsets, filters
from .models import Packages,Amenities,Places
from .serializers import PackagesSerializer,AmenitiesSerializer,PlacesSerializer,BasicDetailPackageSerializer,CompletePackagesSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import ReadOnly,IsAdminOrReadOnly,IsAdmin_Obj
from django.http import Http404
from datetime import datetime 



class PackagesListCreate(generics.ListCreateAPIView):
    """user read only Admin to read and write"""
    permission_classes = [IsAdminUser|ReadOnly]
    queryset=Packages.active_packages.all()
    serializer_class=BasicDetailPackageSerializer
    filter_backends=[filters.OrderingFilter,filters.SearchFilter]
    search_fields= ['^package_name','^description']
    ordering_fields=['start_date','end_date','package_name']
    ordering=['start_date']
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.users)

class CompletePackageDetail(generics.RetrieveAPIView):
    #permission_classes = [IsAdminUser|ReadOnly]
    queryset = Packages.objects.all()
    serializer_class =CompletePackagesSerializer
    lookup_kwargs=['package_id']

class PackagesDetail(generics.RetrieveUpdateDestroyAPIView):#PackageRetrieveUpdateDestroyAPIView
    permission_classes = [IsAdminUser|ReadOnly]
    queryset = Packages.objects.all()
    serializer_class =PackagesSerializer


class OldPackages(generics.ListAPIView):
    permission_classes=[IsAdminUser|ReadOnly]
    queryset = Packages.objects.filter(start_date__gt=datetime.now())
    serializer_class = PackagesSerializer


class AmenitiesList(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser|ReadOnly]
    #queryset=Amenities.objects.all()
    serializer_class=AmenitiesSerializer

    def get_queryset(self):
        package_id = self.kwargs['package']
        package = Packages.objects.filter(package_id=package_id).first()
        return Amenities.objects.filter(package=package)
    
    def perform_create(self, serializer):
        package_id = self.kwargs['package']
        package = Packages.objects.filter(package_id=package_id).first()
        serializer.save(package=package)


class AmenityDetail(generics.RetrieveUpdateDestroyAPIView):
    #API endpoint to manage amenities for a certain package.
    permission_classes=[IsAdminUser|ReadOnly]
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer
    lookup_url_kwarg = 'amenity_id'

    def get_queryset(self):
        #print(self.request.data,self.args,self.kwargs)
        package_id = self.kwargs['package']
        return Amenities.objects.filter(package=package_id)


class PlacesList(generics.ListCreateAPIView):
    permission_classes=[IsAdminOrReadOnly]
    #queryset=Amenities.objects.all()
    serializer_class=PlacesSerializer

    def get_queryset(self):
        package_id = self.kwargs['package']
        package = Packages.objects.filter(package_id=package_id).first()
        return Places.objects.filter(package=package)
    
    def perform_create(self, serializer):
        package_id = self.kwargs['package']
        package = Packages.objects.filter(package_id=package_id).first()
        serializer.save(package=package)


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint to manage places for a certain package."""
    permission_classes=[IsAdminUser]
    queryset = Places.objects.all()
    serializer_class = PlacesSerializer
    lookup_url_kwarg = 'place_id'

    def get_queryset(self):
        package_id = self.kwargs['package']
        return Places.objects.filter(package=package_id)