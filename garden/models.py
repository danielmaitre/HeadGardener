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


class PlantImage(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="plants/")
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["uploaded_at"]


class AnnualTask(models.Model):
    PERIOD_CHOICES = [
        (1,  "Early Spring"),
        (2,  "Mid Spring"),
        (3,  "Late Spring"),
        (4,  "Early Summer"),
        (5,  "Mid Summer"),
        (6,  "Late Summer"),
        (7,  "Early Autumn"),
        (8,  "Mid Autumn"),
        (9,  "Late Autumn"),
        (10, "Early Winter"),
        (11, "Mid Winter"),
        (12, "Late Winter"),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="annual_tasks")
    period = models.PositiveSmallIntegerField(choices=PERIOD_CHOICES)
    task = models.CharField(max_length=200)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["period"]

    def __str__(self):
        return f"{self.get_period_display()} — {self.task}"


class AnnualTaskCompletion(models.Model):
    task = models.ForeignKey(AnnualTask, on_delete=models.CASCADE, related_name="completions")
    year = models.PositiveSmallIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("task", "year")]


class PlantJourney(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="journeys")
    label = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "plant journeys"
        ordering = ["-created_at"]

    @property
    def display_label(self):
        if self.label:
            return self.label
        from django.db.models import Min, Max
        agg = self.steps.aggregate(first=Min("start_date"), last=Max("end_date"))
        first, last = agg["first"], agg["last"]
        if first is None:
            return "No steps yet"
        fmt_first = first.strftime("%-d %b %Y") if first.year != (last.year if last else first.year) else first.strftime("%-d %b")
        fmt_last = last.strftime("%-d %b %Y") if last else None
        return f"{fmt_first} → {fmt_last}" if fmt_last else f"{fmt_first} →"

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

    _ICONS = {
        "plan":    "fa-solid fa-clipboard-list",
        "seed":    "fa-solid fa-seedling",
        "plant":   "fa-solid fa-leaf",
        "repot":   "fa-solid fa-arrows-rotate",
        "harvest": "fa-solid fa-wheat-awn",
    }

    @property
    def icon(self):
        return self._ICONS.get(self.step_type, "fa-solid fa-circle")

    def __str__(self):
        return f"{self.get_step_type_display()} — {self.journey.plant.name}"
