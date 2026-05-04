from django.urls import path
from . import views

urlpatterns = [
    # Annual tasks
    path("tasks/", views.AnnualTaskOverviewView.as_view(), name="annual-task-overview"),
    path("tasks/<int:pk>/toggle/", views.AnnualTaskToggleView.as_view(), name="annual-task-toggle"),
    path("plants/<int:plant_pk>/tasks/new/", views.AnnualTaskCreateView.as_view(), name="annual-task-create"),
    path("tasks/<int:pk>/edit/", views.AnnualTaskUpdateView.as_view(), name="annual-task-update"),
    path("tasks/<int:pk>/delete/", views.AnnualTaskDeleteView.as_view(), name="annual-task-delete"),

    # Plants
    path("plants/", views.PlantListView.as_view(), name="plant-list"),
    path("plants/new/", views.PlantCreateView.as_view(), name="plant-create"),
    path("plants/<int:pk>/", views.PlantDetailView.as_view(), name="plant-detail"),
    path("plants/<int:pk>/edit/", views.PlantUpdateView.as_view(), name="plant-update"),
    path("plants/<int:pk>/delete/", views.PlantDeleteView.as_view(), name="plant-delete"),
    path("photos/<int:pk>/delete/", views.PlantImageDeleteView.as_view(), name="plant-image-delete"),
    path("plants/<int:plant_pk>/photos/add/", views.PlantImageUploadView.as_view(), name="plant-image-upload"),
    path("plants/<int:plant_pk>/journeys/new/", views.PlantJourneyCreateView.as_view(), name="journey-create"),

    # Journeys
    path("journeys/", views.PlantJourneyListView.as_view(), name="journey-list"),
    path("journeys/new/", views.PlantJourneyStandaloneCreateView.as_view(), name="journey-create-standalone"),
    path("journeys/<int:pk>/", views.PlantJourneyDetailView.as_view(), name="journey-detail"),
    path("journeys/<int:pk>/edit/", views.PlantJourneyUpdateView.as_view(), name="journey-update"),
    path("journeys/<int:pk>/delete/", views.PlantJourneyDeleteView.as_view(), name="journey-delete"),
    path("journeys/<int:journey_pk>/steps/new/", views.PlantJourneyStepCreateView.as_view(), name="step-create"),

    # Steps
    path("steps/<int:pk>/edit/", views.PlantJourneyStepUpdateView.as_view(), name="step-update"),
    path("steps/<int:pk>/delete/", views.PlantJourneyStepDeleteView.as_view(), name="step-delete"),

    # Locations
    path("locations/", views.LocationListView.as_view(), name="location-list"),
    path("locations/new/", views.LocationCreateView.as_view(), name="location-create"),
    path("locations/<int:pk>/edit/", views.LocationUpdateView.as_view(), name="location-update"),

    # General Areas
    path("areas/", views.GeneralAreaListView.as_view(), name="area-list"),
    path("areas/new/", views.GeneralAreaCreateView.as_view(), name="area-create"),
    path("areas/<int:pk>/edit/", views.GeneralAreaUpdateView.as_view(), name="area-update"),
    path("areas/<int:pk>/gantt/", views.AreaGanttView.as_view(), name="area-gantt"),

    # Categories
    path("categories/", views.PlantCategoryListView.as_view(), name="category-list"),
    path("categories/new/", views.PlantCategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:pk>/edit/", views.PlantCategoryUpdateView.as_view(), name="category-update"),
]
