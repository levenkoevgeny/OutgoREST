from rest_framework import serializers
from .models import CustomUser, Subdivision, EmployeeKind, SheetItem, OutgoKind, OutgoData, Outgo


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class SubdivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdivision
        fields = '__all__'


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
        fields = ['id', 'date_time_created', 'kind', 'owner', 'subdivision', 'outgo_date', 'kind_data', 'subdivision_data']


class OutgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outgo
        fields = '__all__'
