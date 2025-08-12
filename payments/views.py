from rest_framework import generics, permissions
from .models import PaymentOrSponsorship
from .serializers import PaymentOrSponsorshipSerializer

class SubmitPaymentOrSponsorshipView(generics.CreateAPIView):
    """
    Student uploads payment proof or sponsorship letter.
    Admin will approve later.
    """
    queryset = PaymentOrSponsorship.objects.all()
    serializer_class = PaymentOrSponsorshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)

class ApprovePaymentOrSponsorshipView(generics.UpdateAPIView):
    
    # Admin approves payment or sponsorship document.
    
    queryset = PaymentOrSponsorship.objects.all()
    serializer_class = PaymentOrSponsorshipSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(approved=True)
