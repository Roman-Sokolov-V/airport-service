from django.db import transaction
from rest_framework import serializers

from airport.models import *


class AirplanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplanType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplan
        fields = ("id", "name", "rows", "seats_in_row", "airplan_type")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name",)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityListSerializer(serializers.ModelSerializer):
    country = CountryListSerializer(many=False, read_only=True)

    class Meta:
        model = City
        fields = ("name", "country")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city",)


class AirportListSerializer(serializers.ModelSerializer):
    closest_big_city = CityListSerializer(many=False, read_only=True)

    class Meta:
        model = Airport
        fields = ("name", "closest_big_city",)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance",)

class RouteListSerializer(serializers.ModelSerializer):
    source = AirportListSerializer(many=False, read_only=True)
    destination = AirportListSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = ("source", "destination", "distance",)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplan", "departure_time", "arrival_time",)

class FlightListSerializer(serializers.ModelSerializer):
    airplan = AirplaneSerializer(many=False, read_only=True)
    route = RouteListSerializer(many=False, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplan", "departure_time", "arrival_time",)



class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

class TicketListSerializer(serializers.ModelSerializer):
    flight = FlightListSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")

class OrderListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ("id", "created", "tickets")


class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)


    class Meta:
        model = Order
        fields = ("id", "created", "tickets")



    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                order.tickets.add(Ticket.objects.create(order=order, **ticket_data))
            return order

