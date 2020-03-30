from test_plus.test import TestCase


class TestUser(TestCase):
    # 定义初始化函数
    def setUp(self) -> None:
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(self.user.__str__(), "testuser")

    def test_get_profile_name(self):
        assert self.user.get_profile_name() == "testuser"
        self.user.nickname = "nike"
        assert self.user.get_profile_name() == "nike"

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), '/users/testuser/')
