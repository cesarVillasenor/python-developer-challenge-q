from ..models import User, Address
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'addresses']
        depth = 1


class AddressSerializer(serializers.ModelSerializer):

    @staticmethod
    def clean(user_id, primary, address_id=None):
        addresses = Address.objects.filter(user_id=user_id)
        response = {}
        if address_id is None and addresses.count() >= 3:
            response["msg"] = 'User already has maximal amount of addresses (3)'
            response['validated'] = False
        elif not primary:
            all_primary = False
            if address_id is not None:
                addresses = Address.objects.filter(user_id=user_id).exclude(id=address_id)
            for address in addresses:
                if address.primary:
                    all_primary = True
                    break
            if not all_primary:
                if address_id is None:
                    response["msg"] = 'There Is Not A Primary Please Create A primary Address'
                else:
                    response["msg"] = 'Cannot Update You Should Have At Least One Primary Address'
                response['validated'] = False
            else:
                response['validated'] = True
        else:
            response['validated'] = True
        return response

    class Meta:
        model = Address
        fields = '__all__'

