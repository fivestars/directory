from directory.models import Employee, Pet
from django.forms import ModelForm


class EditForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ("start_date", "birthday", "image_url")


class PetEditForm(ModelForm):
    class Meta:
        model = Pet
        exclude = ("owner", "image_url")
