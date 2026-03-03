# https://www.youtube.com/watch?v=xT4SV7AH3G8
# https://www.youtube.com/watch?v=RqR0AvEujrU
# $ python3 tests.py

import unittest
from unittest.mock import patch, MagicMock

from main_add import add
from main_joke import len_joke, get_joke

from requests.exceptions import Timeout
import requests.exceptions


class AllTests(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(2,2), 4)

    @patch('main_joke.get_joke') # decorator para pacth a len_function. recebe o path do que a gente quer mockar
    def test_len_joke(self, mock_get_joke): #  mock_get_joke vai receber esse objeto patcheado
        # a função len_joke depende do site de piadas (que pode falhar), então não vamos testar esse metodo especifico considerando ele
        # e como testar a função len, se cada piada tem um tamanho diferente?
        mock_get_joke.return_value = 'piada' # retorno fake da função é 'piada'
        
        self.assertEqual(len_joke(), 5)
    
    @patch('main_joke.requests') # lib requests
    def test_get_joke(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'value': 'hello world'}
        mock_requests.get.return_value = mock_response

        result = get_joke()
        self.assertEqual(get_joke(), 'hello world')

    @patch('main_joke.requests')
    def test_get_joke_fail(self, mock_requests):
        mock_response = MagicMock(status_code = 400) # pode setar o atributo no construtor
        mock_response.json.return_value = {'value': 'hello world'}
        mock_requests.get.return_value = mock_response

        self.assertEqual(get_joke(), 'No jokes')

    @patch('main_exception.requests')
    def test_get_joke_raise_exception(self, mock_requests):
        mock_requests.exceptions = requests.exceptions # as exceções deixam de ser um mock e passam a ser reais
        mock_requests.get.side_effect = Timeout()
        
        self.assertEqual(get_joke(), 'No jokes')


if __name__ == "__main__":
    unittest.main()