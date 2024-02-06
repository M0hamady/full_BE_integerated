import os
import sys
import django

# Adjust the path to the Django project's settings.py accordingly
sys.path.append('/home/M0hamady/supportconstruction')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supportconstruction.settings')
django.setup()
from datetime import date
from client.models import Client
from project.slck import send_slack_notification

def get_all_clients_has_no_actions():
    today = date.today()
    clients = Client.objects.all()
    res = [client for client in clients if not client.has_action() and client.calculate_data_completion_percentage2() <=13]
    message = "Manager's Report - Customer Service Call List\n\n"
    message += f"Manager: Ahmed Qorashy\n"
    message += f"Company: Support Constructions\n"
    message += f"Date: {today.strftime('%B %d, %Y')}\n\n"
    print(res)
    for step in res:
        message += f"Client: {step.name}\n"
        message += f"Number: {step.number}\n"
        message += f"Location: {step.location}\n"
        message += "------------------------\n"

    return message

def send_steps_notification():
    message = get_all_clients_has_no_actions()
    send_slack_notification("#customer-service", message)

send_steps_notification()