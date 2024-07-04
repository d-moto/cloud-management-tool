
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
