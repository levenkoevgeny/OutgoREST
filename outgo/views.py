from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from .models import CustomUser, Subdivision, EmployeeKind, SheetItem, OutgoKind, OutgoData, Outgo
from .serializers import CustomUserSerializer, SubdivisionSerializer, EmployeeKindSerializer, SheetItemSerializer, \
    OutgoKindSerializer, OutgoDataSerializer, OutgoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action

from jose import jwt
from django.conf import settings
from django.db import transaction


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubdivisionViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff:
            return Subdivision.objects.all()
        else:
            return Subdivision.objects.filter(user=current_user)
    serializer_class = SubdivisionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {'user': ['exact'],
                        }

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeKindViewSet(viewsets.ModelViewSet):
    queryset = EmployeeKind.objects.all()
    serializer_class = EmployeeKindSerializer

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SheetItemViewSet(viewsets.ModelViewSet):
    queryset = SheetItem.objects.all()
    serializer_class = SheetItemSerializer

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OutgoKindViewSet(viewsets.ModelViewSet):
    queryset = OutgoKind.objects.all()
    serializer_class = OutgoKindSerializer

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OutgoDataViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff:
            return OutgoData.objects.all()
        else:
            return OutgoData.objects.filter(subdivision__user=current_user)

    serializer_class = OutgoDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {'subdivision': ['exact'], 'kind': ['exact'], 'outgo_date': ['lte', 'gte', 'exact'],
                        }

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def save_full_outgo(self, request):
        serializer = OutgoDataSerializer(data=request.data)
        if serializer.is_valid():
            outgo_data = serializer.save()
            for shItem in SheetItem.objects.all():
                for emlKind in EmployeeKind.objects.all():
                    new_outgo = Outgo(outgo=outgo_data, sheet_item=shItem, employee_kind=emlKind)
                    new_outgo.save()
                    if 'item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_count' in request.data:
                        count = request.data['item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_count']
                        if count != '' and count != 0:
                            new_outgo.count = int(count)
                            new_outgo.save()
                    if 'item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_description' in request.data:
                        description = request.data[
                            'item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_description']
                        new_outgo.description = description
                        new_outgo.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    @transaction.atomic
    def update_full_outgo(self, request, pk=None):
        outgo_data = self.get_object()
        serializer = OutgoDataSerializer(data=request.data)
        if serializer.is_valid():
            outgo_data.subdivision = serializer.validated_data['subdivision']
            outgo_data.kind = serializer.validated_data['kind']
            outgo_data.outgo_date = serializer.validated_data['outgo_date']
            outgo_data.save()
            for shItem in SheetItem.objects.all():
                for emlKind in EmployeeKind.objects.all():
                    qs = Outgo.objects.filter(outgo=outgo_data, sheet_item=shItem, employee_kind=emlKind)
                    if qs.exists():
                        outgo = qs.first()
                        if 'item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_count' in request.data:
                            count = request.data['item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_count']
                            if count != '':
                                outgo.count = int(count)
                                outgo.save()
                        if 'item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_description' in request.data:
                            description = request.data[
                                'item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_description']
                            outgo.description = description
                            outgo.save()
                    else:
                        pass
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    @transaction.atomic
    def make_full_clone(self, request, pk=None):
        outgo_data = self.get_object()
        copy_outgo_data = OutgoData(kind=outgo_data.kind, owner=outgo_data.owner, subdivision=outgo_data.subdivision,
                                    outgo_date=outgo_data.outgo_date)
        copy_outgo_data.save()
        for item in Outgo.objects.filter(outgo=outgo_data):
            Outgo.objects.create(outgo=copy_outgo_data, sheet_item=item.sheet_item, employee_kind=item.employee_kind,
                                 count=item.count, description=item.description)
        return Response(OutgoDataSerializer(copy_outgo_data).data, status=status.HTTP_201_CREATED)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OutgoViewSet(viewsets.ModelViewSet):
    queryset = Outgo.objects.all()
    serializer_class = OutgoSerializer
    filterset_fields = {'outgo': ['exact', 'in']
                        }

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
    except jwt.JWTError:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user_data = CustomUser.objects.get(pk=payload['user_id'])
        serializer = CustomUserSerializer(user_data)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
