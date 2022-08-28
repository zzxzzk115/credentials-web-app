import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from credentials.models import CredentialConfigForm

# Create your views here.
def index_handler(request):
    return redirect('https://www.credentials-inc.com')


def pdfcgi2_handler(request):
    try:
        param = str(list(request.GET.keys())[0])
        id = param[6:16]
        email = param[16:]
        context = {
            'access_transcript_from': 'University of California, Davis',
            'email_address': email,
            'access_code': 'HbyCs$hV',
            'pdf_name': 'TEST ONLY.pdf'
        }
        return render(request, 'PDFCGI2.html', context)
    except:
        return redirect('https://www.credentials-inc.com/CGI-BIN/PDFCGI2.pgm')


@csrf_exempt
def send_email_handler(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'send_email.html', context)
    elif request.method == 'POST':
        try:
            model = CredentialConfigForm(request.POST)
            if model.is_valid():
                saved_model = model.save()
                if not os.path.exists('credentials/static/caches/'):
                    os.mkdir('credentials/static/caches/')
                with open('credentials/static/caches/' + saved_model.left_logo_path, 'wb+') as des:
                    for chunk in request.FILES.get('left_logo_file').chunks():
                        des.write(chunk)
                with open('credentials/static/caches/' + saved_model.right_logo_path, 'wb+') as des:
                    for chunk in request.FILES.get('right_logo_file').chunks():
                        des.write(chunk)
                with open('credentials/static/pdfs/' + saved_model.pdf_file_path, 'wb+') as des:
                    for chunk in request.FILES.get('pdf_file').chunks():
                        des.write(chunk)
                return HttpResponse('Email Sent!')
            else:
                return HttpResponse('Form invalid, please check and retry.')
        except Exception as e:
            return HttpResponse("Internal Exception: " + e)
    return redirect('https://www.baidu.com')