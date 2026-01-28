"""
Signals untuk mengirim notifikasi email saat ada pendaftaran baru
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_admins
from django.conf import settings
from .models import Player


@receiver(post_save, sender=Player)
def player_registration_notify(sender, instance, created, **kwargs):
    """
    Kirim email ke admin saat ada pendaftaran pemain baru
    """
    if not created:
        return
    
    # Hanya kirim notifikasi jika status pending
    if instance.status != Player.STATUS_PENDING:
        return
    
    subject = f"Pendaftaran Baru: {instance.name}"
    message = f"""
Pendaftaran pemain baru di SSB Academy:

Nama: {instance.name}
Umur: {instance.age}
Posisi: {instance.position}
Username: {instance.user.username}
Email: {instance.user.email}

Silakan login ke admin dashboard untuk approve atau reject pendaftaran ini.
    """
    
    try:
        mail_admins(subject, message, fail_silently=True)
    except Exception as e:
        print(f"Failed to send email: {e}")
