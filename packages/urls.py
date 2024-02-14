from django.views.generic import TemplateView
from django.urls import path
from .views import (
    PackagesListCreate,
    PackagesDetail,
    AmenitiesList,
    PlacesList,
    PlaceDetail,
    OldPackages,
    AmenityDetail,
    CompletePackageDetail
)

urlpatterns = [
    #path('home/',TemplateView.as_view(template_name='packages/index.html')),
    path('',PackagesListCreate.as_view(),name='new_packages'),
    path('detail/<int:pk>/',CompletePackageDetail.as_view(),name='complete_package'),
    path('<int:pk>/',PackagesDetail.as_view(),name='package_delete_update'),
    path('expried/',OldPackages.as_view(),name='old_packages'),
    path('<int:package>/amenities/',AmenitiesList.as_view(),name='package_amenities_listcreate'),
    path('<int:package>/amenities/<int:amenity_id>/', AmenityDetail.as_view(), name='amenity-detail'),
    path('<int:package>/places/',PlacesList.as_view(),name='package_places_list'),
    path('<int:package>/places/<int:place_id>/', PlaceDetail.as_view(), name='place-detail'),
]
