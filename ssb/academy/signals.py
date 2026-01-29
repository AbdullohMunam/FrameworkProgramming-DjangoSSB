"""
Signals untuk mengirim notifikasi email saat ada pendaftaran baru
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
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
    
    # Skip if no email configured
    if not settings.EMAIL_HOST_USER:
        print("Email not configured - skipping notification")
        return
    
    subject = f"[SSB Academy] Pendaftaran Baru: {instance.name}"
    message = f"""
Ada pendaftaran pemain baru di SSB Academy!

=====================================
DETAIL PENDAFTAR
=====================================
Nama: {instance.name}
Umur: {instance.age} tahun
Posisi: {instance.position}
Username: {instance.user.username}
Email: {instance.user.email}
Tanggal Daftar: {instance.registered_at.strftime('%d/%m/%Y %H:%M') if instance.registered_at else '-'}

=====================================

Silakan login ke admin dashboard untuk approve atau reject pendaftaran ini:
{settings.FRONTEND_URL}/admin/pending

---
Email ini dikirim otomatis oleh sistem SSB Academy.
    """
    
    try:
        # Send directly to admin email
        admin_email = settings.EMAIL_HOST_USER
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email],
            fail_silently=False
        )
        print(f"Email notification sent to {admin_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
