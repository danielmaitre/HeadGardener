from django import forms
from .models import PlantCategory, PlantJourneyStep


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


class PlantJourneyStepForm(forms.ModelForm):
    class Meta:
        model = PlantJourneyStep
        fields = ["step_type", "location", "start_date", "end_date", "notes"]
        widgets = {
            "start_date": DatePickerInput(),
            "end_date": DatePickerInput(),
        }
