from rest_framework import serializers
# from rest_framework.serializers import ModelSerializer
from blog_app.models import User , Blog
from general.models import Country , Address


from rest_framework import serializers
from blog_app.models import User
from general.models import Address, Country

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['line_1', 'line_2', 'city', 'state', 'postal_code', 'country']

class RegisterSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)  # Nested AddressSerializer to handle address data

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'bio', 'date_of_birth', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        user = User.objects.create_user(**validated_data)
        if address_data:
            Address.objects.create(**address_data)

        return user
    



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id' , 'continent', 'country' , 'country_code'] 


class UserSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_of_birth', 'bio', 'country' , 'address']

    def get_country(self,obj):
        request = self.context.get('request')
        if request and request.query_params.get('expand') == 'country':
            return CountrySerializer(obj.country).data if obj.country else None
        return obj.country_id
    
    def get_address(self, obj):
        request = self.context.get('request')
        if request and request.query_params.get('expand') == 'address':
            if obj.address:
                return {
                    "line_1": obj.address.line_1,
                    "line_2": obj.address.line_2,
                    "city": obj.address.city,
                    "state": obj.address.state,
                    "postal_code": obj.address.postal_code,
                    "country": obj.address.country.id if obj.address.country else None
                }
        return obj.address_id if obj.address else None
    


class BlogSerializer(serializers.ModelSerializer):
    # created_by = serializers.SerializerMethodField()
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )

    
    class Meta:
        model = Blog
        fields = ['id' , 'title' , 'content' , 'created_at', 'created_by']


    def get_created_by(self , obj):
        request = self.context.get('request')
        if request and request.query_params.get('expand') == 'created_by':
            return UserSerializer(obj.created_by,context=self.context).data
        return obj.created_by.id

    

