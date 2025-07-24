from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Disease

@receiver(m2m_changed, sender=Disease.medicine.through)
def update_medicine_text(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        medicine_names = ", ".join(m.name for m in instance.medicine.all())
        Disease.objects.filter(pk=instance.pk).update(medicine_text=medicine_names)
