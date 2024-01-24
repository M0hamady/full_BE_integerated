from datetime import date
from project.models import Step
from project.slck import send_slack_notification

def get_today_steps():
    today = date.today()
    steps = Step.objects.filter(start_date=today)
    message = "Today's Steps:\n\n"
    
    for step in steps:
        message += f"Step: {step.name}\n"
        message += f"Status: {step.status}\n"
        message += f"Floor: {step.floor.name}\n"
        message += f"Project: {step.floor.project.name}\n"
        message += f"Client: {step.floor.project.client.name}\n"
        message += f"Total Budget: {step.total_budget()}\n"
        message += "------------------------\n"

    return message

def send_steps_notification():
    steps = get_today_steps()
    
    for step in steps:
        floor = step.floor
        branch = floor.project.branch
        slack_channel = branch.slack

        send_slack_notification(slack_channel, steps)

send_slack_notification()