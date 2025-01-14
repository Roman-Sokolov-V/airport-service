from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.models import Count

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse

from airport.models import (
    AirplaneType,
    Airplane,
    Country,
    City,
    Airport,
    Route,
    Crew,
    Ticket,
    Flight,
    Order,
)
from airport.serializers import (
    AirplaneTypeSerializer,
    AirplaneListSerializer,
    CountryListSerializer,
    CityListSerializer,
    AirportListSerializer,
    RouteListSerializer,
    CrewSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    OrderListSerializer,
    OrderListSerializer,
    OrderCreateSerializer,
)

BASE_URL = reverse("airport:api-root")


def create_auth_user():
    return get_user_model().objects.create_user(
        email="<EMAIL>",
        password="<PASSWORD>",
        first_name="Test",
        last_name="User",
    )


def sample_airplane_type(**params) -> AirplaneType:
    defaults = {"name": "small airplane"}
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params) -> Airplane:
    airplane_type = sample_airplane_type()
    defaults = {
        "name": "Dream",
        "rows": 20,
        "seats_in_row": 4,
        "airplane_type": airplane_type,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_country(name: str = "New Zealand") -> Country:
    return Country.objects.create(name=name)


def sample_city(name: str = "Kharkiv", **params) -> City:
    defaults = {"country": sample_country()}
    defaults.update(params)
    return City.objects.create(name=name, **defaults)


def sample_airport(**params) -> Airport:
    defaults = {"name": "Airport_1", "closest_big_city": sample_city()}
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route() -> Route:
    country = Country.objects.create(name="USA")
    country2 = Country.objects.create(name="Ukraine")
    city1 = City.objects.create(name="New York", country=country)
    city2 = City.objects.create(name="Fargo", country=country)
    city3 = City.objects.create(name="Harkiv", country=country2)
    city4 = City.objects.create(name="Lviv", country=country2)
    airport1 = Airport.objects.create(name="NYA", closest_big_city=city1)
    airport2 = Airport.objects.create(name="FA", closest_big_city=city2)
    airport3 = Airport.objects.create(name="HA", closest_big_city=city3)
    airport4 = Airport.objects.create(name="LVA", closest_big_city=city4)
    route = Route.objects.create(
        source=airport1, destination=airport2, distance=1000
    )
    Route.objects.create(source=airport2, destination=airport3, distance=1000)
    Route.objects.create(source=airport3, destination=airport4, distance=1000)
    Route.objects.create(source=airport4, destination=airport1, distance=1000)
    return route


def sample_crew(**params) -> Crew:
    defaults = {
        "first_name": "Jhon",
        "last_name": "Dow",
        "position": "captain",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_flight(**params) -> Flight:
    defaults = {
        "departure_time": datetime(2025, 1, 15, 9, 30),
        "arrival_time": datetime(2025, 1, 15, 12, 45),
    }
    defaults.update(params)
    crew = sample_crew()
    flight = Flight.objects.create(
        route=sample_route(), airplane=sample_airplane(), **defaults
    )
    flight.crew.add(crew)
    Flight.objects.create(
        route=Route.objects.get(pk=2),
        airplane=Airplane.objects.get(pk=1),
        **defaults,
    )
    Flight.objects.create(
        route=Route.objects.get(pk=3),
        airplane=Airplane.objects.get(pk=1),
        **defaults,
    )
    return flight


class AirplaneTypeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.client.force_authenticate(self.user)
        self.airplan_type = sample_airplane_type()

    def test_list_airplane_type(self):
        response = self.client.get(BASE_URL + "airplane-type/")
        airplane_types = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_types, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_airplane_type(self):
        data = {"name": "big airplane"}
        response = self.client.post(BASE_URL + "airplane-type/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_airplane_type(self):
        response = self.client.get(BASE_URL + "airplane-type/1/")
        airplane_type = AirplaneType.objects.get(id=1)
        serializer = AirplaneTypeSerializer(airplane_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_airplane_type(self):
        data = {"name": "big airplane"}
        response = self.client.put(BASE_URL + "airplane-type/1/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_putch_airplane_type(self):
        data = {"name": "big airplane"}
        response = self.client.patch(BASE_URL + "airplane-type/1/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


############################################################
class AirplaneTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.client.force_authenticate(self.user)
        self.airplane = sample_airplane()

    def test_list_airplane(self):
        response = self.client.get(BASE_URL + "airplane/")
        airplanes = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplanes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_airplane(self):
        data = {
            "name": "New plane",
            "rows": 20,
            "seats_in_row": 4,
            "airplane_type": 1,
        }
        response = self.client.post(BASE_URL + "airplane/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_airplane(self):
        response = self.client.get(BASE_URL + "airplane/1/")
        serializer = AirplaneListSerializer(self.airplane)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_airplane(self):
        data = {
            "name": "New plane",
            "rows": 20,
            "seats_in_row": 4,
            "airplane_type": 1,
        }
        response = self.client.put(BASE_URL + "airplane/1/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_putch_airplane(self):
        data = {"name": "big airplane"}
        response = self.client.patch(BASE_URL + "airplane/1/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CountryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.client.force_authenticate(self.user)
        self.country = sample_country()
        self.list_url = reverse("airport:country-list")
        self.detail_url = reverse(
            "airport:country-detail", kwargs={"pk": self.country.pk}
        )

    def test_list_countries(self):
        response = self.client.get(self.list_url)
        countries = Country.objects.all()
        serializer = CountryListSerializer(countries, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_country(self):
        data = {"name": "United country of Eirth"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_country(self):
        response = self.client.get(self.detail_url)
        serializer = CountryListSerializer(self.country)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_country(self):
        data = {"name": "New"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_putch_country(self):
        data = {"name": "Best"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.client.force_authenticate(self.user)
        self.city = sample_city()
        self.country = Country.objects.get(cities=self.city)
        self.list_url = reverse("airport:city-list")
        self.detail_url = reverse(
            "airport:city-detail", kwargs={"pk": self.city.pk}
        )

    def test_list_cities(self):
        response = self.client.get(self.list_url)
        cities = City.objects.all()
        serializer = CityListSerializer(cities, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_city(self):
        data = {"name": "Just city", "country": self.country.id}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_city(self):
        response = self.client.get(self.detail_url)
        serializer = CityListSerializer(self.city)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_country(self):
        data = {"name": "Just city", "country": self.country.id}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_putch_country(self):
        data = {"name": "UUUS"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AirportTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.client.force_authenticate(self.user)
        self.airport = sample_airport()
        self.city = City.objects.get(airports=self.airport)
        self.list_url = reverse("airport:airport-list")
        self.detail_url = reverse(
            "airport:airport-detail", kwargs={"pk": self.airport.pk}
        )

    def test_list_airports(self):
        response = self.client.get(self.list_url)
        airports = Airport.objects.all()
        serializer = AirportListSerializer(airports, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_airport(self):
        data = {"name": "UWR", "closest_big_city": self.city.pk}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_airport(self):
        response = self.client.get(self.detail_url)
        serializer = AirportListSerializer(self.airport)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_airport(self):
        data = {"name": "UWR", "closest_big_city": self.city.pk}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_putch_airport(self):
        data = {"name": "RED"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RouteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.client.force_authenticate(self.user)
        self.route = sample_route()
        self.list_url = reverse("airport:route-list")
        self.detail_url = reverse(
            "airport:route-detail", kwargs={"pk": self.route.pk}
        )

    def test_list_routs(self):
        response = self.client.get(self.list_url)
        routs = Route.objects.all()
        serializer = RouteListSerializer(routs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_routs_filtred(self):
        response = self.client.get(self.list_url + "?countries=us-uk")
        routs = Route.objects.filter(
            source__closest_big_city__country__name__icontains="us",
            destination__closest_big_city__country__name__icontains="uk",
        )
        serializer = RouteListSerializer(routs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

        response = self.client.get(self.list_url + "?cities=fa-ha")
        routs = Route.objects.filter(
            source__closest_big_city__name__icontains="fa",
            destination__closest_big_city__name__icontains="ha",
        )
        serializer = RouteListSerializer(routs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

        response = self.client.get(self.list_url + "?airports=1-2")
        routs = Route.objects.filter(source__id=1, destination__id=2)
        serializer = RouteListSerializer(routs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_route(self):
        data = {"source": 2, "destination": 1, "distance": 2000}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_route(self):
        response = self.client.get(self.detail_url)
        serializer = RouteListSerializer(self.route)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_route(self):
        data = {"source": 2, "destination": 3, "distance": 2000}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_putch_route(self):
        data = {"distance": 2000}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CrewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.client.force_authenticate(self.user)
        self.crew = sample_crew()
        self.list_url = reverse("airport:crew-list")
        self.detail_url = reverse(
            "airport:crew-detail", kwargs={"pk": self.crew.pk}
        )

    def test_list_crew(self):
        response = self.client.get(self.list_url)
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_crew(self):
        data = {
            "first_name": "Jaine",
            "last_name": "Dow",
            "position": "first officer",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_crew(self):
        response = self.client.get(self.detail_url)
        serializer = CrewSerializer(self.crew)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_crew(self):
        data = {
            "first_name": "Jaine",
            "last_name": "Dow",
            "position": "first officer",
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_putch_crew(self):
        data = {"position": "first officer"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FlightTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.client.force_authenticate(self.user)
        self.flight = sample_flight()
        self.list_url = reverse("airport:flight-list")
        self.detail_url = reverse(
            "airport:flight-detail", kwargs={"pk": self.flight.pk}
        )

    def test_list_flights(self):
        response = self.client.get(self.list_url)
        flights = Flight.objects.all().annotate(
            num_taken_tickets=Count("taken_tickets")
        )
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_flights_filtred(self):
        response = self.client.get(self.list_url + "?countries=us-uk")
        flights = Flight.objects.filter(
            route__source__closest_big_city__country__name__icontains="us",
            route__destination__closest_big_city__country__name__icontains="uk",
        ).annotate(num_taken_tickets=Count("taken_tickets"))
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

        response = self.client.get(self.list_url + "?airports=1-2")
        flights = Flight.objects.filter(
            route__source__id=1, route__destination__id=2
        ).annotate(num_taken_tickets=Count("taken_tickets"))
        serializer = FlightListSerializer(flights, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_flights(self):
        data = {
            "route": 1,
            "airplane": 1,
            "departure_time": datetime(2025, 1, 15, 9, 30),
            "arrival_time": datetime(2025, 1, 15, 12, 45),
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrive_flight(self):
        response = self.client.get(self.detail_url)
        serializer = FlightDetailSerializer(self.flight)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_flight(self):
        data = {
            "route": 1,
            "airplane": 1,
            "departure_time": datetime(2025, 1, 15, 9, 30),
            "arrival_time": datetime(2025, 1, 15, 12, 45),
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_putch_flight(self):
        data = {"arrival_time": datetime.now()}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_auth_user()
        self.another_user = get_user_model().objects.create_user(
            email="<EMAIL2>",
            password="<PASSWORD2>",
            first_name="Test2",
            last_name="User2",
        )
        self.client.force_authenticate(self.user)
        self.flight = sample_flight()
        self.order = Order.objects.create(user=self.user)
        self.another_order = Order.objects.create(user=self.another_user)
        self.list_url = reverse("airport:order-list")
        self.detail_url = reverse(
            "airport:order-detail", kwargs={"pk": self.order.pk}
        )

    def test_list_order(self):
        response = self.client.get(self.list_url)
        order = Order.objects.all().filter(user=self.user)
        serializer = OrderListSerializer(order, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_post_order(self):
        data = {
            "tickets": [
                {"row": 1, "seat": 1, "flight": self.flight.id},
                {"row": 1, "seat": 2, "flight": self.flight.id},
            ]
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), len(data["tickets"]))

        data = {"tickets": [{"row": 1, "seat": 1, "flight": self.flight.id}]}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["tickets"][0]["row"] = self.flight.airplane.rows + 1
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["tickets"][0]["row"] = -1
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["tickets"][0]["row"] = 1
        data["tickets"][0]["seat"] = -1
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["tickets"][0]["seat"] = self.flight.airplane.seats_in_row + 1
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["tickets"] = []
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_order(self):
        response = self.client.get(self.detail_url)
        serializer = OrderListSerializer(self.order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_put_order(self):
        data = {"tickets": [{"row": 1, "seat": 1, "flight": self.flight.id}]}
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_putch_order(self):
        data = {"tickets": [{"row": 1, "seat": 1, "flight": self.flight.id}]}
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
