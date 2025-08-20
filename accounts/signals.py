from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import CustomUser
from api.models import Student,Instructor


old_roles = {}

@receiver(pre_save, sender=CustomUser)
def store_old_role(sender, instance, **kwargs):
    if instance.pk: 
        try:
            old_roles[instance.pk] = sender.objects.get(pk=instance.pk).role
        except sender.DoesNotExist:
            old_roles[instance.pk] = None

@receiver(post_save, sender=CustomUser)
def create_user_role(sender, instance, created, **kwargs):
    old_role = old_roles.pop(instance.pk, None)


    if instance.role == "student" and (created or old_role != "student"):
        Student.objects.get_or_create(user=instance)

    elif instance.role == "instructor" and (created or old_role != "instructor"):
        Instructor.objects.get_or_create(user=instance)