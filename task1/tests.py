from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .views import CurrencyConversionView


class CurrencyConversionTests(APITestCase):
    def setUp(self):
        self.response = []
        self.url = reverse('api-currency')
        self.data = [
            {
                "current_currency": "GBP",
                "value": 20,
                "convert_to_currency": "UAH"
            },
            {
                "current_currency": "USD",
                "value": "20",
                "convert_to_currency": "EUR"
            },
            {
                "current_currency": "GBP",
                "value": "20m",
                "convert_to_currency": "USD"
            },
            {
                "current": "GBP",
                "value": 20,
                "convert_to_currency": "UAH"
            }
        ]

    def test_post(self):
        self.response.append(self.client.post(self.url, self.data[0], format="json"))
        self.response.append(self.client.post(self.url, self.data[1], format="json"))
        self.response.append(self.client.post(self.url, self.data[2], format="json"))
        self.response.append(self.client.post(self.url, self.data[3], format="json"))

        self.assertEqual(self.response[0].status_code, status.HTTP_200_OK)
        self.assertEqual(self.response[1].status_code, status.HTTP_200_OK)
        self.assertEqual(self.response[2].status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.response[3].status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_data(self):
        self.assertTrue(CurrencyConversionView.data_is_valid(self.data[0]))
        self.assertTrue(CurrencyConversionView.data_is_valid(self.data[1]))
        self.assertFalse(CurrencyConversionView.data_is_valid(self.data[2]))
        self.assertFalse(CurrencyConversionView.data_is_valid(self.data[3]))

    def test_get_conversion_rate(self):
        expected = [
            CurrencyConversionView.get_conversion_rate(
                self.data[i]["current_currency"], self.data[i]["convert_to_currency"]
            )
            for i in range(3)
        ]
        self.assertEqual(type(expected[0]), float)
        self.assertEqual(type(expected[1]), float)
        self.assertEqual(type(expected[2]), float)

        self.assertGreater(expected[0], 30.)
        self.assertLess(abs(1. - expected[1]), 0.5)
        self.assertGreater(expected[2], 1.)
