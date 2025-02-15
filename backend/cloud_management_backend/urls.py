"""cloud_management_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

# cloud_management_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from resource_management.views import VirtualMachineViewSet, get_azure_vms
from resource_management.views import fetch_azure_vms

router = DefaultRouter()
router.register(r'vms', VirtualMachineViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/azure_vms/', get_azure_vms, name='get_azure_vms'),
    # path('api/aws_vms/', get_aws_vms, name='get_aws_vms'),
    path('api/fetch_azure_vms/', fetch_azure_vms, name='fetch_azure_vms'),
]

