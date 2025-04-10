from django.db import models

class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    pricing_package = models.CharField(max_length=100, blank=True, null=True)  # Added field for pricing package
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.first_name} {self.last_name}"
