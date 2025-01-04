from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from airport.models import (
    AirplanType,
    Airplan,
    Country,
    City,
    Airport,
    Route,
    Crew,
    Flight,
    Ticket,
    Order
)

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

from airport.permissions import IsAdminAllOrAuthenticatedReadOnly



class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplanType.objects.all()
    serializer_class = AirplanTypeSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return (IsAuthenticated(),)
        else:
            return (IsAdminUser(),)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplan.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)



class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)



class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)



class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)



class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)



class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)


