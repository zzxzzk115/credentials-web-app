from django.db import models
from django.forms import ModelForm

# Create your models here.
class Credential(models.Model):
    credential_id = models.TextField(primary_key=True)
    base_url = models.TextField()
    access_transcript_from = models.TextField()
    user_email_address = models.EmailField()
    user_access_code = models.TextField()
    part1_name1 = models.TextField()
    part1_name2 = models.TextField()
    part1_name3 = models.TextField()
    part1_until_date = models.TextField()
    part1_university_website = models.TextField()
    school_logo_path = models.TextField()
    pdf_file_path = models.TextField()
    email_send_interval = models.TextField()


class CredentialConfigForm(ModelForm):
    class Meta:
        model = Credential
        fields = ['base_url', 'credential_id', 'access_transcript_from',
            'user_email_address', 'user_access_code', 'part1_name1',
            'part1_name2', 'part1_name3', 'part1_until_date',
            'part1_university_website', 'school_logo_path',
            'pdf_file_path', 'email_send_interval']


# class UserSubmitCredentialInfoForm(ModelForm):
#     class Meta:
#         model = Credential
#         fields = ['user_first_name', 'user_middle_name', 'user_last_name', 
#             'user_telephone_number', 'user_submit_date_time']