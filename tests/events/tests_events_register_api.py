from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.models import Event
from users.models import CustomUser
from tests.AuthAPITestCase import AuthAPITestCase

class EventRegisterTestCase(AuthAPITestCase):
    def setUp(self):
        super(EventRegisterTestCase,self).setUp()
        """
        Create different events with different years and flag input in test database
        """
        # create an unverifeid authenticated user
        self.auth_unverified_user_email = "crash.test1.dummy@gmail.com"
        self.auth_unverified_user_password = "test1.modelx"
        self.auth_unverified_user = CustomUser.objects.create_user(
            email = self.auth_unverified_user_email,
            username = self.auth_unverified_user_email,
            password = self.auth_unverified_user_password,
            verified=False
        )
        
        # create an verified authenticated user
        self.auth_verified_user_email = "crash.test2.dummy@gmail.com"
        self.auth_verified_user_password = "test2.modelx"
        self.auth_verified_user = CustomUser.objects.create_user(
            email = self.auth_verified_user_email,
            username = self.auth_verified_user_email,
            password = self.auth_verified_user_password,
            verified=True
        )
        
        login_api="/users/login/"
        client = APIClient()
        # get auth token of verified user
        verified_login_payload = {
            'email':self.auth_verified_user_email,
            'password':self.auth_verified_user_password
        }
        verified_login_response = client.post(login_api,verified_login_payload)
        self.verified_auth_token = verified_login_response.data['token']
        
        self.event = Event.objects.create(
            id=1,
            name= "test1",
            venue = "test_venue",
            time ="test_time",
            details= "test_details",
            details_html= "test.html",
            cover_pic = "test_cover.jpeg",
            icon= "test_icon.png",
            email= "test@email.com",
            flag = True,
            year = 2019,
        )

    def test_fail_invalid_endpoint(self):
        """
        Test with invalid endpoint
        """ 
        post_register_event_api = "/events/register/twentieth/"
        get_client = APIClient()
        get_client.credentials(HTTP_AUTHORIZATION=self.verified_auth_token)
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_fail_unauthenticated_user(self):
        """
        Test with unauthenticated user
        """
        post_register_event_api = "/events/register/1/"
        get_client = APIClient()
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_fail_unverified_user(self):
        """
        Test with unverified user
        """  
        post_register_event_api = "/events/register/1/"
        get_client = self.create_auth_client()
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_pass_registeration(self):    
        """
        Test with registeration
        """
        post_register_event_api = "/events/register/1/"
        get_client = APIClient()
        get_client.credentials(HTTP_AUTHORIZATION=self.verified_auth_token)
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_fail_event_not_found(self):    
        """
        Test with event not found
        """
        post_register_event_api = "/events/register/0/"
        get_client = APIClient()
        get_client.credentials(HTTP_AUTHORIZATION=self.verified_auth_token)
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)    

    def tearDown(self):
        self.event.delete()
        self.auth_unverified_user.delete()
        self.auth_verified_user.delete()
