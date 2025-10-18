from django.db import transaction

from .models import Membership, Organization


class OrganizationService:
    @staticmethod
    @transaction.atomic
    def create_organization_with_admin(user, organization_name=None):
        if not organization_name:
            organization_name = f"{user.email}'s Organization"

        organization = Organization.objects.create(name=organization_name, created_by=user)

        Membership.objects.create(
            user=user,
            organization=organization,
            role=Membership.Role.ADMIN,
            invited_by=None,
        )

        return organization

    @staticmethod
    def get_user_role_in_organization(user, organization):
        try:
            membership = Membership.objects.get(user=user, organization=organization, is_active=True)
            return membership.role
        except Membership.DoesNotExist:
            return None
