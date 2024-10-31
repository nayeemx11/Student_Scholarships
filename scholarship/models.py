from django.db import models
from django.conf import settings
from decimal import Decimal

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_identity_number = models.CharField(max_length=10)
    ssn = models.CharField(max_length=9, null=True, blank=True, unique=True)
    user_gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
        null=True,
    )
    date_of_birth = models.DateField(null=True)
    current_status = models.CharField(
        max_length=20,
        choices=[
            ("Freshman", "Freshman"),
            ("Sophomore", "Sophomore"),
            ("Junior", "Junior"),
            ("Senior", "Senior"),
        ],
    )
    cumulative_gpa = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    credit_hours = models.IntegerField(null=True)
    department = models.CharField(max_length=20, null=True)
    
    eligible_for_application = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.id} of {self.user.username}"


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_applied = models.DateField(auto_now_add=True)
    scholarship_status = models.BooleanField(default=False)
    applied = models.BooleanField(default=False)
    can_get_scholarship = models.BooleanField(default=False)
    # Add review_status or scholarship_type if needed


class Award(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    awarded_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    season = models.CharField(
        max_length=50,
        choices=[
            ("Spring", "Spring"),
            ("Fall", "Fall"),
            ("Summer", "Summer"),
        ],
    )
    gets_scholarship = models.BooleanField(default=False)
    

class Message(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    season_received = models.CharField(max_length=20)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    

