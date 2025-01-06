from django.urls import path, include

from rest_framework.routers import DefaultRouter

from airport.views import (
    AirplaneTypeViewSet,
    AirportViewSet,
    AirplaneViewSet,
    CountryViewSet,
    CityViewSet,
    RouteViewSet,
    CrewViewSet,
    FlightViewSet,
    OrderViewSet,
    # TicketViewSet
)

app_name = "airport"

router = DefaultRouter()
router.register(r"airplane-type", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("country", CountryViewSet)
router.register("city", CityViewSet)
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)
router.register("crew", CrewViewSet)
router.register("flight", FlightViewSet)
router.register("order", OrderViewSet)
# router.register(r"ticket", TicketViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
