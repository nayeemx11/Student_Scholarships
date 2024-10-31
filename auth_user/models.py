from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    state = models.CharField(
        max_length=20,
        choices=[
            ("Alabama", "Alabama"),
            ("Alaska", "Alaska"),
            ("Arizona", "Arizona"),
            ("Arkansas", "Arkansas"),
            ("California", "California"),
            ("Colorado", "Colorado"),
            ("Connecticut", "Connecticut"),
            ("Delaware", "Delaware"),
            ("Florida", "Florida"),
            ("Georgia", "Georgia"),
        ],
        null=True,
    )
    zipcode = models.IntegerField(null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    # Add related_name attributes to prevent clashes with default auth.User groups and permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Change related_name to prevent clash with auth.User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Change related_name to prevent clash with auth.User.user_permissions
        blank=True,
    )

    def __str__(self):
        return self.username
