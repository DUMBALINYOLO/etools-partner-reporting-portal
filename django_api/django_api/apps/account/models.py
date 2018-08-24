from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.functional import cached_property

from model_utils.models import TimeStampedModel

from core.common import PRP_ROLE_TYPES, USER_TYPES


class User(AbstractUser):
    """
    User model inherited after AbstractUser class.

    related models:
        partner.Partner (ForeignKey): "partner"
    """
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    partner = models.ForeignKey(
        'partner.Partner', related_name="users", null=True, blank=True
    )
    organization = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True
    )
    position = models.CharField(max_length=64, null=True, blank=True, default=None)

    def __str__(self):
        return '[{}] {} ({})'.format(
            self.pk, self.get_fullname(), self.username
        )

    def get_fullname(self):
        return ' '.join(filter(None, [self.first_name, self.last_name]))

    @property
    def display_name(self):
        full_name = self.get_fullname()
        return full_name + ' ({})'.format(self.email) if full_name else self.email

    @cached_property
    def is_unicef(self):
        return self.username == getattr(settings, 'DEFAULT_UNICEF_USER', None)

    @classmethod
    def lock_password_if_new(cls, sender, instance, created, **kwargs):
        if created:
            instance.set_unusable_password()
            instance.save()

    @cached_property
    def role_list(self):
        return self.prp_roles.values_list('role', flat=True).distinct()

    @property
    def user_type(self):
        user_prp_roles = set(self.role_list)
        if PRP_ROLE_TYPES.cluster_system_admin in user_prp_roles:
            return USER_TYPES.cluster_admin
        if PRP_ROLE_TYPES.cluster_imo in user_prp_roles:
            return USER_TYPES.imo
        if {PRP_ROLE_TYPES.cluster_member,
            PRP_ROLE_TYPES.cluster_viewer,
            PRP_ROLE_TYPES.cluster_coordinator}.intersection(user_prp_roles):
            return USER_TYPES.partner


class UserProfile(TimeStampedModel):
    """
    User Profile model related with user as profile.

    related models:
        account.User (OneToOne): "user"
    """
    user = models.OneToOneField(User, related_name="profile")

    def __str__(self):
        return "{} - Profile".format(self.user.get_fullname())

    @classmethod
    def create_user_profile(cls, sender, instance, created, **kwargs):
        """
        Signal handler to create user profiles automatically
        """
        if created:
            cls.objects.create(user=instance)


post_save.connect(UserProfile.create_user_profile, sender=User)
post_save.connect(User.lock_password_if_new, sender=User)
