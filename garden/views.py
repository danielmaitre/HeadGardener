import calendar
import datetime
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
from .models import GeneralArea, Plant, PlantCategory, Location, PlantJourney, PlantJourneyStep
from .forms import PlantCategoryForm, PlantJourneyStepForm


class BootstrapFormMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            widget = field.widget
            css = widget.attrs.get("class", "")
            if widget.__class__.__name__ == "Textarea":
                widget.attrs["class"] = (css + " form-control").strip()
                widget.attrs.setdefault("rows", 3)
            elif widget.__class__.__name__ in ("Select", "NullBooleanSelect"):
                widget.attrs["class"] = (css + " form-select").strip()
            elif getattr(widget, "input_type", None) == "color":
                widget.attrs["class"] = (css + " form-control form-control-color").strip()
            elif getattr(widget, "input_type", None) == "date":
                widget.attrs["class"] = (css + " form-control").strip()
            else:
                widget.attrs["class"] = (css + " form-control").strip()
        return form


# ── Plant ──────────────────────────────────────────────────────────────────────

class PlantListView(ListView):
    model = Plant
    template_name = "garden/plant_list.html"
    context_object_name = "plants"


class PlantDetailView(DetailView):
    model = Plant
    template_name = "garden/plant_detail.html"
    context_object_name = "plant"


class PlantCreateView(BootstrapFormMixin, CreateView):
    model = Plant
    template_name = "garden/plant_form.html"
    fields = ["name", "category", "notes"]
    success_url = reverse_lazy("plant-list")


class PlantUpdateView(BootstrapFormMixin, UpdateView):
    model = Plant
    template_name = "garden/plant_form.html"
    fields = ["name", "category", "notes"]

    def get_success_url(self):
        return reverse("plant-detail", kwargs={"pk": self.object.pk})


class PlantDeleteView(DeleteView):
    model = Plant
    template_name = "garden/plant_confirm_delete.html"
    success_url = reverse_lazy("plant-list")


# ── PlantJourney ───────────────────────────────────────────────────────────────

class PlantJourneyListView(ListView):
    model = PlantJourney
    template_name = "garden/journey_list.html"
    context_object_name = "journeys"
    queryset = PlantJourney.objects.select_related("plant", "plant__category").prefetch_related("steps")


class PlantJourneyDetailView(DetailView):
    model = PlantJourney
    template_name = "garden/journey_detail.html"
    context_object_name = "journey"


class PlantJourneyStandaloneCreateView(BootstrapFormMixin, CreateView):
    """Create a journey from the /journeys/new/ page — plant chosen via dropdown."""
    model = PlantJourney
    template_name = "garden/journey_form.html"
    fields = ["plant", "label", "notes"]

    def get_success_url(self):
        return reverse("journey-detail", kwargs={"pk": self.object.pk})


class PlantJourneyCreateView(BootstrapFormMixin, CreateView):
    model = PlantJourney
    template_name = "garden/journey_form.html"
    fields = ["label", "notes"]

    def form_valid(self, form):
        form.instance.plant_id = self.kwargs["plant_pk"]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["plant"] = Plant.objects.get(pk=self.kwargs["plant_pk"])
        return ctx

    def get_success_url(self):
        return reverse("journey-detail", kwargs={"pk": self.object.pk})


class PlantJourneyUpdateView(BootstrapFormMixin, UpdateView):
    model = PlantJourney
    template_name = "garden/journey_form.html"
    fields = ["label", "notes"]

    def get_success_url(self):
        return reverse("journey-detail", kwargs={"pk": self.object.pk})


class PlantJourneyDeleteView(DeleteView):
    model = PlantJourney
    template_name = "garden/journey_confirm_delete.html"

    def get_success_url(self):
        return reverse("plant-detail", kwargs={"pk": self.object.plant_id})


# ── PlantJourneyStep ───────────────────────────────────────────────────────────

class PlantJourneyStepCreateView(BootstrapFormMixin, CreateView):
    model = PlantJourneyStep
    form_class = PlantJourneyStepForm
    template_name = "garden/step_form.html"

    def form_valid(self, form):
        form.instance.journey_id = self.kwargs["journey_pk"]
        response = super().form_valid(form)
        new_step = self.object
        # Truncate any sibling step at the same location whose period contains the new start date
        if new_step.location:
            PlantJourneyStep.objects.filter(
                journey=new_step.journey,
                location=new_step.location,
                start_date__lt=new_step.start_date,
            ).filter(
                Q(end_date__gte=new_step.start_date) | Q(end_date__isnull=True)
            ).exclude(pk=new_step.pk).update(end_date=new_step.start_date)
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["journey"] = PlantJourney.objects.get(pk=self.kwargs["journey_pk"])
        return ctx

    def get_success_url(self):
        return reverse("journey-detail", kwargs={"pk": self.object.journey_id})


class PlantJourneyStepUpdateView(BootstrapFormMixin, UpdateView):
    model = PlantJourneyStep
    form_class = PlantJourneyStepForm
    template_name = "garden/step_form.html"

    def get_success_url(self):
        return reverse("journey-detail", kwargs={"pk": self.object.journey_id})


