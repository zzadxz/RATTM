from unittest.mock import patch
from rest_framework.test import APIClient
from django.test import SimpleTestCase
from .use_case import LoginUseCase


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
        with patch("login.use_cases.randint") as mock_randint:
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
        with patch("login.use_cases.randint") as mock_randint:
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
        with patch("login.use_cases.randint") as mock_randint:
            mock_randint.return_value = 57
            user_id = login_use_case.match_email_to_id(email)
            self.assertEqual(
                user_id, "57"
            )  # Should not match existing email due to case sensitivity
            mock_randint.assert_called_once_with(0, 99)


class GetUserEmailFromFrontendTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/login/get_email/"

    @patch("login.use_cases.match_email_to_id")  # Mock the use case function
    def test_existing_email(self, mock_match_email_to_id):
        """
        Test that the view returns the correct user ID for an existing email.
        """
        mock_match_email_to_id.return_value = "21"
        email = "liuyimeng01@gmail.com"

        response = self.client.post(
            self.url,
            data=email,  # Send raw email as plain text
            content_type="text/plain",  # Indicate the content type
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"message": f"Got user's email {email}", "data": "21"},
        )
        mock_match_email_to_id.assert_called_once_with(email)  # Pass plain email string

    @patch("login.use_cases.match_email_to_id")
    def test_non_existing_email(self, mock_match_email_to_id):
        """
        Test that the view handles non-existing emails and returns a random user ID.
        """
        mock_match_email_to_id.return_value = "42"
        email = "nonexistentemail@gmail.com"

        response = self.client.post(
            self.url,
            data=email,  # Send raw email as plain text
            content_type="text/plain",  # Indicate the content type
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {"message": f"Got user's email {email}", "data": "42"},
        )
        mock_match_email_to_id.assert_called_once_with(email)  # Pass plain email string

    def test_invalid_request_method(self):
        """
        Test that the view rejects non-POST requests.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
