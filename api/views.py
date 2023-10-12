from django.shortcuts import render
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from complaints.models import Complain, ComplainOutcome
from .serializers import ComplainSerializer, ComplainFilter, ComplainOutcomeSerializer ,UpdateStatusSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, status


class ComplainViewSet(viewsets.ModelViewSet):
    queryset = Complain.objects.all()
    serializer_class = ComplainSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ComplainFilter

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
        serializer = UpdateStatusSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComplainOutcomeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ComplainOutcomeSerializer
    queryset = ComplainOutcome.objects.all()

# from rest_framework.decorators import api_view

# @api_view(['GET'])
# def get_complain_outcomes_by_customer_id(request, customer_id):
#     complain_outcomes = ComplainOutcome.objects.filter(complain__customer_id=customer_id)
#     serializer = ComplainOutcomeSerializer(complain_outcomes, many=True)
#     return Response(serializer.data)
