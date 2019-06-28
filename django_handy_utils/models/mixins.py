import uuid

from django.db import models
from django.utils import timezone


class UUIDMixin(models.Model):
    """
    Generate uuid as id field and act as primary key
    """
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
        help_text='Unique ID of the instance')

    class Meta:
        abstract = True


class TimeTrackingMixin(models.Model):
    """
    Track created at and modified at time
    """
    created_at = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
        editable=False,
        help_text='Datetime the instance was created')
    modified_at = models.DateTimeField(
        default=timezone.now,
        null=False,
        blank=False,
        help_text='Datetime the instance was last modified at')

    # Update modified_at field upon save.
    def save(self, *args, **kwargs):
        if getattr(self, 'modified_at'):
            self.modified_at = timezone.now()
        super(TimeTrackingMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Allow model to be soft deleted and track deleted time
    """
    is_deleted = models.BooleanField(
        default=False, help_text='Whether the instance is soft deleted or not')
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Datetime the instance was soft deleted at (if applicable)')

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        super(SoftDeleteMixin, self).save()

    class Meta:
        abstract = True


class DisablableMixin(models.Model):
    """
    Allow model to be disabled and track when disabled
    """
    is_enabled = models.BooleanField(
        default=True, help_text='Whether the instance is enabled or not')
    disabled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Datetime the instance was disabled at (if applicable)')

    class Meta:
        abstract = True


class HideableMixin(models.Model):
    """
    Allow model to be hidden
    """
    is_hidden = models.BooleanField(
        default=False, help_text='Whether the instance is hidden or not')
    hidden_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Datetime the instance was hidden at (if applicable)')

    class Meta:
        abstract = True
