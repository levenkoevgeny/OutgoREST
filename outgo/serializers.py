from rest_framework import serializers
from .models import CustomUser, Subdivision, EmployeeKind, SheetItem, OutgoKind, OutgoData, Outgo


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username',
                  'password',
                  'is_staff',
                  'first_name',
                  'last_name',
                  'is_active',
                  'date_joined',
                  'last_login',
                  ]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class SubdivisionSerializer(serializers.ModelSerializer):
    user_data = CustomUserSerializer(read_only=True, source='user')
    class Meta:
        model = Subdivision
        fields = ['id', 'subdivision_name', 'subdivision_short_name', 'user', 'user_data']


class EmployeeKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeKind
        fields = '__all__'


class SheetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetItem
        fields = '__all__'


class OutgoKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutgoKind
        fields = '__all__'


class OutgoDataSerializer(serializers.ModelSerializer):
    kind_data = OutgoKindSerializer(read_only=True, source='kind')
    subdivision_data = SubdivisionSerializer(read_only=True, source='subdivision')

    class Meta:
        model = OutgoData
        fields = ['id', 'date_time_created', 'kind', 'owner', 'subdivision', 'outgo_date', 'kind_data',
                  'subdivision_data']


class OutgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outgo
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)


class UserNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']
