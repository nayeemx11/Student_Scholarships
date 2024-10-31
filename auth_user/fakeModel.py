from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    state = models.CharField(
        max_length=20,
        choices=[
            ("AL", "Alabama"),
            ("AK", "Alaska"),
            ("AZ", "Arizona"),
            ("AR", "Arkansas"),
            ("CA", "California"),
            ("CO", "Colorado"),
            ("CT", "Connecticut"),
            ("DE", "Delaware"),
            ("FL", "Florida"),
            ("GA", "Georgia"),
        ],
        null=True,
    )
    zipcode = models.IntegerField()
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True,
    )

    def __str__(self):
        return self.username
