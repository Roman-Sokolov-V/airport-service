from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError

from airport.models import (
    AirplaneType,
    Airplane,
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
    AirplaneTypeSerializer,
    AirportSerializer,
    AirplaneSerializer,
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    CrewSerializer,
    FlightSerializer,
    TicketSerializer,
    OrderListSerializer,
    OrderCreateSerializer,
    RouteListSerializer,
    AirportListSerializer,
    CityListSerializer,
    AirplaneListSerializer,
    CountryListSerializer, FlightListSerializer, FlightDetailSerializer,
)

from airport.permissions import IsAdminAllOrAuthenticatedReadOnly



class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return (IsAuthenticated(),)
        else:
            return (IsAdminUser(),)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListSerializer
        return self.serializer_class


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CountryListSerializer
        return self.serializer_class


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CityListSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)



class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all().select_related("closest_big_city__country")
    serializer_class = AirportListSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)


    def get_queryset(self):
        queryset = self.queryset
        country = self.request.query_params.get("country")
        city = self.request.query_params.get("city")
        if country:
            queryset = queryset.filter(
                closest_big_city__country__name__iexact=country
            )
        if city:
            queryset = queryset.filter(
                closest_big_city__name__iexact=city
            )

        return queryset


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().prefetch_related(
        "source__closest_big_city__country", "destination__closest_big_city__country")
    serializer_class = RouteSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RouteListSerializer
        return self.serializer_class

    @staticmethod
    def split_params(params):
        return params.split("-")

    def get_queryset(self):
        queryset = self.queryset
        for param in self.request.query_params:
            if param not in ["countries", "cities", "airports"]:
                continue
            try:
                route = self.split_params(self.request.query_params[param])
                if len(route) != 2:
                    raise ValidationError(
                        {
                            param: f"Parameter {param} must contain "
                                   f"exactly two values separated by a '-'."
                        }
                    )
                source, destination = route
                source, destination = source.strip(), destination.strip()
                if param == "cities":
                    queryset = queryset.filter(
                        source__closest_big_city__name__iexact=source,
                        destination__closest_big_city__name__iexact=destination
                    )
                elif param == "countries":
                    queryset = queryset.filter(
                        source__closest_big_city__country__name__iexact=source,
                        destination__closest_big_city__country__name__iexact=destination
                    )
                elif param == "airports":
                    queryset = queryset.filter(
                        source__id=int(source),
                        destination__id=int(destination)
                    )
            except ValueError:
                raise ValidationError(
                    {"airports": "Parameter 'airports' must contain valid integers."}
                )
            except Exception as e:
                raise ValidationError({param: str(e)})

        return queryset



class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)



class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
       "airplane", "route__source", "route__destination"
    ).prefetch_related("crew", "taken_tickets",)
    serializer_class = FlightSerializer
    permission_classes = (IsAdminAllOrAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action=="retrieve":
            return FlightDetailSerializer
        return self.serializer_class

    @staticmethod
    def split_params(params):
        return params.split("-")

    def get_queryset(self):
        queryset = self.queryset
        for param in self.request.query_params:
            if param not in ["countries", "cities", "airports"]:
                continue
            try:
                route = self.split_params(self.request.query_params[param])
                if len(route) != 2:
                    raise ValidationError(
                        {
                            param: f"Parameter {param} must contain "
                                   f"exactly two values separated by a '-'."
                        }
                    )
                source, destination = route
                source, destination = source.strip(), destination.strip()
                if param == "cities":
                    queryset = queryset.filter(
                        route__source__closest_big_city__name__iexact=source,
                        route__destination__closest_big_city__name__iexact
                        =destination
                    )
                elif param == "countries":
                    queryset = queryset.filter(
                        route__source__closest_big_city__country__name__iexact
                        =source,
                        route_destination__closest_big_city__country__name__iexact=destination
                    )
                elif param == "airports":
                    queryset = queryset.filter(
                        route__source__id=int(source),
                        route__destination__id=int(destination)
                    )
            except ValueError:
                raise ValidationError(
                    {
                        "airports": "Parameter 'airports' must contain valid integers."}
                )
            except Exception as e:
                raise ValidationError({param: str(e)})

        return queryset



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related(
    "tickets__flight__route__source",
        "tickets__flight__route__destination",
        "tickets__flight__airplane",

)
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderListSerializer
        elif self.action == "create":
            return OrderCreateSerializer
