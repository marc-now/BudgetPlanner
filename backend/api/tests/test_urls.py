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


class EntriesListCreateAPITest(APITestCase):
    """Test Endpoints related to EntriesListCreate view"""
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

    def test_entries_create_full(self):
        """Test if authenticated User can successfully create an Entry when providing full data"""

        data = {
            "title": "Brand new entry",
            "value": 9.99,
            "account_id": self.account.id,
            "category_name": self.category.name,
            "subcategory_name": self.subcategory.name,
            "description": "A description of a brand new entry"
        }

        response = self.client.post(self.url, data, format="json", HTTP_AUTHORIZATION=self.authorization)

        # Check if status == 201 Created
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Entry.objects.count(), 2)


    def test_entries_create_no_category_no_subcategory(self):
        """Test if the User cann create an Entry without providing category and subcategory"""

        data = {
            "title": "Brand new entry",
            "value": 9.99,
            "account_id": self.account.id,
            "description": "A description of a brand new entry"
        }

        response = self.client.post(self.url, data, format="json", HTTP_AUTHORIZATION=self.authorization)

        # Check if status == 201 Created
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Entry.objects.count(), 2)


class DeleteEntryAPITest(APITestCase):
    """Test Endpoints related to DeleteEntry view"""
    def setUp(self):
        """Create test data"""
        self.url = reverse("delete-entry", args=[1])
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

    def test_delete_entry_url_resolves_to_correct_view(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.resolver_match.func.view_class, views.EntryDelete)

    def test_delete_entry_url_when_unauthorized(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(models.Entry.objects.count(), 1)

    def test_delete_entry_gets_deleted(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=self.authorization)

        # Check if status == 200 OK and the Entry got deleted
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Entry.objects.count(), 0)

        # Check if deleted Entry data gets returned in the response
        self.assertEqual(response.data["id"], self.entry.id)
        self.assertEqual(response.data["title"], self.entry.title)
        self.assertEqual(float(response.data["value"]), self.entry.value)
        self.assertEqual(response.data["account"]["id"], self.entry.account.id)
        self.assertEqual(response.data["account"]["name"], self.entry.account.name)
        self.assertEqual(response.data["category"]["id"], self.entry.category.id)
        self.assertEqual(response.data["category"]["name"], self.entry.category.name)
        self.assertEqual(response.data["subcategory"]["id"], self.entry.subcategory.id)
        self.assertEqual(response.data["subcategory"]["name"], self.entry.subcategory.name)
        self.assertEqual(response.data["description"], self.entry.description)
    

class UpdateEntryAPITest(APITestCase):
    def setUp(self):
        """Create test data"""
        self.url = reverse("update-entry", args=[1])
        self.user = User.objects.create(
            username="testuser", password="password123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.authorization = f"Bearer {self.token}"
        self.category = models.Category.objects.create(name="TestCat1")
        self.subcategory = models.Subcategory.objects.create(category=self.category, name="TestSubCat1")
        self.account = models.Account.objects.create(name="Test Account", user=self.user)
        self.entry_data = {
            "title": "Test Entry",
            "value": 100.00,
            "account": self.account,
            "category": self.category,
            "subcategory": self.subcategory,
            "description": "Test Description of the Test Entry"
        }
        self.entry = models.Entry.objects.create(**self.entry_data)

    def test_update_entry_url_resolves_to_correct_view(self):
        response = self.client.head(self.url)
        self.assertEqual(response.resolver_match.func.view_class, views.EntryUpdate)

    def test_update_entry_url_when_unauthorized(self):
        response = self.client.patch(self.url, data={"title": "new entry title"})

        self.assertEqual(response.status_code, 401)

    def test_update_entry_all_data(self):
        """Test if all Entry data gets modified properly"""

        category = models.Category.objects.create(name="EditedCat1")
        subcategory = models.Subcategory.objects.create(category=category, name="EditedSubCat1")
        account = models.Account.objects.create(name="Edited Account", user=self.user)

        modified_data = {
            "title": "Edited entry",
            "value": 19.99,
            "account_id": account.id,
            "category_name": category.name,
            "subcategory_name": subcategory.name,
            "description": "A description of an edited entry"
        }

        response = self.client.patch(self.url, modified_data, HTTP_AUTHORIZATION=self.authorization)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["id"], self.entry.id)
        self.assertEqual(response.data["title"], modified_data["title"])
        self.assertEqual(float(response.data["value"]), modified_data["value"])
        self.assertEqual(response.data["account"]["id"], account.id)
        self.assertEqual(response.data["account"]["name"], account.name)
        self.assertEqual(response.data["category"]["id"], category.id)
        self.assertEqual(response.data["category"]["name"], category.name)
        self.assertEqual(response.data["subcategory"]["id"], subcategory.id)
        self.assertEqual(response.data["subcategory"]["name"], subcategory.name)
        self.assertEqual(response.data["description"], modified_data["description"])

    def test_update_entry_partial(self):
        account = models.Account.objects.create(name="Edited Account", user=self.user)

        data = {
            "title": "Edited entry",
            "account_id": account.id
        }

        response = self.client.patch(self.url, data, HTTP_AUTHORIZATION=self.authorization)

        self.assertEqual(response.status_code, 200)

        # Check modified data
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["account"]["id"], account.id)
        self.assertEqual(response.data["account"]["name"], account.name)

        # Check data, which should not have been modified
        self.assertEqual(float(response.data["value"]), self.entry_data["value"])
        self.assertEqual(response.data["category"]["id"], self.category.id)
        self.assertEqual(response.data["category"]["name"], self.category.name)
        self.assertEqual(response.data["subcategory"]["id"], self.subcategory.id)
        self.assertEqual(response.data["subcategory"]["name"], self.subcategory.name)
        self.assertEqual(response.data["description"], self.entry_data["description"])

    def test_update_entry_category_without_subcategory_sets_subcategory_to_none(self):
        new_category = models.Category.objects.create(name="NewCat1")

        data = {
            "category_name": new_category.name,
        }

        response = self.client.patch(self.url, data, HTTP_AUTHORIZATION=self.authorization)

        self.assertEqual(response.data["category"]["id"], new_category.id)
        self.assertEqual(response.data["category"]["name"], new_category.name)
        self.assertEqual(response.data["subcategory"], None)

        self.assertEqual(response.status_code, 200)

