from django.db import models
from django.db.models import ForeignKey

from service_config import settings


class AirplanType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Airplan(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplan_type = models.ForeignKey(
        AirplanType, on_delete=models.CASCADE, related_name="airplanes"
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
        City, on_delete=models.CASCADE,
        related_name="airports"
    )

    class Meta:
        unique_together = ("name", "closest_big_city")

    def __str__(self):
        return (
            f"{self.name}/{self.closest_big_city.name}/"
                f"{self.closest_big_city.country}"
        )

class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="routes_from"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="routes_to"
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"From {self.source} to {self.destination}"

class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.position} - {self.first_name} {self.last_name}"

class Flight(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights"
    )
    airplan = models.ForeignKey(
        Airplan, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "flight")
