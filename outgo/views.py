from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from .models import CustomUser, Subdivision, EmployeeKind, SheetItem, OutgoKind, OutgoData, Outgo
from .serialisers import CustomUserSerializer, SubdivisionSerializer, EmployeeKindSerializer, SheetItemSerializer, \
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
    queryset = Subdivision.objects.all()
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
    queryset = OutgoData.objects.all()
    serializer_class = OutgoDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {'owner': ['exact'], 'outgo_date': ['lte', 'gte'],
                        }

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def save_full_outgo(self, request):
        serializer = OutgoDataSerializer(data=request.data)
        if serializer.is_valid():
            outgoData = serializer.save()
            for shItem in SheetItem.objects.all():
                for emlKind in EmployeeKind.objects.all():
                    new_outgo = Outgo(outgo=outgoData, sheet_item=shItem, employee_kind=emlKind)
                    new_outgo.save()

                    if 'item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_count' in request.data:
                        count = request.data['item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_count']
                        if count != '' and count != 0:
                            new_outgo.count = int(count) * shItem.sign
                            new_outgo.save()
                    if 'item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_description' in request.data:
                        description = request.data['item_' + str(shItem.id) + '_kind_' + str(emlKind.id) + '_description']
                        new_outgo.description = description
                        new_outgo.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OutgoViewSet(viewsets.ModelViewSet):
    queryset = Outgo.objects.all()
    serializer_class = OutgoSerializer

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
