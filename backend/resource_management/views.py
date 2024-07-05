from django.shortcuts import render

# Create your views here.

# resource_management/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer

from django.http import JsonResponse
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from django.conf import settings

import os
from dotenv import load_dotenv

load_dotenv()

# 環境変数からクレデンシャル情報を取得
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
tenant_id = os.getenv("AZURE_TENANT_ID")
subscription_id = "7fe7f7b1-5b14-4459-863d-26d92b90ccf2"
credentials = ClientSecretCredential(tenant_id, client_id, client_secret)

class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def get_azure_vms(request):
    credential = ClientSecretCredential(
        client_id=settings.AZURE_CLIENT_ID,
        client_secret=settings.AZURE_CLIENT_SECRET,
        tenant_id=settings.AZURE_TENANT_ID
    )

    compute_client = ComputeManagementClient(credential, settings.AZURE_SUBSCRIPTION_ID)
    vms = compute_client.virtual_machines.list_all()
    vm_list = [vm.as_dict() for vm in vms]
    
    return JsonResponse(vm_list, safe=False)


def fetch_azure_vms(request):
    compute_client = ComputeManagementClient(credentials, subscription_id)
    vm_list = []

    for vm in compute_client.virtual_machines.list_all():
        vm_info = {
            "name": vm.name,
            "location": vm.location,
            "resource_group": vm.id.split('/')[4],  # リソース グループを取得
            "type": vm.type,
            "vm_id": vm.vm_id
        }
        vm_list.append(vm_info)

    return JsonResponse(vm_list, safe=False)