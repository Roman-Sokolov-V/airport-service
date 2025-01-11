from django.db import transaction
from django.db.models import Count
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from airport.models import (
    AirplaneType,
    Airport,
    Country,
    City,
    Airplane,
    Route,
    Crew,
    Flight,
    Order,
    Ticket,
)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class CountryListSerializer(serializers.ModelSerializer):
    cities = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ("id", "name", "cities")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "country")


class CityListSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = City
        fields = ("name", "country")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "closest_big_city",
        )


class AirportListSerializer(serializers.ModelSerializer):
    closest_big_city = CityListSerializer(many=False, read_only=True)

    class Meta:
        model = Airport
        fields = (
            "id",
            "name",
            "closest_big_city",
        )


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )


class RouteListSerializer(serializers.ModelSerializer):
    source = AirportListSerializer(many=False, read_only=True)
    destination = AirportListSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = (
            "source",
            "destination",
            "distance",
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )


class FlightOrderSerializer(serializers.ModelSerializer):
    airplane = serializers.StringRelatedField(many=False, read_only=True)
    route = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )


class FlightListSerializer(serializers.ModelSerializer):
    airplane = serializers.StringRelatedField(many=False, read_only=True)
    route = serializers.StringRelatedField(many=False, read_only=True)
    tickets = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "tickets",
        )

    def get_tickets(self, obj):
        all_tickets = obj.airplane.rows * obj.airplane.seats_in_row
        return {
            "all_tickets": all_tickets,
            "taken_tickets": obj.num_taken_tickets,
            "available_tickets": all_tickets - obj.num_taken_tickets,
        }


class FlightDetailSerializer(serializers.ModelSerializer):
    airplane = serializers.StringRelatedField(many=False, read_only=True)
    route = serializers.StringRelatedField(many=False, read_only=True)
    crew = serializers.StringRelatedField(many=True, read_only=True)
    taken_tickets = serializers.StringRelatedField(many=True, read_only=True)
    available_tickets = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "airplane",
            "route",
            "departure_time",
            "arrival_time",
            "crew",
            "taken_tickets",
            "available_tickets",
        )

    def get_available_tickets(self, obj):
        available_tickets = []
        taken_tickets = Ticket.objects.filter(flight=obj).values_list(
            "row", "seat"
        )
        for row in range(1, obj.airplane.rows + 1):
            for seat in range(1, obj.airplane.seats_in_row + 1):
                if (row, seat) not in taken_tickets:
                    available_tickets.append(f"row: {row} seat: {seat}")
        return available_tickets


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=("row", "seat", "flight"),
            ),
        ]

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_ticket(
            row=attrs["row"],
            seat=attrs["seat"],
            rows=attrs["flight"].airplane.rows,
            seats=attrs["flight"].airplane.seats_in_row,
            error_to_rase=serializers.ValidationError,
        )
        return data


class TicketListSerializer(serializers.ModelSerializer):
    flight = FlightOrderSerializer(many=False, read_only=True)

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
                order.tickets.add(
                    Ticket.objects.create(order=order, **ticket_data)
                )
            return order
