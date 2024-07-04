
# Cloud Management Tool

This is a cloud management tool built with Django for the backend and PyQt5 for the frontend.

## Installation

### Backend

1. **Navigate to the `backend` directory**:
   ```bash
   cd backend
   ```
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

### Frontend

1. **Navigate to the `frontend` directory**:
   ```bash
   cd frontend
   ```
2. **Run the PyQt5 application**:
   ```bash
   python main.py
   ```

## Usage

- Use the frontend application to create and fetch virtual machines.

### Creating a Virtual Machine
1. Enter the VM details (Name, Provider, Status) in the GUI.
2. Click "Create VM" to create a new virtual machine.

### Fetching Virtual Machines
1. Click "Fetch VMs" to retrieve the list of virtual machines from the backend.
2. The list of VMs will be displayed in the GUI.

## API Reference

- `GET /api/vms/`: Fetch all virtual machines.
- `POST /api/vms/`: Create a new virtual machine.

## Troubleshooting

### Qt platform plugin "windows" issue

If you encounter an issue with the Qt platform plugin "windows", ensure that the environment variables are set correctly in `main.py`:

```python
import os
import sys

# PyQt5のパスを設定
pyqt5_path = r'G:\マイドライブ\python\venv\cloud-tool-env39\Lib\site-packages\PyQt5'
qt_plugin_path = os.path.join(pyqt5_path, 'Qt5', 'plugins')
os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(qt_plugin_path, 'platforms')

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFormLayout, QListWidget
import requests

def fetch_vms():
    try:
        response = requests.get('http://localhost:8000/api/vms/')
        response.raise_for_status()
        vms = response.json()
        vm_list.clear()
        for vm in vms:
            vm_list.addItem(f"Name: {vm['name']}, Provider: {vm['provider']}, Status: {vm['status']}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching VMs: {e}")

def create_vm():
    name = name_input.text()
    provider = provider_input.text()
    status = status_input.text()
    data = {
        "name": name,
        "provider": provider,
        "status": status,
    }
    try:
        response = requests.post('http://localhost:8000/api/vms/', json=data)
        response.raise_for_status()
        if response.status_code == 201:
            print("Virtual Machine created successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error creating VM: {e}")

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Cloud Management Tool")

layout = QVBoxLayout()

name_input = QLineEdit()
provider_input = QLineEdit()
status_input = QLineEdit()

form_layout = QFormLayout()
form_layout.addRow("Name", name_input)
form_layout.addRow("Provider", provider_input)
form_layout.addRow("Status", status_input)

layout.addLayout(form_layout)

create_button = QPushButton("Create VM")
create_button.clicked.connect(create_vm)
layout.addWidget(create_button)

fetch_button = QPushButton("Fetch VMs")
fetch_button.clicked.connect(fetch_vms)
layout.addWidget(fetch_button)

# 仮想マシンリスト表示の追加
vm_list = QListWidget()
layout.addWidget(vm_list)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
```

## License

[Your License Here]

## PostgreSQL Configuration

### Install PostgreSQL

If PostgreSQL is not already installed, you can download and install it from the [official PostgreSQL website](https://www.postgresql.org/download/).

### Create a Database and User

1. **Login to PostgreSQL**:
   ```bash
   psql -U postgres
   ```

2. **Create a new database**:
   ```sql
   CREATE DATABASE your_db_name;
   ```

3. **Create a new user**:
   ```sql
   CREATE USER your_db_user WITH PASSWORD 'your_db_password';
   ```

4. **Grant all privileges to the new user**:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
   ```

5. **Set up the database schema**:
   ```sql
   \c your_db_name
   GRANT ALL PRIVILEGES ON SCHEMA public TO your_db_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_db_user;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_db_user;
   ```

### Configure Django to Use PostgreSQL

1. **Update the `DATABASES` setting in `backend/cloud_management_backend/settings.py`**:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### Start PostgreSQL Service

Ensure that the PostgreSQL service is running. You can start it using the following command:

```bash
sudo service postgresql start
```

For Windows, use the following command in the Command Prompt:

```cmd
net start postgresql-x64-13
```


## Django Installation and Setup
### Install Django

1. Navigate to the `backend` directory:
```
cd backend
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install Django and other dependencies:
```
pip install Django djangorestframework psycopg2-binary boto3 azure-mgmt-resource
```

4. Create a Django project:
```
django-admin startproject cloud_management_backend
cd cloud_management_backend
```

5. Create a Django app:
```
python manage.py startapp resource_management
```

6. Update the settings file:
- Add resource_management and rest_framework to INSTALLED_APPS
- Configure the database settings for PostgreSQL
```
# settings.py
INSTALLED_APPS = [
    ...
    'resource_management',
    'rest_framework',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

7. Create models and run migrations:
```
# resource_management/models.py
from django.db import models

class VirtualMachine(models.Model):
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=50)  # 'AWS' or 'Azure'
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
```
```
python manage.py makemigrations
python manage.py migrate
```

8. Create serializers and views:
```
# resource_management/serializers.py
from rest_framework import serializers
from .models import VirtualMachine

class VirtualMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMachine
        fields = '__all__'
```
```
# resource_management/views.py
from rest_framework import viewsets
from .models import VirtualMachine
from .serializers import VirtualMachineSerializer

class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer
```

9. Update the URL configuration:
```
# cloud_management_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from resource_management.views import VirtualMachineViewSet

router = DefaultRouter()
router.register(r'vms', VirtualMachineViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
```

10. Start the Django development server:
```
python manage.py runserver
```

### Create a Superuser

To access the Django admin interface, create a superuser account.

```
cd backend
python manage.py createsuperuser
Username (leave blank to use 'mokos'): admin
Email address: mokosan123@outlook.jp
Password: admin00
Password (again): admin00
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```
