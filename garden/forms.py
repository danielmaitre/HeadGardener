from django import forms
from .models import AreaImage, Plant, PlantCategory, PlantJourneyStep, PlantImage


class ColorInput(forms.TextInput):
    input_type = "color"


class DatePickerInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs.setdefault("format", "%Y-%m-%d")
        super().__init__(**kwargs)


class PlantCategoryForm(forms.ModelForm):
    class Meta:
        model = PlantCategory
        fields = ["name", "color"]
        widgets = {"color": ColorInput()}


class AreaImageForm(forms.ModelForm):
    class Meta:
        model = AreaImage
        fields = ["date", "caption"]
        widgets = {"date": DatePickerInput()}


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "category", "notes"]


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class PlantImageUploadForm(forms.Form):
    images = forms.ImageField(
        widget=MultipleFileInput(attrs={"accept": "image/*"}),
        label="Photos",
    )


class PlantJourneyStepForm(forms.ModelForm):
    class Meta:
        model = PlantJourneyStep
        fields = ["step_type", "location", "start_date", "end_date", "notes"]
        widgets = {
            "start_date": DatePickerInput(),
            "end_date": DatePickerInput(),
        }
