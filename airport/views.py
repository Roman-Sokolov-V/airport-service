from django.db.models import Count, F, Value
from django.db.models.functions import Concat

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

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
    Order,
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
    CountryListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    """Endpoint for airplane types"""

    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    """Endpoint for airplanes"""

    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListSerializer
        return self.serializer_class


class CountryViewSet(viewsets.ModelViewSet):
    """Endpoint for countries"""

    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CountryListSerializer
        return self.serializer_class


class CityViewSet(viewsets.ModelViewSet):
    """Endpoint for cities"""

    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CityListSerializer
        return self.serializer_class


class AirportViewSet(viewsets.ModelViewSet):
    """Endpoint for airports"""

    queryset = Airport.objects.all().select_related("closest_big_city__country")
    serializer_class = AirportSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirportListSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        country = self.request.query_params.get("country")
        city = self.request.query_params.get("city")
        if country:
            queryset = queryset.filter(
                closest_big_city__country__name__icontains=country
            )
        if city:
            queryset = queryset.filter(closest_big_city__name__icontains=city)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="location",
                type=OpenApiTypes.STR,
                description="Filter by city or/and country ("
                "example/?city=paris&country=france)",
            )
        ]
    )
    def list(self, request):
        """Get list of all Airports."""
        return super().list(request, *self.args, **self.kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    """Endpoint for routes"""

    queryset = Route.objects.all().prefetch_related(
        "source__closest_big_city__country", "destination__closest_big_city__country"
    )
    serializer_class = RouteSerializer

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
                        source__closest_big_city__name__icontains=source,
                        destination__closest_big_city__name__icontains=destination,
                    )
                elif param == "countries":
                    queryset = queryset.filter(
                        source__closest_big_city__country__name__icontains=source,
                        destination__closest_big_city__country__name__icontains=destination,
                    )
                elif param == "airports":
                    queryset = queryset.filter(
                        source__id=int(source), destination__id=int(destination)
                    )
            except ValueError:
                raise ValidationError(
                    {"airports": "Parameter 'airports' must contain valid integers."}
                )
            except Exception as e:
                raise ValidationError({param: str(e)})

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source-destination",
                type=OpenApiTypes.STR,
                description="Filter by route, city-city or country-country "
                "or id_airport-id_airport("
                "example_1/?cities=paris-london "
                "example_2/?countries=france-ukraine"
                "example_3/?airports=1-5)",
            )
        ]
    )
    def list(self, request):
        """Get list of routs."""
        return super().list(request, *self.args, **self.kwargs)


class CrewViewSet(viewsets.ModelViewSet):
    """Endpoint for crews"""

    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    """Endpoint for flights"""

    queryset = (
        Flight.objects.select_related("airplane", "route")
        .prefetch_related(
            "crew",
            "taken_tickets",
        )
        .annotate(num_taken_tickets=Count("taken_tickets"))
    )

    serializer_class = FlightSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
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
                        route__source__closest_big_city__name__icontains
                        =source,
                        route__destination__closest_big_city__name__icontains
                        =destination,
                    )
                elif param == "countries":
                    queryset = queryset.filter(
                        route__source__closest_big_city__country__name__icontains=source,
                        route__destination__closest_big_city__country__name__icontains=destination,
                    )
                elif param == "airports":
                    queryset = queryset.filter(
                        route__source__id=int(source),
                        route__destination__id=int(destination),
                    )
            except ValueError:
                raise ValidationError(
                    {"airports": "Parameter 'airports' must contain valid integers."}
                )
            except Exception as e:
                raise ValidationError({param: str(e)})

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source-destination",
                type=OpenApiTypes.STR,
                description="Filter by route, city-city or country-country "
                "or id_airport-id_airport("
                "example_1/?cities=paris-london "
                "example_2/?countries=france-ukraine"
                "example_3/?airports=1-5)",
            )
        ]
    )
    def list(self, request):
        """Get list of flights."""
        return super().list(request, *self.args, **self.kwargs)


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Endpoint for orders"""

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
