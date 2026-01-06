import json
from django.shortcuts import render
from dashboardapp.models import *
from sqlalchemy import create_engine

# Create your views here.
engine = create_engine('postgresql+psycopg2://postgres:neha1626@127.0.0.1/Dashboard', pool_recycle=3600)


def HomePage(request):
    # Fetch all machines and their associated parameters efficiently
    # machines = Machine.objects.prefetch_related('parameters').all()
    mock_machines = [
        {
            'id': 1,
            'name': 'CNC Milling Alpha',
            'is_online': True,
            'status': 'Critical',
            # Alarm priority: 1: Critical (Red), 2: Warning (Orange), 3: Info (Blue)
            'highest_alarm_priority': 1, 
            'alarms': [
                {'msg': 'Spindle Overheat', 'priority': 'critical', 'time': '10:45 AM'},
                {'msg': 'Coolant Low', 'priority': 'warning', 'time': '10:30 AM'}
            ],
            'parameters': [
                {'label': 'Temp', 'value': '105', 'type': 'int', 'unit': '°C'},
                {'label': 'Load1', 'value': '92', 'type': 'int', 'unit': '%'},
                {'label': 'Load2', 'value': '90', 'type': 'int', 'unit': '%'},
                {'label': 'Load3', 'value': '82', 'type': 'int', 'unit': '%'},
                {'label': 'Load4', 'value': '98', 'type': 'int', 'unit': '%'},
            ]
        },
        {
            'id': 2,
            'name': 'Power Gen 04',
            'is_online': True,
            'status': 'Warning',
            'highest_alarm_priority': 2,
            'alarms': [
                {'msg': 'Fuel Filter Bypass', 'priority': 'warning', 'time': '09:15 AM'}
            ],
            'parameters': [
                {'label': 'Output', 'value': '440', 'type': 'int', 'unit': 'kW'},
                {'label': 'Fuel', 'value': '15', 'type': 'int', 'unit': '%'},
                {'label': 'Fuel', 'value': '10', 'type': 'int', 'unit': '%'},
                {'label': 'Fuel', 'value': '12', 'type': 'int', 'unit': '%'},
            ]
        },
        {
            'id': 3,
            'name': 'Hydraulic Press',
            'is_online': True,
            'status': 'Healthy',
            'highest_alarm_priority': 3,
            'alarms': [], # No active alarms
            'parameters': [
                {'label': 'Pressure', 'value': '120', 'type': 'int', 'unit': 'Bar'},
            ]
        }
    ]
    machines_json = json.dumps(mock_machines)
    print('the json converstion received is --- ',machines_json,len(machines_json))
    return render(request,'HomePage.html', {'machines': mock_machines,'machines_json': machines_json})

def machine_config(request, machine_id):
    # Logic to fetch specific machine details
    return render(request, 'machine_config.html', {'machine_id': machine_id})