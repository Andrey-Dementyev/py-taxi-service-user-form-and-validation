from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Car, Driver


class LicenseNumberValidationMixin:
    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if (
            len(license_number) != 8
            or not license_number[:3].isalpha()
            or not license_number[:3].isupper()
            or not license_number[3:].isdigit()
        ):
            raise ValidationError(
                "Ensure that the license number consist of "
                "8 characters: first 3 characters are uppercase letters, "
                "last 5 characters are digits."
            )

        return license_number


class DriverCreationForm(LicenseNumberValidationMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class DriverLicenseUpdateForm(LicenseNumberValidationMixin, forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"