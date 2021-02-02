from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings

@csrf_exempt
def contact_us(request):
    if request.method == 'POST':
        sender_email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(
            subject,
            message,
           sender_email,
           ['settings.EMAIL_HOST_USER'],
            fail_silently=False,
        )


    return redirect('contact')
