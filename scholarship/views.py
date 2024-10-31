from decimal import Decimal
from django.db import IntegrityError
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student, Application, Award, Message
from .forms import StudentApplicationForm


@login_required
def update_student_info(request):
    # Retrieve the current user's Student instance
    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST":
        print("method post")
        form = StudentApplicationForm(request.POST, instance=student)
        if form.is_valid():
            print("valid post")
            try:
                form.save()
                print("save post")  # Debug print after save
                messages.success(
                    request, "Your information has been updated successfully!"
                )
                return redirect("update_student_info")  # Adjust as necessary
            except IntegrityError as e:
                print(f"IntegrityError in view: {e}")  # Print error if it occurs
                messages.error(
                    request, "An error occurred while updating. Please try again."
                )
        else:
            print("Form errors:", form.errors)  # Debug print for form errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = StudentApplicationForm(instance=student)

    return render(request, "student/update_student_info.html", {"form": form})


@login_required
def verify_student(request):
    # Retrieve the current user's Student instance
    student = get_object_or_404(Student, user=request.user)

    # List of fields to verify
    required_fields = {
        "student_identity_number": "Student identity number",
        "ssn": "Social Security Number",
        "first_name": ("First name", student.user.first_name),
        "last_name": ("Last name", student.user.last_name),
        "email": ("Email address", student.user.email),
        "mobile_number": ("Mobile number", student.user.mobile_number),
        "user_gender": "Gender",
        "date_of_birth": "Date of birth",
        "current_status": "Current status",
        "cumulative_gpa": "Cumulative GPA",
        "credit_hours": "Credit hours",
        "department": "Department",
    }

    # Check for null or empty fields
    for field, value in required_fields.items():
        if isinstance(value, tuple):  # For user-related fields
            field_name, field_value = value
        else:
            field_name = value
            field_value = getattr(student, field)

        if field_value is None or (
            isinstance(field_value, str) and not field_value.strip()
        ):
            messages.error(request, f"{field_name} cannot be empty or null.")
            return redirect("update_student_info")

    current_year = timezone.now().year
    age_at_application = current_year - student.date_of_birth.year
    if (
        student.cumulative_gpa >= 3.2
        and student.credit_hours >= 12
        and age_at_application <= 23
    ):
        student.eligible_for_application = True
        student.save()

    messages.success(request, "All fields are valid.")
    print("All fields are valid.")

    return redirect("view_application")  # Redirect to the appropriate page


from django.core.exceptions import ObjectDoesNotExist


@login_required
def apply_scholarship(request):
    print("Starting scholarship application process...")
    student = get_object_or_404(Student, user=request.user)
    print(f"Student retrieved: {student}")

    # Check if the request is a POST and if the student is eligible to apply
    if request.method == "POST":
        print("Received POST request.")
        if student.eligible_for_application:
            print("Student is eligible for application.")
            try:
                # Attempt to retrieve an existing application for the student
                application = Application.objects.get(student=student)
                print("Existing application found.")
                # Redirect to view the existing application
                return view_application(request)
            except ObjectDoesNotExist:
                print("No existing application found; creating a new application.")
                # No application exists, so create a new one
                Application.objects.create(
                    student=student,
                    applied=True,
                )
                messages.success(request, "Application submitted successfully!")
                print("Application created and saved successfully.")
                return redirect("view_application")
        else:
            messages.error(
                request, "You are not eligible to apply for this scholarship."
            )
            print("Student is not eligible for application.")
    else:
        print("Request method is not POST.")
        messages.error(request, "Invalid request method for applying.")

    print("Redirecting to update student info page.")
    return redirect("update_student_info")


@login_required
def view_application(request):
    student = get_object_or_404(Student, user=request.user)
    application = get_object_or_404(Application, student=student)
    context = {
        "application": application,
    }
    return render(request, "student/view_application.html", context)


def message(request):
    student = get_object_or_404(Student, user=request.user)
    print(student)
    messages_all = Message.objects.filter(student=student) if student else []

    context = {
        "messages_all": messages_all,
    }
    return render(request, "student/message.html", context)


def comm_home(request):
    return render(request, "comm_home.html")


# checks criteria
def check_eligibility(request):
    applications = Application.objects.filter(applied=True)
    current_year = timezone.now().year
    # Eligibility criteria
    for application in applications:
        student = application.student
        age_at_application = current_year - student.date_of_birth.year
        if (
            student.cumulative_gpa >= 3.2
            and student.credit_hours >= 12
            and age_at_application <= 23
        ):
            application.can_get_scholarship = True
        else:
            application.can_get_scholarship = False
        application.save()


