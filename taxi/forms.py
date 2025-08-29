from importlib.resources.abc import TraversableResources

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from taxi.models import Driver, Car


class DriverLicenseUpdateForm(UserCreationForm):
    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]
        if len(license_number) != 8:
            raise ValidationError("License_number must have exactly"
                                  " 8 characters")
        elif not (license_number[:3].isupper()):
            raise ValidationError("First 3 charectes of license number must"
                                  " be uppercases")
        elif not (license_number[-5:].isdigit()):
            raise ValidationError("Last 5 characters must be numbers")

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"
