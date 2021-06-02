
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from apps.users.api.views import UserViewSet

from .factories import UserFactory

User = get_user_model()


class TestUserViewSet(TestCase):
    def setUp(self):
        self.rf: RequestFactory = RequestFactory()
        self.user: User = UserFactory()

    def test_get_queryset(self):
        view = UserViewSet()
        request = self.rf.get("/fake-url/")
        request.user = self.user

        view.request = request

        self.assertIn(self.user, view.get_queryset())

    def test_me(self):
        view = UserViewSet()
        request = self.rf.get("/fake-url/")
        request.user = self.user

        view.request = request

        response = view.me(request)

        expected_response = {
            "id": str(self.user.id),
            "email": self.user.email,
            "url": f"http://testserver/api/users/{self.user.id}/",
        }

        self.assertEqual(response.data, expected_response)
