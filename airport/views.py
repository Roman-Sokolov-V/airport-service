from airport.models import AirplanType, Airplan, Country, City, Airport, Route, \
    Crew, Flight, Ticket, Order
from django.shortcuts import render

from airport.serializers import (
    AirplanTypeSerializer,
    AirportSerializer,
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    CrewSerializer,
    FlightSerializer,
    TicketSerializer,
    OrderSerializer,
    TicketSerializer,
    AirplaneSerializer,
)
from rest_framework import viewsets


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplanType.objects.all()
    serializer_class = AirplanTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplan.objects.all()
    serializer_class = AirplaneSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
