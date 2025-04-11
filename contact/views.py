from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(['POST'])
def submit_contact_form(request):
    serializer = ContactSubmissionSerializer(data=request.data)
    
    if serializer.is_valid():
        contact_submission = serializer.save()

        subject = f"New contact form submission from {contact_submission.first_name} {contact_submission.last_name}"
        email_body = (
            f"Message from {contact_submission.first_name} {contact_submission.last_name}:\n\n"
            f"{contact_submission.message}\n\n"
            f"Phone: {contact_submission.phone}\n"
            f"Pricing Package: {contact_submission.pricing_package}"
        )

        try:
            send_mail(
                subject,
                email_body,
                contact_submission.email,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
            return Response({"error": "Form saved, but email failed to send."}, status=500)

        return Response({"success": True, "message": "Form submitted successfully!"}, status=201)

    return Response(serializer.errors, status=400)
