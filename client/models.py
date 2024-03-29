from datetime import datetime 
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist

from twilio.rest import Client as tw_client

from project.models import Project
from project.slck import send_slack_notification

# from markting.models import Marketing
CITIES = (
    ('cairo', 'Cairo'),
    ('giza', 'Giza'),
    ('alexandria', 'Alexandria'),
    ('beheira', 'Beheira'),
    ('ismailia', 'Ismailia'),
    ('luxor', 'Luxor'),
    ('red_sea', 'Red Sea'),
    ('daqahliyah', 'Daqahliyah'),
    ('sharqiyah', 'Sharqiyah'),
    ('fayoum', 'Fayoum'),
    ('gharbiyah', 'Gharbiyah'),
    ('ismailia', 'Ismailia'),
    ('cairo', 'Cairo'),
    ('qalyubia', 'Qalyubia'),
    ('suez', 'Suez'),
    ('sharqiyah', 'Sharqiyah'),
    ('gharbiyah', 'Gharbiyah'),
    ('fayoum', 'Fayoum'),
    ('cairo', 'Cairo'),
    ('qalyubia', 'Qalyubia'),
    ('canal', 'Canal'),
    ('qena', 'Qena'),
    ('menofia', 'Menofia'),
    ('minya', 'Minya'),
    ('new_valley', 'New Valley'),
    ('assiut', 'Assiut'),
    ('aswan', 'Aswan'),
    ('beni_suef', 'Beni Suef'),
    ('port_said', 'Port Said'),
    ('south_sinai', 'South Sinai'),
    ('damietta', 'Damietta'),
    ('sohag', 'Sohag'),
    ('north_sinai', 'North Sinai'),
    ('qena', 'Qena'),
    ('kafr_el_sheikh', 'Kafr El Sheikh'),
    ('matrouh', 'Matrouh')
)
class Client(models.Model):
    SOCIAL_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram')
    ]
    LICENSE_METHOD_CHOICES = [
        ('mobile', 'Mobile Number'),
        ('email', 'Email'),
        ('phone_call', 'Phone Call')
    ]
    
    add_by = models.ForeignKey('markting.Marketing', on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=150)
    slack_channel_name = models.CharField(max_length=150,null=True)
    email = models.EmailField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    number = models.CharField(max_length=150, null=True, blank=True)
    location = models.CharField(max_length=150,choices=CITIES, null=True, blank=True)
    locationLink = models.CharField(max_length=150, validators=[URLValidator(message='Enter a valid Google Maps location link.')], null=True, blank=True)
    coming_from = models.CharField(max_length=150, choices=SOCIAL_CHOICES, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,verbose_name="Client Login License")
    is_active = models.BooleanField(default=True)
    is_viewer_viewed =models.BooleanField(default=False)
    date_viewer_viewed =models.DateTimeField( null=True,blank=True)
    is_tech_viewed =models.BooleanField(default=False)
    date_tech_viewed =models.DateTimeField( null=True,blank=True)
    meeting_time  = models.DateTimeField( null=True,blank=True)
    contract_meeting_time  = models.DateTimeField( null=True,blank=True)
    is_meeting_approved = models.BooleanField(default=False)
    is_contract_meeting_approved = models.BooleanField(default=False)
    is_location_approved = models.BooleanField(default=False)
    is_contract_location_approved = models.BooleanField(default=False)
    is_contract_approved = models.BooleanField(default=False)
    is_3d_design_approved = models.BooleanField(default=False)
    is_client_project_finished = models.BooleanField(default=False)
    is_Project_done = models.BooleanField(default=False)
    notes_for_home = models.TextField(null=True, blank=True)
    preferred_license_method = models.CharField(max_length=150, choices=LICENSE_METHOD_CHOICES, null=True, blank=True)
    company_percentage = models.IntegerField(default= 15)
    def __str__(self):
        return self.name
    

    def has_action(self):
        try:
            clientAction = ClientAction.objects.get(client=self)
            # if clientAction.action == 'searching':
            return True
        except: return False
    def project_client(self):
        try:
            return Project.objects.get(client__uuid=self.uuid)
        except ObjectDoesNotExist:
            return None
    def viewer_message(self):
        text  = f'''
                        تم اضافة عميل جديد قم/ي باستكمال البيانات
                        https://www.backend.support-constructions.com/client/{self.uuid}/update/
                    '''
        return text
    def save(self, *args, **kwargs):
        is_new_client = self.pk is None
        if is_new_client:
            send_slack_notification("#new-customers",self.generate_welcome_message())
            send_slack_notification("#mo3aynat",self.viewer_message())
        if self.slack_channel_name is not None and not self.slack_channel_name.startswith("#"):
            self.slack_channel_name = f"#{self.slack_channel_name}"  # Check if it's a new client (not yet saved)  # Check if it's a new client (not yet saved)
        super().save(*args, **kwargs)  # Save the client first
        send_slack_notification("#customer-service",self.generate_welcome_message())
        
    def action_needed(self):
        
        if not self.is_viewer_viewed:
            return f" markting   add {self.name}"
        if not self.is_tech_viewed:
            return f"team viewer  approved new client {self.name} "
        if self. calculate_data_completion_percentage2() > 20 and  self. calculate_data_completion_percentage2() < 50:
            return f"team viewer: {self.name} action in need"
        if self. calculate_data_completion_percentage2() > 50 :
            return f"technical manager: {self.name} action in need"
            
    def needed_action(self):
        completion_percentage = self.calculate_data_completion_percentage2()

        if 10 < completion_percentage < 20:
            return "نحتاج إلى استكمال بيانات المعاينة."

        if 15 < completion_percentage < 40:
            try:
                project = Project.objects.get(client=self)
                if not project.assign_to_2d_designer:
                    return 'اشر لمصمم الـ 2D.'
                elif not project.assign_to_3d_designer:
                    return 'اشر لمصمم الـ 3D.'
            except:
                pass
            return "نحتاج إلى استكمال دراسة المشروع."

        return "لا توجد إجراءات مطلوبة حاليًا."
    def get_profile_completion_actions(self):
        actions = []

        # if not self.is_active:
        #     actions.append("Activate the profile")

        if not self.is_viewer_viewed:
            actions.append("View the profile")

        if not self.uuid:
            actions.append("Generate a UUID")

        if not self.location:
            actions.append("Provide a location")

        if not self.locationLink:
            actions.append("Provide a Google Maps location link")

        if not self.number:
            actions.append("Provide a phone number")

        if not self.is_contract_location_approved:
            actions.append("Approve the contract location")

        if not self.is_contract_meeting_approved:
            actions.append("Approve the contract meeting")

        if not self.is_meeting_approved:
            actions.append("Approve the meeting")

        if not self.is_tech_viewed:
            actions.append("View the tech information")

        if not self.meeting_time:
            actions.append("Set a meeting time")

        if not self.contract_meeting_time:
            actions.append("Set a contract meeting time")

        if not self.is_location_approved:
            actions.append("Approve the location")

        if not self.is_contract_location_approved:
            actions.append("Approve the contract location")

        if not self.is_client_project_finished:
            actions.append("Finish the client project")

        if not self.is_Project_done:
            actions.append("Mark the project as done")

        return actions  
    def calculate_data_completion_percentage2(self):
        conditions = {
            'is_active': 1,
            'is_viewer_viewed': 1,
            'uuid': 1,
            'location': 1,
            'locationLink': 1,
            'number': 1,
            'is_contract_location_approved': 3,
            'is_contract_meeting_approved': 2,
            'is_meeting_approved': 3,
            'is_tech_viewed': 1,
            'meeting_time': 1,
            'contract_meeting_time': 1,
            'is_location_approved': 1,
            'is_contract_location_approved': 1,
            'is_client_project_finished': 9,
            'is_Project_done': 4
        }

        completed_conditions = sum(conditions[field] for field in conditions if getattr(self, field))
        total_conditions = sum(conditions.values())
        print(total_conditions)
        return int((completed_conditions / total_conditions) * 100)
    def whatsapp_num(self):
        try:
            return self.number[1:]
        except: return None
    def generate_welcome_message(self):
        message = f"""Hello {self.name}!

Welcome to https://support-constructions.com. 

to get your access visit our provider: https://www.backend.support-constructions.com/website/ClientUuid/{self.uuid}"""
        return message
    def generate_welcome_message_for_customerService(self):
        message = f"""Hello {self.name}!

new client added 

to get access to clint : https://www.backend.support-constructions.com/website/ClientUuid/{self.uuid}"""
        return message
    @property
    def calculate_data_completion_percentage(self):
        conditions = {
            'is_active': 1,
            'is_viewer_viewed': 1,
            'uuid': 1,
            'location': 1,
            'locationLink': 1,
            'number': 1,
            'is_contract_location_approved': 3,
            'is_contract_meeting_approved': 2,
            'is_meeting_approved': 3,
            'is_tech_viewed': 1,
            'meeting_time': 1,
            'contract_meeting_time': 1,
            'is_location_approved': 1,
            'is_contract_location_approved': 1,
            'is_client_project_finished': 9,
            'is_Project_done': 4
        }

        completed_conditions = sum(conditions[field] for field in conditions if getattr(self, field))
        total_conditions = sum(conditions.values())
        print(total_conditions)
        return (completed_conditions / total_conditions) * 100
    def percentage_needs(self):
        return 100 -self.calculate_data_completion_percentage2()
    
    @property
    def total_payments(self):
        return Payment.objects.filter(client=self).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def get_all_payments(self, filter_by=None):
        payments = self.payment_set.filter(client=self)
        if filter_by:
            payments = payments.filter(payment_method=filter_by)
        return payments

    @property
    def is_under_expenditure_limit(self):
        return self.total_payments < self.maximum_expenditure
    
    def client_action_notes(self):
        try:
            action = ClientAction.objects.filter(client=self).order_by('-id').first()
            if action:
                return action
            else:
                return "no action"
        except ClientAction.DoesNotExist:
            return "no action"


