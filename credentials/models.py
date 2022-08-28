from django.db import models
from django.forms import ModelForm

# Create your models here.
class Credential(models.Model):
    credential_id = models.TextField(primary_key=True)
    base_url = models.TextField()
    access_transcript_from = models.TextField()
    user_email_address = models.EmailField()
    user_access_code = models.TextField()
    left_logo_path = models.TextField()
    right_logo_path = models.TextField()
    pdf_file_path = models.TextField()


class CredentialConfigForm(ModelForm):
    class Meta:
        model = Credential
        fields = ['base_url', 'credential_id', 'access_transcript_from',
            'user_email_address', 'user_access_code',
            'left_logo_path', 'right_logo_path', 'pdf_file_path']


# class UserSubmitCredentialInfoForm(ModelForm):
#     class Meta:
#         model = Credential
#         fields = ['user_first_name', 'user_middle_name', 'user_last_name', 
#             'user_telephone_number', 'user_submit_date_time']