def view_applicant(request):
    check_eligibility(request)
    applications = Application.objects.filter(applied=True)
    context = {
        "applications": applications,
    }
    return render(request, "view_applicant.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application, Student

@login_required
def selected_applicant(request):
    applications = Application.objects.filter(applied=True)
    context = {
        "applications": applications,
    }
    return render(request, "selected_applicant.html", context)


@login_required
def info_send(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    student = application.student

    # Prepare initial data for the form fields
    initial_data = {
        'student_identity_number': student.student_identity_number,
        'first_name': student.user.first_name,
        'last_name': student.user.last_name,
        'email': student.user.email,
    }

    # Pass the initial data to the context
    context = {
        "application": application,
        "initial_data": initial_data,
    }
    return render(request, "info_send.html", context)

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from decimal import Decimal
from .models import Award, Message, Student

def award_send(request, student_identity_number):
    student = get_object_or_404(Student, student_identity_number=student_identity_number)
    
    if request.method == "POST":
        # Retrieve form data from POST request
        amount = request.POST.get("amount")
        season = request.POST.get("season")
        
        # Convert the amount to a Decimal if needed
        amount = Decimal(amount)

        # Check if an award for the student in the given season already exists
        award, created = Award.objects.get_or_create(
            student=student,
            season=season,
            defaults={"amount": amount, "gets_scholarship": True}
        )
        
        if not created:
            # If the award already exists, add to the existing amount
            award.amount += amount
            award.save()

        # Create a message with the award details
        Message.objects.create(
            student=student,
            award=award,
            season_received=season,
            amount_received=amount  # Use updated amount if it was modified
        )

        # Redirect to awarded_student after saving
        return redirect("awarded_student")

    # Redirect with application_id, or render the template directly
    # Assuming `info_send` expects `application_id`, retrieve it accordingly
    application_id = ...  # retrieve application_id or define its logic here
    return redirect(reverse("info_send", args=[application_id]))


def awarded_student(request):
    awards = Award.objects.filter(gets_scholarship=True)
    context = {
        "awards": awards,
    }
    return render(request, "awarded_student.html", context)


@login_required
def committee_dashboard(request):
    eligible_applications = Application.objects.filter(
        can_get_scholarship=True
    ).order_by("-student__cumulative_gpa")

    if eligible_applications.exists():
        # Only access the first application if there are eligible applications
        student_gets_scholarship = eligible_applications[0].student
    else:
        student_gets_scholarship = None  # No eligible student

    return render(
        request,
        "committee_dashboard.html",
        {
            "student_eligible": eligible_applications,
            "student_gets_scholarship": student_gets_scholarship,
        },
    )


@login_required
def award_scholarship(request):
    check_eligibility(request)
    eligible_applications = Application.objects.filter(
        can_get_scholarship=True
    ).order_by("-student__cumulative_gpa")

    if not eligible_applications:
        messages.error(request, "No eligible applicants found.")
        return redirect("committee_dashboard")

    top_gpa = eligible_applications[0].student.cumulative_gpa
    top_students = [
        app for app in eligible_applications if app.student.cumulative_gpa == top_gpa
    ]

    if len(top_students) > 1:
        top_students.sort(
            key=lambda x: (
                -x.student.cumulative_gpa,
                x.student.current_status == "Junior",
                x.student.user_gender == "Female",
                x.student.date_of_birth,
            )
        )

    winner = top_students[0].student
    Award.objects.create(
        student=winner, amount=5000, balance=1500, gets_scholarship=True
    )
    messages.success(
        request,
        f"Scholarship awarded to {winner.user.first_name} {winner.user.last_name}.",
    )

    return redirect("committee_dashboard")


@login_required
def send_mail_to_awarded_student(request):
    try:
        winner = Award.objects.get(gets_scholarship=True)
    except Award.DoesNotExist:
        messages.error(request, "No awarded student found.")
        return redirect("committee_dashboard")

    # # Send congratulatory email to winner
    # send_mail(
    #     "Congratulations!",
    #     f"Dear {winner.student.user.first_name}, you have been awarded the Smart Scholarship.",
    #     "admin@example.com",
    #     [winner.student.user.email],
    # )

    messages.success(
        request,
        f"Scholarship awarded to {winner.student.user.first_name} {winner.student.user.last_name}.",
    )

    return redirect("committee_dashboard")


@login_required
def notify_other_eligible_applicants(request):
    try:
        winner = Award.objects.get(gets_scholarship=True)
    except Award.DoesNotExist:
        messages.error(request, "No awarded student found.")
        return redirect("committee_dashboard")

    # Notify other eligible applicants
    eligible_applications = Application.objects.filter(
        can_get_scholarship=True
    ).exclude(student=winner.student)

    # for application in eligible_applications:
    #     send_mail(
    #         "Scholarship Outcome",
    #         f"Dear {application.student.user.first_name}, unfortunately you were not selected for the scholarship.",
    #         "admin@example.com",
    #         [application.student.user.email],
    #     )

    return redirect("committee_dashboard")
