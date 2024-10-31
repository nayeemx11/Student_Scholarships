# forms.py
from django import forms
from .models import Student
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class StudentApplicationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    mobile_number = forms.CharField(max_length=15, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = [
            "student_identity_number",
            "ssn",
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "user_gender",
            "date_of_birth",
            "current_status",
            "cumulative_gpa",
            "credit_hours",
            "department",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self, commit=True):
        student = super().save(commit=False)  # Retrieve the existing student instance without saving immediately
        user = self.instance.user  # Retrieve the associated user instance
        
        alt_student = Student.objects.get(user = user)
        
        print(student)
        print(alt_student)
        print(student == alt_student)

        # Debug print to confirm data
        print("Saving form data:")
        print(f"Student ID: {student.student_identity_number}")
        print(f"User: {user.username}, Email: {self.cleaned_data.get('email')}, Mobile: {self.cleaned_data.get('mobile_number')}")

        # Update user fields
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.mobile_number = self.cleaned_data.get("mobile_number")
        
        student.save()

        try:
            if commit:
                user.save()  # Save changes to the user
                print("User saved successfully.")
                # student.save()  # Save changes to the student
                # print("Student saved successfully.")
            return student
        except IntegrityError as e:
            print(f"IntegrityError: {e}")  # Print the error message
            raise IntegrityError("A unique constraint error occurred while saving the student instance.")

