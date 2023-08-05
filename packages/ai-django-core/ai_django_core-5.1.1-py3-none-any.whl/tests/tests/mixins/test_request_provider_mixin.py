from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpRequest
from django.test import TestCase

from ai_django_core.tests.mixins import RequestProviderMixin


class RequestProviderMixinTest(RequestProviderMixin, TestCase):

    def test_request_is_request(self):
        request = self.get_request(None)
        self.assertIsInstance(request, HttpRequest)

    def test_request_user_set(self):
        user = User.objects.create(username='albertus_magnus')
        request = self.get_request(user)
        self.assertEqual(request.user, user)

    def test_request_user_is_none_working(self):
        request = self.get_request(None)
        self.assertEqual(request.user, None)

    def test_django_messages_set_up_correctly(self):
        request = self.get_request(None)

        # This would fail if the django messages were not set up correctly
        messages.add_message(request, messages.SUCCESS, 'I am a great message!')

        self.assertIsInstance(request.session, SessionBase)

    def test_django_session_set_up_correctly(self):
        request = self.get_request(None)
        request.session['my_val'] = 27
        request.session.modified = True

        self.assertEqual(request.session['my_val'], 27)
