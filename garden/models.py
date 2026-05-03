from django.db import models


class PlantCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default="#4caf50")

    class Meta:
        verbose_name_plural = "plant categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class GeneralArea(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    area = models.ForeignKey(
        GeneralArea,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="locations",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Plant(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        PlantCategory, on_delete=models.PROTECT, related_name="plants"
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PlantJourney(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="journeys")
    label = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "plant journeys"
        ordering = ["-created_at"]

    def __str__(self):
        suffix = f" — {self.label}" if self.label else ""
        return f"{self.plant.name}{suffix}"


class StepType(models.TextChoices):
    PLAN = "plan", "Plan"
    SEED = "seed", "Seed"
    PLANT = "plant", "Plant"
    REPOT = "repot", "Repot"
    HARVEST = "harvest", "Harvest"


class PlantJourneyStep(models.Model):
    journey = models.ForeignKey(
        PlantJourney, on_delete=models.CASCADE, related_name="steps"
    )
    step_type = models.CharField(max_length=20, choices=StepType.choices)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="steps",
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.get_step_type_display()} — {self.journey.plant.name}"