class ClientAction(models.Model):
    ACTION_CHOICES = [
        ('searching', 'Searching for services'),
        ('future', 'Interested in future services'),
        ('working', 'Considering working with us')
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    notes = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_reported = models.BooleanField(default= False)
    is_viewer_seen = models.BooleanField(default= False)
    is_tech_seen = models.BooleanField(default= False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return f'{self.client.name} - {self.get_action_display()}'
    def save(self, *args, **kwargs):
        is_new_action = self.pk is None  # Check if it's a new action
        super().save(*args, **kwargs)
        if self.action == 'working' and not self.is_reported:
            send_slack_notification("#customer-service-notes-and-actions", self.get_powerful_arabic_message())
            if self.action != 'working': 
                send_slack_notification("#customer-service-notes-and-actions", self.get_powerful_arabic_message2())
    def get_powerful_arabic_message(self):
        if self.action == 'working':
            client_name = self.client.name
            message = f"عميل جديد: {client_name} يفكر في العمل معنا."
            return f":rocket: :muscle: :star2: {message}"
        return None
    def get_powerful_arabic_message2(self):
        if self.action == 'working':
            client_name = self.client.name
            message = f"عميل: {client_name} تم تغير حالة العميل الي مهتم بالعمل معنا شكرا للعمل الجاد ."
            return f":rocket: :muscle: :star2: {message}"
        return None

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now=True,)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    paid_for = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Payment of {self.amount} for client {self.client.name}"  
      
    
    