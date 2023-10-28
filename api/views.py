from django.shortcuts import render
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from complaints.models import Complain, ComplainOutcome
from rest_framework.generics import ListCreateAPIView
from .serializers import ComplainSerializer, ComplainOutcomeSerializer, UpdateStatusSerializer, LoginSerializer ,ChangePasswordSerializer, ComplainOutcomeCreateSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTechnicianUser
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser

User = get_user_model()


class UserLogin(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.role != 'technician':
            return Response({'error': 'You do not have permission to log in.'}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(password):
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class ChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplainViewSet(viewsets.ModelViewSet):
    queryset = Complain.objects.all()
    serializer_class = ComplainSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {
        "status": ["exact"]
    }
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["id", "status"]

    @action(detail=True, methods=['post'], serializer_class=UpdateStatusSerializer)
    def update_status(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateStatusSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], serializer_class=UpdateStatusSerializer)
    def partial_update_status(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateStatusSerializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        if IsTechnicianUser().has_permission(self.request, self):
            return Complain.objects.filter(technician__user=user)
        else:
            return Complain.objects.all()


class ComplainOutcomeByCustomerID(ListCreateAPIView):
    queryset = ComplainOutcome.objects.all()
    serializer_class = ComplainOutcomeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Assuming the URL parameter is named customer_id
        customer_id = self.kwargs['customer_id']
        return ComplainOutcome.objects.filter(complain__customer_id=customer_id)


class ComplainOutcomeByMchindID(ListCreateAPIView):
    queryset = ComplainOutcome.objects.all()
    serializer_class = ComplainOutcomeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Assuming the URL parameter is named mchind_id
        mchind_id = self.kwargs['mchind_id']
        return ComplainOutcome.objects.filter(complain__mchind_id=mchind_id)


class ComplainOutcomeViewSet(viewsets.ModelViewSet):
    queryset = ComplainOutcome.objects.all()
    serializer_class = ComplainOutcomeSerializer
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action == "create":
            return ComplainOutcomeCreateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.complain = Complain.Statuses.completed
        obj.save()