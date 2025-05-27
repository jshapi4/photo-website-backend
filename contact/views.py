import os
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


def create_html_email(contact_submission):
    """This function creates a modern HTML email template for contact form submissions."""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Form Submission</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <!-- Header with logo -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                                <img src="https://emishapirophotography.com/assets/Emi_Shapiro_Logo.PNG" alt="Emi Shapiro Photography" style="max-width: 150px; height: auto; margin-bottom: 10px;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 300;">New Contact Form Submission</h1>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 25px; border-left: 4px solid #667eea;">
                                    <h2 style="color: #333333; margin: 0 0 15px 0; font-size: 20px;">Contact Information</h2>
                                    <table width="100%" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">
                                                <strong style="color: #495057; font-size: 14px;">Name:</strong>
                                                <span style="color: #333333; font-size: 16px; margin-left: 10px;">{contact_submission.first_name} {contact_submission.last_name}</span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">
                                                <strong style="color: #495057; font-size: 14px;">Email:</strong>
                                                <a href="mailto:{contact_submission.email}" style="color: #667eea; text-decoration: none; font-size: 16px; margin-left: 10px;">{contact_submission.email}</a>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 8px 0; border-bottom: 1px solid #e9ecef;">
                                                <strong style="color: #495057; font-size: 14px;">Phone:</strong>
                                                <a href="tel:{contact_submission.phone}" style="color: #667eea; text-decoration: none; font-size: 16px; margin-left: 10px;">{contact_submission.phone}</a>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 8px 0;">
                                                <strong style="color: #495057; font-size: 14px;">Pricing Package:</strong>
                                                <span style="color: #333333; font-size: 16px; margin-left: 10px; background-color: #e9ecef; padding: 2px 8px; border-radius: 4px;">{contact_submission.pricing_package}</span>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                                
                                <div style="background-color: #ffffff; padding: 20px; border: 1px solid #e9ecef; border-radius: 8px;">
                                    <h3 style="color: #333333; margin: 0 0 15px 0; font-size: 18px;">Message:</h3>
                                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; font-size: 16px; line-height: 1.6; color: #495057;">
                                        {contact_submission.message.replace(chr(10), '<br>')}
                                    </div>
                                </div>
                                
                                <!-- Call to action -->
                                <div style="text-align: center; margin-top: 30px;">
                                    <a href="mailto:{contact_submission.email}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 25px; font-size: 16px; font-weight: 500; display: inline-block;">Reply to Client</a>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; border-top: 1px solid #e9ecef;">
                                <p style="margin: 0; color: #6c757d; font-size: 14px;">
                                    This email was sent from your website contact form.<br>
                                    <strong>Emi Shapiro Photography</strong>
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


@csrf_exempt
@api_view(['POST'])
def submit_contact_form(request):
    serializer = ContactSubmissionSerializer(data=request.data)

    if serializer.is_valid():
        contact_submission = serializer.save()

        # Prepare email subject and message
        subject = (
            f"📸 New Contact Form Submission - "
            f"{contact_submission.first_name} {contact_submission.last_name}"
        )

        # Create both HTML and plain text versions
        html_message = create_html_email(contact_submission)

                # Plain text fallback
        text_message = (
            f"NEW CONTACT FORM SUBMISSION\n"
            f"{'='*40}\n\n"
            f"Name: {contact_submission.first_name} {contact_submission.last_name}\n"
            f"Email: {contact_submission.email}\n"
            f"Phone: {contact_submission.phone}\n"
            f"Pricing Package: {contact_submission.pricing_package}\n\n"
            f"MESSAGE:\n"
            f"{'-'*20}\n"
            f"{contact_submission.message}\n\n"
            f"Sent from Emi Shapiro Photography website"
        )

        # Send email via Mailgun HTTP API
        mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
        mailgun_api_key = os.environ.get('MAILGUN_API_KEY')

        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
                auth=("api", mailgun_api_key),
                data={
                    "from": f"Emi Shapiro Photography Contact Form <postmaster@{mailgun_domain}>",
                    "to": ["webmaster@emishapirophotography.com", "emishapirophotography@gmail.com"],
                    "subject": subject,
                    "text": text_message,
                    "html": html_message,  # Uncomment if you implement HTML version
                }
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Mailgun API error:", e)
            return Response({"error": "Form saved, but email failed to send."}, status=500)

        return Response({"success": True, "message": "Form submitted and email sent!"}, status=201)

    return Response(serializer.errors, status=400)
