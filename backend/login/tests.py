from unittest.mock import patch, MagicMock
from rest_framework.response import Response
from rest_framework.request import Request
from django.test import SimpleTestCase, TestCase, RequestFactory
from .use_case import LoginUseCase
from .views import LoginView
from .abstract_use_case import AbstractLoginUseCase


class MatchEmailToIdTests(SimpleTestCase):
    def test_match_existing_email(self):
        """
        Test that an email in the email_to_user_id dictionary returns the correct user ID.
        """
        login_use_case = LoginUseCase()
        email = "liuyimeng01@gmail.com"
        expected_user_id = "21"
        self.assertEqual(login_use_case.match_email_to_id(email), expected_user_id)

    def test_match_non_existing_email(self):
        """
        Test that an email not in the email_to_user_id dictionary returns a random ID.
        """
        login_use_case = LoginUseCase()
        email = "nonexistentemail@gmail.com"
        with patch("login.use_case.randint") as mock_randint:
            mock_randint.return_value = 42  # Mock randint to return a predictable value
            user_id = login_use_case.match_email_to_id(email)
            self.assertEqual(user_id, "42")
            mock_randint.assert_called_once_with(0, 99)

    def test_match_multiple_existing_emails(self):
        """
        Test multiple emails that exist in the email_to_user_id dictionary.
        """
        login_use_case = LoginUseCase()
        test_cases = {
            "gabrielezrathompson@gmail.com": "1",
            "chongwan.w@gmail.com": "4",
            "jennifer.r.chiou@gmail.com": "95",
        }
        for email, expected_user_id in test_cases.items():
            with self.subTest(email=email):
                self.assertEqual(
                    login_use_case.match_email_to_id(email), expected_user_id
                )

    def test_match_edge_case_empty_email(self):
        """
        Test edge case where the email is an empty string.
        """
        login_use_case = LoginUseCase()
        email = ""
        with patch("login.use_case.randint") as mock_randint:
            mock_randint.return_value = 99
            user_id = login_use_case.match_email_to_id(email)
            self.assertEqual(user_id, "99")
            mock_randint.assert_called_once_with(0, 99)

    def test_match_case_sensitivity(self):
        """
        Test that the function is case-sensitive.
        """
        login_use_case = LoginUseCase()
        email = "Liuyimeng01@gmail.com"
        with patch("login.use_case.randint") as mock_randint:
            mock_randint.return_value = 57
            user_id = login_use_case.match_email_to_id(email)
            self.assertEqual(
                user_id, "57"
            )  # Should not match existing email due to case sensitivity
            mock_randint.assert_called_once_with(0, 99)


class GetUserEmailFromFrontendTests(TestCase):
    def setUp(self):
        self.mock_use_case = MagicMock(spec=AbstractLoginUseCase)
        self.view = LoginView(self.mock_use_case)
        self.factory = RequestFactory()

    def test_existing_email_directly(self):
        """
        Test the logic inside the view directly with an existing email.
        """
        email = {"email": "liuyimeng01@gmail.com"}
        django_request = self.factory.post("/login/get_email/", data=email, content_type="application/json")
        
        # Wrap Django's request with DRF's Request
        request = Request(django_request)

        self.mock_use_case.match_email_to_id.return_value = "21"

        # Call the class method directly
        response = self.view.get_user_email_from_frontend(request)

        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": f"Got user's email {email}", "data": "21"})
        self.mock_use_case.match_email_to_id.assert_called_once_with(email)

    def test_non_existing_email_directly(self):
        """
        Test the logic inside the view directly with a non-existing email.
        """
        email = {"email": "nonexistentemail@gmail.com"}
        django_request = self.factory.post("/login/get_email/", data=email, content_type="application/json")
        
        # Wrap Django's request with DRF's Request
        request = Request(django_request)

        self.mock_use_case.match_email_to_id.return_value = "42"

        # Call the class method directly
        response = self.view.get_user_email_from_frontend(request)

        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": f"Got user's email {email}", "data": "42"})
        self.mock_use_case.match_email_to_id.assert_called_once_with(email)

    def test_invalid_request_method_directly(self):
        """
        Test the logic inside the view directly with an invalid request method.
        """
        django_request = self.factory.get("/login/get_email/")

        # Wrap Django's request with DRF's Request
        request = Request(django_request)

        # Call the class method directly
        response = self.view.get_user_email_from_frontend(request)

        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 405)