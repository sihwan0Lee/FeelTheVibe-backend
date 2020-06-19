import json
from account.models     import User
from django.test        import TransactionTestCase, Client
from unittest.mock      import patch, MagicMock
from django.db          import transaction

class UserTest(TransactionTestCase):
    def setUp(self):
        User.objects.create(
            name     = '아이유',
            nickname = '낑깡',
            email    = 'dnwi@nawi.com',
            image_url= 'qwdqwdqwd.png'
        )

    def tearDown(self):
        User.objects.filter(name='아이유').delete()

    @patch("account.views.requests")
    def test_user_naver_account(self, mocked_requests):
        c = Client()

        class MockedResponse:
            def json(self):
                return {
                    "response" : {
                        'name' : '파이리',
                        'nickname' : '곧깡패',
                        'email' : 'awd@awd.com',
                        'profile_image' :'awdqwd.png'
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        response = c.get("/account/sign-in",  { "content_type":"applications/json"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message' : 'SUCCESS'})














