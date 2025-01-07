from django.db import models
from django.db.models import ForeignKey

from service_config import settings


class AirplaneType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = ForeignKey(
        City, on_delete=models.CASCADE, related_name="airports"
    )

    class Meta:
        unique_together = ("name", "closest_big_city")

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="routes_from"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="routes_to"
    )
    distance = models.IntegerField()
    route_description = models.CharField(max_length=255, blank=True)

    # def __str__(self):
    #     return f"From {self.source.name} to {self.destination.name}"

    def save(self, *args, **kwargs):
        self.route_description = (
            f"From {self.source.name} ({self.source.closest_big_city.name} / "
            f"{self.source.closest_big_city.country.name})"
            f" to {self.destination.name} ({self.destination.closest_big_city.name}"
            f" / {self.destination.closest_big_city.country.name})"
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.route_description


class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.position} - {self.first_name} {self.last_name}"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew)


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="taken_tickets"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return f"row:{self.row} seat:{self.seat}"

    class Meta:
        unique_together = ("row", "seat", "flight")

    @staticmethod
    def validate_ticket(row: int, rows: int, seat: int, seats: int, error_to_rase):
        if not (1 <= row <= rows):
            raise error_to_rase({"row": f"row must be in range [1, {rows}]"})
        if not (1 <= seat <= seats):
            raise error_to_rase({"seat": f"seat must be in range " f"[1, {seats}]"})

    def clean(self):
        validate_ticket(
            row=self.row,
            rows=self.flight.airplane.rows,
            seat=self.seat,
            seats=self.flight.airplane.seats_in_row,
            error_to_rase=ValueError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
