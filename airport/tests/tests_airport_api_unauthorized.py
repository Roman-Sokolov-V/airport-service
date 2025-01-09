from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse

BASE_URL = reverse("airport:api-root")

class UnauthenticatedTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_airplan_type_view(self):
        response = self.client.get(BASE_URL + "airplane-type/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airplan_view(self):
        response = self.client.get(BASE_URL + "airplane/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_country_view(self):
        response = self.client.get(BASE_URL + "country/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_city_view(self):
        response = self.client.get(BASE_URL + "city/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_view(self):
        response = self.client.get(BASE_URL + "airport/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rout_view(self):
        response = self.client.get(BASE_URL + "route/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_view(self):
        response = self.client.get(BASE_URL + "crew/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_view(self):
        response = self.client.get(BASE_URL + "flight/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_view(self):
        response = self.client.get(BASE_URL + "order/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_airplan_type_detail_view(self):
        response = self.client.get(BASE_URL + "airplane-type/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airpla_detail_view(self):
        response = self.client.get(BASE_URL + "airplane/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_country_detail_view(self):
        response = self.client.get(BASE_URL + "country/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_city_detail_view(self):
        response = self.client.get(BASE_URL + "city/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_detail_view(self):
        response = self.client.get(BASE_URL + "airport/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rout_detail_view(self):
        response = self.client.get(BASE_URL + "route/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crew_detail_view(self):
        response = self.client.get(BASE_URL + "crew/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_detail_view(self):
        response = self.client.get(BASE_URL + "flight/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_detail_view(self):
        response = self.client.get(BASE_URL + "order/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)