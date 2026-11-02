from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import UserProfile, Post, Comment, Like, Follow
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def get_sample_image():
    file = BytesIO()
    img = Image.new('RGB', (100, 100), color=(99, 102, 241))
    img.save(file, 'jpeg')
    file.seek(0)
    return SimpleUploadedFile("sample.jpg", file.read(), content_type="image/jpeg")


class ConnectHubCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user_alpha',
            email='alpha@test.com',
            password='password123',
            first_name='Alpha',
            last_name='Tester'
        )
        self.user2 = User.objects.create_user(
            username='user_beta',
            email='beta@test.com',
            password='password123',
            first_name='Beta',
            last_name='Tester'
        )
        self.post = Post.objects.create(
            author=self.user1,
            image=get_sample_image(),
            caption='Alpha test post #connecthub'
        )

    def test_profile_auto_creation(self):
        self.assertTrue(hasattr(self.user1, 'profile'))
        self.assertEqual(self.user1.profile.display_name, 'Alpha Tester')

    def test_like_system(self):
        self.client.login(username='user_beta', password='password123')
        # Like
        res = self.client.post(f'/post/{self.post.id}/like/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()['liked'])
        self.assertEqual(self.post.likes.count(), 1)
        # Duplicate like prevention / unlike
        res2 = self.client.post(f'/post/{self.post.id}/like/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertFalse(res2.json()['liked'])
        self.assertEqual(self.post.likes.count(), 0)

    def test_comment_system(self):
        self.client.login(username='user_beta', password='password123')
        res = self.client.post(
            f'/post/{self.post.id}/comment/',
            {'text': 'Nice post!'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.post.comments.count(), 1)
        comment_id = res.json()['comment_id']

        # Delete comment
        res_del = self.client.post(f'/comment/{comment_id}/delete/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res_del.status_code, 200)
        self.assertEqual(self.post.comments.count(), 0)

    def test_follow_system(self):
        self.client.login(username='user_beta', password='password123')
        # Follow
        res = self.client.post(f'/profile/{self.user1.username}/follow/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()['is_following'])
        self.assertTrue(Follow.objects.filter(follower=self.user2, following=self.user1).exists())
        # Self follow prevention
        res_self = self.client.post(f'/profile/{self.user2.username}/follow/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res_self.status_code, 400)
