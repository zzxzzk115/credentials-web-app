from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index_handler(request):
    return redirect('https://www.credentials-inc.com')


def pdfcgi2_handler(request):
    try:
        param = str(list(request.GET.keys())[0])
        id = param[6:16]
        email = param[17:]
        context = {
            'access_transcript_from': 'University of California, Davis',
            'email_address': email,
            'access_code': 'HbyCs$hV',
            'pdf_name': 'TEST ONLY.pdf'
        }
        return render(request, 'PDFCGI2.html', context)
    except:
        return redirect('https://www.credentials-inc.com/CGI-BIN/PDFCGI2.pgm')