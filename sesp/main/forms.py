from django import forms
from django.forms.widgets import PasswordInput
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from database.models import *

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    photo       = forms.ImageField()

    email = forms.EmailField(
        max_length=75,
        validators = [
            RegexValidator(
                regex='$',
                message='NTU Email is Required',
                code='invalid_ntuemail'
            ),
        ]
    )
    password = forms.CharField(
        widget=PasswordInput,
        validators = [MinLengthValidator(8)]
    )
    cfm_password = forms.CharField(widget=PasswordInput)

    def clean_email(self):
        # Perform checking for existing email used by user
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already in use")

        return email

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        # Perform checking for password confirmation
        password = cleaned_data.get("password")
        cfm_password = cleaned_data.get("cfm_password")

        if password and cfm_password and password != cfm_password:
            self._errors["cfm_password"] = self.error_class(["Confirm password does not match"])

            del cleaned_data["password"]
            del cleaned_data["cfm_password"]

        return cleaned_data

class PasswordForgetForm(forms.Form):
    email = forms.EmailField(
        max_length=75,
        validators = [
            RegexValidator(
                regex='$',
                message='Email is Required',
                code='invalid_ntuemail'
            ),
        ]
    )

    def clean_email(self):
        # Perform checking for existing email used by user
        email = self.cleaned_data['email']

        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account has been registered with this email")

        return email

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=75,
        validators = [
            RegexValidator(
                regex='$',
                message='Email is Required',
                code='invalid_ntuemail'
            ),
        ]
    )
    password = forms.CharField(
        widget=PasswordInput,
        validators = [MinLengthValidator(8)]
    )
    cfm_password = forms.CharField(widget=PasswordInput)

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()

        # Perform checking for password confirmation
        password = cleaned_data.get("password")
        cfm_password = cleaned_data.get("cfm_password")

        if password and cfm_password and password != cfm_password:
            self._errors["cfm_password"] = self.error_class(["Confirm password does not match"])

            del cleaned_data["password"]
            del cleaned_data["cfm_password"]

        return cleaned_data

class ActivationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class FeedbackForm(forms.Form):
    feedback = forms.CharField()


class EventForm(forms.Form):
    title       = forms.CharField()
    description = forms.CharField()
    content     = forms.CharField()
    test        = forms.CharField()
    image       = forms.ImageField()
    organizer   = forms.CharField()

class CommentForm(forms.Form):
    content     = forms.CharField()



