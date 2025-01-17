from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpRequest
from rest_framework import status
from rest_framework.test import APITestCase
from fundooNotes.settings import BASE_URL
from collections.abc import Mapping, Sequence
from . import views

import unittest
import pytest

client = Client()


@pytest.mark.django_db
class test_TestUrls(unittest.TestCase):

    def test_RegistarationOnSubmit_ThenReturn_HTTP_406_NOT_ACCEPTABLE(self):
        url = BASE_URL + reverse("register")
        userData = {'username': '', 'email': '',
                    'password': '', 'confirm_password': ''}
        response = client.post(path=url, data=userData, format='json')

        self.assertEqual(response.status_code, 406)

    def test_RegistarationOnSubmit_ThenReturn_HTTP_200_OK(self):
        url = BASE_URL + reverse("register")
        userData = {'username': 'raki', 'email': 'raki@gmail.com',
                    'password': '123', 'confirm_password': '123'}
        response = client.post(path=url, data=userData, format='json')

        self.assertEqual(response.status_code, 200)

    def test_RegistarationPasswordMissMatchOnSubmit_ThenReturn_HTTP_400_BAD_REQUEST(self):
        url = BASE_URL + reverse("register")
        userData = {'username': 'raki', 'email': 'raki@gmail.com',
                    'password': '123', 'confirm_password': '1234'}
        response = client.post(path=url, data=userData, format='json')

        self.assertEqual(response.status_code, 400)
    
    def test_LoginOnSubmit_ThenReturn_HTTP_202_ACCEPTED(self):
        url = BASE_URL + reverse("login")
        userData = {'username': 'raki', 'password': '123'}
        response = client.post(path=url, data=userData, format='json')

        self.assertEqual(response.status_code, 202)

    def test_LoginOnSubmitWithWrongPassword_ThenReturn_HTTP_406_NOT_ACCEPTABLE(self):
        url = BASE_URL + reverse("login")
        userData = {'username': 'raki', 'password': '1234'}
        response = client.post(path=url, data=userData, format='json')

        self.assertEqual(response.status_code, 406)