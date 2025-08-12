from rest_framework import serializers
from .models import PaymentOrSponsorship  # make sure class name matches exactly

class PaymentOrSponsorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrSponsorship
        fields = ['id', 'student', 'type', 'document', 'approved', 'created_at']
        read_only_fields = ['approved', 'created_at']
