from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import User, Address
from .serializers import UserSerializer, AddressSerializer
from django.http import Http404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PasswordResetView(APIView):

    def get(self, request,  user_id, format=None):
        """
        :param request:
            {
                "password": str
            }
        :param user_id: User Id
        :return: Response
        """
        address = User.objects.filter(id=user_id)
        serializer = UserSerializer(address, many=True)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        """
        :param request:
            {
                "password": "String"
            }
        :param user_id: User Id
        :return: Response
        """
        try:
            if 'password' not in request.data:
                return Response('Password Field Is Empty', status=status.HTTP_400_BAD_REQUEST)
            new_password = str(request.data['password'])
            user = User.objects.get(pk=user_id)
            user_serializer = UserSerializer(user, data={'password': new_password}, partial=True)
            if not user_serializer.is_valid():
                raise Exception(user_serializer.errors, status.HTTP_400_BAD_REQUEST)
            user_serializer.save()
            return Response('Password Updated Successfully', status=status.HTTP_200_OK)
        except Exception as inst:
            err, st = inst.args
            return Response(err, status=st)


class CreateAddressView(APIView):
    def get(self, request,  user_id, format=None):
        """
        :param request:
            {
                "address_id": int
                "postal_code" : int,
                "municipality" : "String",
                "state" : "String",
                "primary" : 1/0
            }
        :param user_id: User Id
        :return: Response
        """
        address = Address.objects.filter(user=user_id)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        """
        :param request:
            {
                "postal_code" : int,
                "municipality" : "String",
                "state" : "String",
                "primary" : 1/0
            }
        :param user_id: User Id
        :return: Response
        """
        try:
            data = request.data
            data["user"] = user_id
            address_serializer = AddressSerializer(data=request.data)
            if not address_serializer.is_valid():
                raise Exception(address_serializer.errors, status.HTTP_400_BAD_REQUEST)
            clean = address_serializer.clean(user_id, data["primary"])
            if not clean['validated']:
                return Response(clean["msg"], status=status.HTTP_400_BAD_REQUEST)
            address_serializer.save()
            return Response('Address Created Successfully', status=status.HTTP_201_CREATED)
        except Exception as inst:
            err, st = inst.args
            return Response(err, status=st)


class UpdatePrimaryAddressView(APIView):

    def get_object(self, pk):
        try:
            return Address.objects.get(id=pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, address_id, user_id, format=None):
        """
        :param request:
            {
                "address_id": int
                "postal_code" : int,
                "municipality" : "String",
                "state" : "String",
                "primary" : 1/0
            }
        :param user_id: User Id
        :param address_id: Address Id
        :return: Response
        """
        self.get_object(address_id)
        address = Address.objects.filter(id=address_id)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)

    def put(self, request, address_id, user_id,  format=None):
        """
        :param request:
            {
                "address_id": int
                "postal_code" : int,
                "municipality" : "String",
                "state" : "String",
                "primary" : 1/0
            }
        :param user_id: User Id
        :param address_id: Address Id
        :return: Response
        """
        try:
            self.get_object(address_id)
            data = request.data
            data["user"] = user_id
            data["id"] = address_id
            address = self.get_object(address_id)
            address_serializer = AddressSerializer(address, data=request.data)
            if not address_serializer.is_valid():
                raise Exception(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            clean = address_serializer.clean(user_id, request.data["primary"], address_id)
            if not clean['validated']:
                return Response(clean["msg"], status=status.HTTP_400_BAD_REQUEST)
            address_serializer.is_valid()
            address_serializer.save()
            return Response('Primary Address Updated Successfully', status=status.HTTP_201_CREATED)
        except Exception as inst:
            if type(inst) == Http404:
                return Response('Not Found', status=status.HTTP_400_BAD_REQUEST)
            err, st = inst.args
            return Response(err, status=st)

