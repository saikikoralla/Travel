from rest_framework import serializers
from .models import Profile,User
from TripRecords.models import  User_Packages
from packages.serializers import PackagesSerializer,BasicDetailPackageSerializer
#from django.contrib.auth import authenticate
#from django.core.exceptions import ValidationError


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','phone_no','address','Img']

class RegisterSerializer(serializers.ModelSerializer):
    #confirm_password=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=('email','password')

    def create(self,clean_data):
        user_obj=User.objects.create_user(email=clean_data['email'],password=clean_data['password'])
        #user_obj.save()
        return user_obj
    
class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
    
	"""def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise serializers.ValidationError('User not found')
		return user
    """
class UserSerializer(serializers.ModelSerializer):
    #profile=ProfileSerializer(read_only=True)
    class Meta:
        model=User
        fields=['email',]


class ALLPackagesSerializer(serializers.ModelSerializer):
    email=serializers.SerializerMethodField()
    start_date=serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()
    class Meta:
        model = User_Packages
        fields = ['deal_id','email','package_name', 'no_of_persons', 'total_cost', 'date','start_date']
    
    def get_email(self, obj):
        return obj.user.email if obj.user else None
    
    def get_start_date(self, obj):
        return obj.package.start_date if obj.package else None
    def get_package_name(self, obj):
        return obj.package.package_name if obj.package else None
    

class UserPackagesSerializer(serializers.ModelSerializer):
    package_name = serializers.SerializerMethodField()
    start_date=serializers.SerializerMethodField()
    class Meta:
        model = User_Packages
        fields = ['deal_id','package_name','start_date', 'no_of_persons', 'total_cost', 'date','start_date']
        read_only_fields = ['total_cost','user','date','package'] 
    
    def get_start_date(self, obj):
        return obj.package.start_date if obj.package else None
    def get_package_name(self, obj):
        return obj.package.package_name if obj.package else None