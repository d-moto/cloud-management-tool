import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFormLayout, QListWidget
import requests

# PyQt5のパスを設定
pyqt5_path = r'G:\マイドライブ\python\venv\cloud-tool-env39\Lib\site-packages\PyQt5'
qt_plugin_path = os.path.join(pyqt5_path, 'Qt5', 'plugins')
os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(qt_plugin_path, 'platforms')

# パスをプリントして確認
print("QT_PLUGIN_PATH:", os.environ['QT_PLUGIN_PATH'])
print("QT_QPA_PLATFORM_PLUGIN_PATH:", os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'])

def fetch_vms():
    try:
        response = requests.get('http://localhost:8000/api/vms/')
        response.raise_for_status()
        vms = response.json()
        vm_list.clear()
        for vm in vms:
            vm_list.addItem(f"Name: {vm['name']}, Provider: {vm['provider']}, Status: {vm.get('status', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching VMs: {e}")

def fetch_azure_vms():
    try:
        response = requests.get('http://localhost:8000/api/azure_vms/')
        response.raise_for_status()
        vms = response.json()
        vm_list.clear()
        for vm in vms:
            vm_list.addItem(f"Name: {vm['name']}, Provider: Azure, Status: {vm.get('status', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Azure VMs: {e}")

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

fetch_azure_button = QPushButton("Fetch Azure VMs")
fetch_azure_button.clicked.connect(fetch_azure_vms)
layout.addWidget(fetch_azure_button)

# 仮想マシンリスト表示の追加
vm_list = QListWidget()
layout.addWidget(vm_list)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
