from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Coach(models.Model):
    name = models.CharField(max_length=100)
    license_level = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='coaches/', blank=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50)
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to='players/', blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Approval fields
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    registered_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_players')
    
    @property
    def profile_completed(self):
        """Check if user has completed their profile"""
        return bool(self.name and self.age and self.position)

    def __str__(self):
        return self.name or self.user.username


class TrainingSchedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.group.name} - {self.date}"


# Signal to delete User when Player is deleted
@receiver(post_delete, sender=Player)
def delete_user_with_player(sender, instance, **kwargs):
    """
    Delete associated User when Player is deleted
    This creates bidirectional cascade delete:
    - User deleted → Player deleted (via CASCADE)
    - Player deleted → User deleted (via this signal)
    """
    try:
        if instance.user:
            instance.user.delete()
    except User.DoesNotExist:
        pass  # User already deleted
