# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer

@api_view(['POST'])
def submit_contact_form(request):
    if request.method == 'POST':
        # ensure front end data is passed through correctly
        serializer = ContactSubmissionSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new contact submission to the database
            contact_submission = serializer.save()

            # Send email notification to the admin (or any email address)
            subject = f"New contact form submission from {contact_submission.first_name} {contact_submission.last_name}"
# Send email notification to the admin (or any email address)
            subject = f"New contact form submission from {contact_submission.first_name} {contact_submission.last_name}"
            email_body = f"Message from {contact_submission.first_name} {contact_submission.last_name}:\n\n{contact_submission.message}\n\n"
            email_body += f"Phone: {contact_submission.phone}\n"
            email_body += f"Pricing Package: {contact_submission.pricing_package}"
            
            send_mail(
                subject,
                email_body,
                contact_submission.email,  # Sender's email address
                [settings.EMAIL_HOST_USER],  # Admin email (the one that will receive the message)
                fail_silently=False,
            )

            return Response({"success": True, "message": "Form submitted successfully!"}, status=201)

        return Response(serializer.errors, status=400)