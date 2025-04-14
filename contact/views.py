import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
        message = (
            f"Message:\n{contact_submission.message}\n\n"
            f"Phone: {contact_submission.phone}\n"
            f"Pricing Package: {contact_submission.pricing_package}\n"
            f"Email: {contact_submission.email}"
        )

        # Send via Mailgun HTTP API
        print("MAILGUN_DOMAIN =", os.environ.get('MAILGUN_DOMAIN'))

        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{os.environ.get('MAILGUN_DOMAIN')}/messages",
                auth=("api", os.environ.get('MAILGUN_API_KEY')),
                data={
                    "from": f"Website Contact Form <postmaster@{os.environ.get('MAILGUN_DOMAIN')}>",
                    "to": ["webmaster@emishapirophotography.com", "emishapirophotography@gmail.com"],
                    "subject": subject,
                    "text": message,
                }
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Mailgun API error:", e)
            return Response({"error": "Form saved, but email failed to send."}, status=500)

        return Response({"success": True, "message": "Form submitted and email sent!"}, status=201)

    return Response(serializer.errors, status=400)
