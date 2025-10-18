from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Organization(models.Model):
    name = models.CharField(_("Organization Name"), max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_organizations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - Created by {self.created_by.name}"


class Membership(models.Model):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Admin")
        EDITOR = ("editor", "Editor")
        VIEWER = ("viewer", "Viewer")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)
    invited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sent_invitations"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("user", "organization")]
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user.name} - {self.organization.name} ({self.role})"
