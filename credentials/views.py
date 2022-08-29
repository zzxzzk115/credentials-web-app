from time import sleep
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

from credentials import email_helper
from . import template_helper
from gophish import Gophish
import threading

from credentials.models import Credential, CredentialConfigForm

# Create your views here.
def index_handler(request):
    return redirect('https://www.credentials-inc.com')


def pdfcgi2_handler(request):
    try:
        param = str(list(request.GET.keys())[0])
        id = param[6:16]
        email = param[16:]
        try:
            model : Credential = Credential.objects.get(pk=id)
        except:
            return HttpResponse('Credential not Found')
        context = {
            'access_transcript_from': model.access_transcript_from,
            'email_address': email,
            'access_code': model.user_access_code,
            'pdf_name': model.pdf_file_path
        }
        return render(request, 'PDFCGI2.html', context)
    except Exception as e:
        print(e)
        return redirect('https://www.credentials-inc.com/CGI-BIN/PDFCGI2.pgm')


@csrf_exempt
def send_email_handler(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'send_email.html', context)
    elif request.method == 'POST':
        try:
            try:
                query_model : Credential = Credential.objects.get(pk=request.POST['credential_id'])
                model = CredentialConfigForm(request.POST, instance=query_model)
                print('Updating model...')
            except:
                model = CredentialConfigForm(request.POST)
                print('Creating a new model...')
            if model.is_valid():
                saved_model = model.save()
                if len(saved_model.credential_id) != 10:
                    return HttpResponse('Credential ID must be 10 characters.')
                with open('credentials/static/CIimages/' + saved_model.school_logo_path, 'wb+') as des:
                    for chunk in request.FILES.get('school_logo_file').chunks():
                        des.write(chunk)
                with open('credentials/static/pdfs/' + saved_model.pdf_file_path, 'wb+') as des:
                    for chunk in request.FILES.get('pdf_file').chunks():
                        des.write(chunk)
                # Send Email
                print('Sending Part1...')
                gophish = Gophish(api_key=settings.GOPHISH_API_KEY, host=settings.GOPHISH_HOST)
                email_profile = email_helper.SendEmailProfile('',
                    settings.FROM_EMAIL,
                    'CI-R51: PDF Transcript Notification Part1 - ' + saved_model.credential_id,
                    '',
                    '',
                    saved_model.user_email_address,
                    template_helper.get_rendered_html_native(open('credentials/email_templates/part1.html').read(),
                            { 
                                'Name1': saved_model.part1_name1,
                                'Name2': saved_model.part1_name2,
                                'Name3': saved_model.part1_name3,
                                'Email': saved_model.user_email_address,
                                'UntilDate': saved_model.part1_until_date,
                                'LogoURL': saved_model.base_url + '/static/CIimages/' + saved_model.school_logo_path,
                                'Link': saved_model.base_url + '/CGI-BIN/PDFCGI2.pgm?LOGONP' + saved_model.credential_id + saved_model.user_email_address
                            }),
                    None,
                    settings.SMTP_HOST,
                    settings.SMTP_USER_NAME,
                    settings.SMTP_USER_PASSWORD,
                    True)
                try:
                    email_helper._send_email_proc(gophish, email_profile)
                except Exception as e:
                    return HttpResponse('Email Sent Failed. Exception:' + str(e))
                print('Part1 Sent!')
                t = threading.Thread(target=__send_part2_delay, kwargs={'model': saved_model})
                t.setDaemon(True)
                t.start()
                return HttpResponse('Email Sent Successfully')
            else:
                return HttpResponse('Form invalid, please check and retry.')
            
        except Exception as e:
            return HttpResponse("Internal Exception: " + str(e))
    return redirect('https://www.baidu.com')


def __send_part2_delay(*args, **kwargs):
    if settings.DEBUG:
        sleep(5)
    else:
        sleep(5 * 60)
    print('Sending Part2...')
    saved_model = kwargs['model']
    # send_mail('CI-R52: PDF Transcript Notification Part2 - ' + saved_model.credential_id,
    #     None,
    #     None,
    #     [saved_model.user_email_address],
    #     html_message=template_helper.get_rendered_html_native(open('credentials/email_templates/part2.html').read(),
    #             { 
    #                 'Name1': saved_model.part1_name1,
    #                 'Name2': saved_model.part1_name2,
    #                 'LogoURL': saved_model.base_url + '/static/CIimages/' + saved_model.school_logo_path,
    #                 'AccessCode': saved_model.user_access_code
    #             }))
    gophish = Gophish(api_key=settings.GOPHISH_API_KEY, host=settings.GOPHISH_HOST)
    email_profile = email_helper.SendEmailProfile('',
        settings.FROM_EMAIL,
        'CI-R52: PDF Transcript Notification Part2 - ' + saved_model.credential_id,
        '',
        '',
        saved_model.user_email_address,
        template_helper.get_rendered_html_native(open('credentials/email_templates/part2.html').read(),
                { 
                    'Name1': saved_model.part1_name1,
                    'Name2': saved_model.part1_name2,
                    'LogoURL': saved_model.base_url + '/static/CIimages/' + saved_model.school_logo_path,
                    'AccessCode': saved_model.user_access_code
                }),
        None,
        settings.SMTP_HOST,
        settings.SMTP_USER_NAME,
        settings.SMTP_USER_PASSWORD,
        True)
    try:
        email_helper._send_email_proc(gophish, email_profile)
        print('Part2 Sent!')
    except Exception as e:
        print(e)