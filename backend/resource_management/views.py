from django.shortcuts import render

# Create your views here.

# resource_management/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer

class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
