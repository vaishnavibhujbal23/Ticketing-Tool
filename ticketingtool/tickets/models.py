from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('REGULAR', 'Regular User'),
        ('ENGINEER', 'Engineer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='REGULAR', db_index=True)

    def is_engineer(self):
        return self.user_type == 'ENGINEER'

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_engineer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        limit_choices_to={'user_type': 'ENGINEER'}  # Only engineers can be assigned
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    def can_update_status(self, user):
        return user.is_engineer() and user == self.assigned_engineer

    def can_comment(self, user):
        return user == self.creator or user == self.assigned_engineer
    
    def can_assign_engineer(self, user):
        return user.is_superuser

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.ticket.title}"
