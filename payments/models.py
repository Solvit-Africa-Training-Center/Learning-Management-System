from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentOrSponsorship(models.Model):
    # Link to student (assuming user model is used)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')

    # Type of payment or sponsorship - you can use choices
    PAYMENT_TYPES = [
        ('payment', 'Payment'),
        ('sponsorship', 'Sponsorship'),
    ]
    type = models.CharField(max_length=20, choices=PAYMENT_TYPES)

    # Document upload (e.g., payment proof)
    document = models.FileField(upload_to='payment_documents/')

    # Approved status (default False until admin approves)
    approved = models.BooleanField(default=False)

    # Timestamp when record was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.type} - {self.created_at.strftime('%Y-%m-%d')}"
