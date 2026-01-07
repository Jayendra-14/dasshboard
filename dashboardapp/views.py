from datetime import datetime,timedelta
import json
import random
from django.shortcuts import render
from dashboardapp.models import *
from sqlalchemy import create_engine

# Create your views here.
engine = create_engine('postgresql+psycopg2://postgres:neha1626@127.0.0.1/Dashboard', pool_recycle=3600)


def HomePage(request):
    # Fetch all machines and their associated parameters efficiently
    # machines = Machine.objects.prefetch_related('parameters').all()

    def generate_dynamic_machines(n):
        statuses = ['Stable', 'Warning', 'Critical']
        # Pool of possible parameters to draw from
        parameter_pool = [
            {'label': 'Temp', 'unit': '°C', 'type': 'int'},
            {'label': 'Load1', 'unit': '%', 'type': 'int'},
            {'label': 'Load2', 'unit': '%', 'type': 'int'},
            {'label': 'Pressure', 'unit': 'bar', 'type': 'float'},
            {'label': 'Vibration', 'unit': 'mm/s', 'type': 'float'},
            {'label': 'Flow Rate 1', 'unit': 'L/min', 'type': 'float'},
            {'label': 'Flow Rate 2', 'unit': 'L/min', 'type': 'float'},
            {'label': 'Flow Rate 3', 'unit': 'L/min', 'type': 'float'},
            {'label': 'Flow Rate 4', 'unit': 'L/min', 'type': 'float'},
            {'label': 'Flow Rate 5', 'unit': 'L/min', 'type': 'float'},
            {'label': 'Flow Rate 6', 'unit': 'L/min', 'type': 'float'},
            {'label': 'Flow Rate 7', 'unit': 'L/min', 'type': 'float'},
            {'label': 'Flow Rate 8', 'unit': 'L/min', 'type': 'float'},
            {'label': 'Flow Rate 9', 'unit': 'L/min', 'type': 'float'}
        ]
        
        alarm_pool = [
            {'msg': 'Spindle Overheat', 'priority': 'critical'},
            {'msg': 'Coolant Low', 'priority': 'warning'},
            {'msg': 'Emergency Stop Engaged', 'priority': 'critical'},
            {'msg': 'Sensor Communication Error', 'priority': 'info'},
            {'msg': 'Door Interlock Open', 'priority': 'warning'},
            {'msg': 'Voltage Fluctuation', 'priority': 'info'}
        ]
        
        dynamic_list = []
        
        for i in range(1, n + 1):
            current_status = random.choice(statuses)
            
            # Decide how many parameters this specific machine has (0 to 4)
            num_params = random.randint(0, 10)
            # Randomly select 'num_params' unique items from the pool
            selected_params = random.sample(parameter_pool, 11)
            
            # Build the actual parameter list with random values
            machine_parameters = []
            for p in selected_params:
                val = random.randint(20, 120) if p['type'] == 'int' else round(random.uniform(1.0, 50.0), 2)
                machine_parameters.append({
                    'label': p['label'],
                    'value': str(val),
                    'type': p['type'],
                    'unit': p['unit']
                })
            
            # --- DYNAMIC ALARMS ---
            # If 'Stable', usually 0 alarms. If 'Critical', 1-3 alarms.
            if current_status == 'Stable':
                num_alarms = random.randint(0, 1) # Sometimes a stable machine has an 'info' alarm
            else:
                num_alarms = random.randint(1, 3)
                
            selected_alarms = random.sample(alarm_pool, num_alarms)
            machine_alarms = []
            for a in selected_alarms:
                # Generate a random time within the last 2 hours
                random_minutes = random.randint(1, 120)
                timestamp = (datetime.now() - timedelta(minutes=random_minutes)).strftime('%I:%M %p')
                
                machine_alarms.append({
                    'msg': a['msg'],
                    'priority': a['priority'],
                    'time': timestamp
                })
            
            critical_count = sum(1 for a in selected_alarms if a['priority'] == 'critical')
            warning_count = sum(1 for a in selected_alarms if a['priority'] == 'warning')

            if critical_count > 0 or warning_count > 3:
                alarm_css_class = "alarm-critical"
            elif warning_count > 0:
                alarm_css_class = "alarm-warning"
            else:
                alarm_css_class = ""

            machine = {
                'id': i,
                'name': f'CNC-{random.randint(100, 999)}',
                'is_online': random.choice([True, False]),
                'status': current_status,
                'highest_alarm_priority': random.randint(1, 3),
                'alarms': machine_alarms,
                'alarm_css_class': alarm_css_class,
                'parameters': machine_parameters # This is now dynamic in length
            }
            dynamic_list.append(machine)
            
        return dynamic_list

    # Generate 100 machines to see the variety
    n_machines = 100
    
    
    mock_machines = generate_dynamic_machines(n_machines)
    
    # mock_machines = [
    #     {
    #         'id': 1,
    #         'name': 'CNC Milling Alpha',
    #         'is_online': True,
    #         'status': 'Critical',
    #         # Alarm priority: 1: Critical (Red), 2: Warning (Orange), 3: Info (Blue)
    #         'highest_alarm_priority': 1, 
    #         'alarms': [
    #             {'msg': 'Spindle Overheat', 'priority': 'critical', 'time': '10:45 AM'},
    #             {'msg': 'Coolant Low', 'priority': 'warning', 'time': '10:30 AM'},
    #             {'msg': 'Coolant Low', 'priority': 'warning', 'time': '10:30 AM'},
    #             {'msg': 'Coolant Low', 'priority': 'warning', 'time': '10:30 AM'}
    #         ],
    #         'parameters': [
    #             {'label': 'Temp', 'value': '105', 'type': 'int', 'unit': '°C'},
    #             {'label': 'Load1', 'value': '92', 'type': 'int', 'unit': '%'},
    #             {'label': 'Load2', 'value': '90', 'type': 'int', 'unit': '%'},
    #             {'label': 'Load3', 'value': '82', 'type': 'int', 'unit': '%'},
    #             {'label': 'Load4', 'value': '98', 'type': 'int', 'unit': '%'},
    #         ]
    #     },
    #     {
    #         'id': 2,
    #         'name': 'Power Gen 04',
    #         'is_online': True,
    #         'status': 'Warning',
    #         'highest_alarm_priority': 2,
    #         'alarms': [
    #             {'msg': 'Fuel Filter Bypass', 'priority': 'warning', 'time': '09:15 AM'}
    #         ],
    #         'parameters': [
    #             {'label': 'Output', 'value': '440', 'type': 'int', 'unit': 'kW'},
    #             {'label': 'Fuel', 'value': '15', 'type': 'int', 'unit': '%'},
    #             {'label': 'Fuel', 'value': '10', 'type': 'int', 'unit': '%'},
    #             {'label': 'Fuel', 'value': '12', 'type': 'int', 'unit': '%'},
    #         ]
    #     },
    #     {
    #         'id': 3,
    #         'name': 'Hydraulic Press',
    #         'is_online': True,
    #         'status': 'Healthy',
    #         'highest_alarm_priority': 3,
    #         'alarms': [], # No active alarms
    #         'parameters': [
    #             {'label': 'Pressure', 'value': '120', 'type': 'int', 'unit': 'Bar'},
    #         ]
    #     }
    # ]
    
    
    machines_json = json.dumps(mock_machines)
    print('the json converstion received is --- ',machines_json,len(machines_json))
    return render(request,'HomePage.html', {'machines': mock_machines,'machines_json': machines_json})

def machine_config(request, machine_id):
    # Logic to fetch specific machine details
    return render(request, 'machine_config.html', {'machine_id': machine_id})