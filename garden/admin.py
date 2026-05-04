from django.contrib import admin
from .models import AnnualTask, AnnualTaskCompletion, GeneralArea, PlantCategory, Location, Plant, PlantJourney, PlantJourneyStep


class PlantJourneyStepInline(admin.TabularInline):
    model = PlantJourneyStep
    extra = 1


class PlantJourneyInline(admin.TabularInline):
    model = PlantJourney
    extra = 1
    show_change_link = True


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1
    fields = ["name", "description"]


@admin.register(GeneralArea)
class GeneralAreaAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]
    inlines = [LocationInline]


@admin.register(PlantCategory)
class PlantCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "area", "description"]
    list_filter = ["area"]
    search_fields = ["name"]


class AnnualTaskInline(admin.TabularInline):
    model = AnnualTask
    extra = 1


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    list_filter = ["category"]
    search_fields = ["name"]
    inlines = [AnnualTaskInline, PlantJourneyInline]


@admin.register(PlantJourney)
class PlantJourneyAdmin(admin.ModelAdmin):
    list_display = ["__str__", "plant", "label", "created_at"]
    list_filter = ["plant__category"]
    search_fields = ["plant__name", "label"]
    inlines = [PlantJourneyStepInline]


@admin.register(AnnualTaskCompletion)
class AnnualTaskCompletionAdmin(admin.ModelAdmin):
    list_display = ["task", "year", "completed_at"]
    list_filter = ["year"]


@admin.register(PlantJourneyStep)
class PlantJourneyStepAdmin(admin.ModelAdmin):
    list_display = ["__str__", "step_type", "location", "start_date", "end_date"]
    list_filter = ["step_type", "location"]
    search_fields = ["journey__plant__name"]
