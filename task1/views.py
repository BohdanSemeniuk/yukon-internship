from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

CURRENCY: list[str] = ['EUR', 'USD', 'GBP', 'UAH']
URL: str = 'https://api.exchangerate.host/convert'
INPUT_LIST_KEYS: list = ['current_currency', 'value', 'convert_to_currency']


class CurrencyConversionView(APIView):
    def get(self, request):
        VALUE = 25
        conv_rate = self.get_conversion_rate('USD', 'UAH')
        data = {
            'example': {
                'input': {
                    'current_currency': 'USD',
                    'value': VALUE,
                    'convert_to_currency': 'UAH'
                },
                'output': {
                    'currency': 'UAH',
                    'value': conv_rate * VALUE,
                    'conversion_rate': conv_rate
                }
            }
        }
        return Response(data)

    def post(self, request):
        if not self.data_is_valid(request.data):
            return Response({'Error': 'Incorrect input data'}, status=status.HTTP_400_BAD_REQUEST)

        conversion_rate: float = self.get_conversion_rate(request.data['current_currency'],
                                                          request.data['convert_to_currency'])
        converted_value: float = float(request.data['value']) * conversion_rate
        return Response({'currency': request.data['convert_to_currency'], 'value': converted_value,
                         'conversion_rate': conversion_rate})

    @staticmethod
    def get_conversion_rate(convert_from: str, convert_to: str) -> float:
        """"
        :param str convert_from: Currency to be converted
        :param str convert_to: Currency to which it is converted
        """
        response = requests.get(URL, params={
            'from': convert_from,
            'to': convert_to,
        })
        conversion_rate = response.json()['info']['rate']

        if conversion_rate <= 0:
            raise Exception('Conversion rate can not be less or equal zero')

        return conversion_rate

    @staticmethod
    def data_is_valid(data: dict) -> bool:
        """"
        checks if the data is entered correctly
        :param dict data: Should include currency to be converted, the amount of currency to be converted and
        currency to be converted to
        :return: true if the data is correct, otherwise false
        """
        if list(data.keys()) != INPUT_LIST_KEYS:
            return False

        if data['current_currency'] not in CURRENCY or data['convert_to_currency'] not in CURRENCY:
            return False

        if type(data['value']) != float or type(data['value']) != int:
            try:
                float(data['value'])
            except ValueError or TypeError:
                return False

        return True
