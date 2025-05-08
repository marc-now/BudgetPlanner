from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
import api.views as views
import api.models as models
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import datetime

class RegisterUserAPITest(APITestCase):
    """Test endpoints related to User registration"""
    def setUp(self):
        """Create test data"""
        self.url = reverse("register")

    def test_register_url_resolves_to_correct_view(self):
        response = self.client.post(self.url)
        self.assertEqual(response.resolver_match.func.view_class, views.CreateUserView)

    def test_register_url_user_created(self):
        data = {
            "username" : "test_user", 
            "password" : "test_password",
            }
        response = self.client.post(self.url, data)

        # Check if status == 201 Created
        self.assertEqual(response.status_code, 201)

        # Check if database got populated
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(**data).exists)

        # Check JSON response
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["username"], data["username"])
        #self.assertEqual(response.data["password"], data["password"])

    def test_register_url_bad_request(self):
        data = {
            "username" : "test_user", 
            }
        response = self.client.post(self.url, data)

        # Check is status == 400 Bad Request
        self.assertEqual(response.status_code, 400)

        # Check if database did not get populated
        self.assertEqual(User.objects.count(), 0)
        self.assertFalse(User.objects.filter(**data).exists())


class EntriesAPITest(APITestCase):
    """Test Endpoints related to entries"""
    def setUp(self):
        """Create test data"""
        self.url = reverse("entries-list")
        self.user = User.objects.create(
            username="testuser", password="password123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.authorization = f"Bearer {self.token}"
        self.category = models.Category.objects.create(name="TestCat1")
        self.subcategory = models.Subcategory.objects.create(category=self.category, name="TestSubCat1")
        self.account = models.Account.objects.create(name="Test Account", user=self.user)
        self.entry = models.Entry.objects.create(
            title="Test Entry", value=100.00, account=self.account, category=self.category, subcategory=self.subcategory,
            description="Test Description of the Test Entry"
        )

    def test_entries_list_create_url_resolves_to_correct_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.resolver_match.func.view_class, views.EntryListCreate)

    def test_entries_list_url_when_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_entries_list(self):
        """Test if authenticated User can access their Entries."""
        response = self.client.get(self.url, HTTP_AUTHORIZATION=self.authorization)

        # Check is status == 200 OK
        self.assertEqual(response.status_code, 200)

        # Check JSON response
        self.assertEqual(response.data[0]["id"], self.entry.id)
        self.assertEqual(response.data[0]["title"], self.entry.title)
        self.assertEqual(float(response.data[0]["value"]), self.entry.value)
        self.assertEqual(response.data[0]["account"]["id"], self.entry.account.id)
        self.assertEqual(response.data[0]["account"]["name"], self.entry.account.name)
        self.assertEqual(response.data[0]["category"]["id"], self.entry.category.id)
        self.assertEqual(response.data[0]["category"]["name"], self.entry.category.name)
        self.assertEqual(response.data[0]["subcategory"]["id"], self.entry.subcategory.id)
        self.assertEqual(response.data[0]["subcategory"]["name"], self.entry.subcategory.name)
        self.assertEqual(response.data[0]["description"], self.entry.description)

    def test_entries_create(self):
        """Test if authenticated User can successfully create an Entry"""

        data = {
            "title": "Brand new entry",
            "value": 9.99,
            "account_id": self.account.id,
            "category_name": self.category.name,
            "subcategory_name": self.subcategory.name,
            "description": "A description of a brand new entry"
        }
        
        #print(data)

        response = self.client.post(self.url, data, format="json", HTTP_AUTHORIZATION=self.authorization)

        # Check if status == 201 Created
        self.assertEqual(response.status_code, 201)
