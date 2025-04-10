# serializers.py
from rest_framework import serializers
from .models import ContactSubmission

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['first_name', 'last_name', 'email', 'phone', 'pricing_package', 'message']
