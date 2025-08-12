from django.urls import path
from .views import SubmitPaymentOrSponsorshipView, ApprovePaymentOrSponsorshipView

urlpatterns = [
    path('submit/', SubmitPaymentOrSponsorshipView.as_view(), name='submit-payment-sponsorship'),
    path('approve/<int:pk>/', ApprovePaymentOrSponsorshipView.as_view(), name='approve-payment-sponsorship'),
]
