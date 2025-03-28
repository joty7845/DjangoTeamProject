from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import Item, Comment, Order, OrderItem
from django.urls import reverse



class CoreModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.item = Item.objects.create(
            title='Test Shirt',
            price=25.0,
            category='S',
            label='P',
            slug='test-shirt',
            description='A test shirt',
            image='test.jpg'
        )

    def test_item_creation(self):
        self.assertEqual(str(self.item), 'Test Shirt')

    def test_comment_creation(self):
        comment = Comment.objects.create(
            item=self.item,
            user=self.user,
            content='Great shirt!'
        )
        self.assertEqual(str(comment), f"{self.user.username} commented on {comment.created_at.strftime('%Y-%m-%d')}")

    def test_add_to_cart_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('core:add-to-cart', kwargs={'slug': self.item.slug}))
        self.assertEqual(response.status_code, 302)  # redirect to order summary
        self.assertTrue(Order.objects.filter(user=self.user, ordered=False).exists())

    def test_order_summary_requires_login(self):
        response = self.client.get(reverse('core:order-summary'))
        self.assertRedirects(response, '/accounts/login/?next=/order-summary/')




