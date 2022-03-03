from django.test import TestCase
from .models import User
import random
import string


class UserAssertion(TestCase):
    def User_model_test(self, user, username, password):
        self.assertEqual(user.username, username)
        self.assertEqual(user.password, password)


class UserModelTests(UserAssertion):
    def create_a_user_and_saving(self, username=None, password=None):
        user = User()
        if username is not None:
            user.username = username
        if password is not None:
            user.password = password

        if User.objects.filter(username=username).count() > 0:
            return

        user.save()

    def test_is_empty(self):
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 0)

    def test_saving_and_retrieving_user(self):
        username = 'admin'
        password = 'adminadmin'
        self.create_a_user_and_saving(username, password)
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 1)
        user = saved_user.first()
        self.User_model_test(user, username, password)

    def test_saving_and_retrieving_users(self):
        user_length = 10000
        username_length = 6
        username_dic = {}
        cnt = user_length
        user_list = self.create_data(user_length, username_length)

        for i in range(user_length):
            username = user_list[i][0]
            password = user_list[i][1]
            if username in username_dic:
                cnt -= 1
            else:
                username_dic[username] = True

            self.create_a_user_and_saving(username, password)

        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), cnt)

    def create_data(self, user_length, username_length):
        user_list = []
        for _ in range(user_length):
            username = create_random_string(username_length)
            password = create_random_string(10)
            user_list.append([username, password])

        return user_list


def create_random_string(string_len: int) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(string_len))