class PlantJourneyStepDeleteView(DeleteView):
    model = PlantJourneyStep
    template_name = "garden/step_confirm_delete.html"

    def get_success_url(self):
        return reverse("journey-detail", kwargs={"pk": self.object.journey_id})


# ── Location ───────────────────────────────────────────────────────────────────

class LocationListView(ListView):
    model = Location
    template_name = "garden/location_list.html"
    context_object_name = "locations"


class LocationCreateView(BootstrapFormMixin, CreateView):
    model = Location
    template_name = "garden/location_form.html"
    fields = ["name", "area", "description"]
    success_url = reverse_lazy("location-list")


class LocationUpdateView(BootstrapFormMixin, UpdateView):
    model = Location
    template_name = "garden/location_form.html"
    fields = ["name", "area", "description"]
    success_url = reverse_lazy("location-list")


# ── GeneralArea ────────────────────────────────────────────────────────────────

class GeneralAreaListView(ListView):
    model = GeneralArea
    template_name = "garden/area_list.html"
    context_object_name = "areas"


class GeneralAreaCreateView(BootstrapFormMixin, CreateView):
    model = GeneralArea
    template_name = "garden/area_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("area-list")


class GeneralAreaUpdateView(BootstrapFormMixin, UpdateView):
    model = GeneralArea
    template_name = "garden/area_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("area-list")


class AreaGanttView(DetailView):
    model = GeneralArea
    template_name = "garden/area_gantt.html"
    context_object_name = "area"

    BAR_H = 26
    BAR_GAP = 4
    ROW_PAD = 8

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        area = self.object
        today = datetime.date.today()

        try:
            year = int(self.request.GET.get("year", today.year))
        except (ValueError, TypeError):
            year = today.year

        year_start = datetime.date(year, 1, 1)
        year_end = datetime.date(year, 12, 31)
        year_days = 366 if calendar.isleap(year) else 365

        # Month header data (proportional widths + cumulative left offset)
        months, cumulative = [], 0.0
        for m in range(1, 13):
            w = calendar.monthrange(year, m)[1] / year_days * 100
            months.append({
                "name": datetime.date(year, m, 1).strftime("%b"),
                "width_pct": round(w, 4),
                "left_pct": round(cumulative, 4),
            })
            cumulative += w

        today_pct = (
            round((today - year_start).days / year_days * 100, 4)
            if year_start <= today <= year_end
            else None
        )

        rows = []
        for location in area.locations.all():
            steps = (
                PlantJourneyStep.objects
                .filter(location=location, start_date__lte=year_end)
                .filter(Q(end_date__gte=year_start) | Q(end_date__isnull=True))
                .select_related("journey__plant__category")
                .order_by("start_date")
            )

            bars = []
            for step in steps:
                s = max(step.start_date, year_start)
                e = min(step.end_date or year_end, year_end)
                if e < s:
                    continue
                left = (s - year_start).days / year_days * 100
                width = max((e - s).days + 1, 1) / year_days * 100
                bars.append({
                    "left_pct": round(left, 4),
                    "width_pct": round(width, 4),
                    "color": step.journey.plant.category.color,
                    "label": step.journey.plant.name,
                    "icon": step.icon,
                    "journey_pk": step.journey.pk,
                    "tooltip": (
                        f"{step.journey.plant.name} — {step.get_step_type_display()}"
                        f"\n{s} → {e}"
                    ),
                    "lane": 0,
                })

            # Greedy lane assignment: earliest-start first, place in first free lane
            bars.sort(key=lambda b: b["left_pct"])
            lane_ends = []
            for bar in bars:
                placed = False
                for i, end in enumerate(lane_ends):
                    if end <= bar["left_pct"]:
                        lane_ends[i] = bar["left_pct"] + bar["width_pct"]
                        bar["lane"] = i
                        placed = True
                        break
                if not placed:
                    bar["lane"] = len(lane_ends)
                    lane_ends.append(bar["left_pct"] + bar["width_pct"])

            num_lanes = max(len(lane_ends), 1)
            for bar in bars:
                bar["top_px"] = self.ROW_PAD + bar["lane"] * (self.BAR_H + self.BAR_GAP)

            rows.append({
                "location": location,
                "bars": bars,
                "height_px": self.ROW_PAD * 2 + num_lanes * self.BAR_H + (num_lanes - 1) * self.BAR_GAP,
            })

        step_years = set(
            PlantJourneyStep.objects
            .filter(location__area=area)
            .values_list("start_date__year", flat=True)
        )
        ctx.update({
            "year": year,
            "years": sorted(step_years | {today.year}),
            "months": months,
            "rows": rows,
            "today_pct": today_pct,
            "bar_h": self.BAR_H,
        })
        return ctx


# ── PlantCategory ──────────────────────────────────────────────────────────────

class PlantCategoryListView(ListView):
    model = PlantCategory
    template_name = "garden/category_list.html"
    context_object_name = "categories"


class PlantCategoryCreateView(BootstrapFormMixin, CreateView):
    model = PlantCategory
    form_class = PlantCategoryForm
    template_name = "garden/category_form.html"
    success_url = reverse_lazy("category-list")


class PlantCategoryUpdateView(BootstrapFormMixin, UpdateView):
    model = PlantCategory
    form_class = PlantCategoryForm
    template_name = "garden/category_form.html"
    success_url = reverse_lazy("category-list")
