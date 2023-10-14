from django.shortcuts import render
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from complaints.models import Complain, ComplainOutcome
from rest_framework.generics import ListCreateAPIView
from .serializers import ComplainSerializer, ComplainOutcomeSerializer, UpdateStatusSerializer,ComplainOutcomeCreateSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import  IsAuthenticated

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

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateStatusSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def partial_update_status(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateStatusSerializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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