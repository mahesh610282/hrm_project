from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from django.contrib import messages
from django.contrib.messages import get_messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .views import register, login_user, forgot_password_request, forgot_password, logout_user

# Create your tests here.

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.forgot_password_request_url = reverse('forgot_password_request')
        self.forgot_password_url = reverse('forgot_password')
        self.logout_url = reverse('logout')
        self.user_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.set_password(self.user_data['password'])
        self.user.save()
    def test_register_user(self):
        response = self.client.post(self.register_url, {
            'firstname': 'Jane',
            'lastname': 'Doe',
            'username': 'janedoe',
            'email': 'janedoe@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='janedoe').exists())
    def test_login_user(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    def test_forgot_password_request(self):
        response = self.client.post(self.forgot_password_request_url, {
            'email': self.user_data['email']
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.forgot_password_url}?email={self.user_data['email']}")
    def test_forgot_password(self):
        response = self.client.post(f"{self.forgot_password_url}?email={self.user_data['email']}", {
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
    def test_logout_user(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertIn('Logged out successfully', [msg.message for msg in get_messages(response.wsgi_request)])  
    def test_register_user_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'firstname': 'Jane',
            'lastname': 'Doe',
            'username': 'janedoe',
            'email': 'janedoe@example.com',
            'password': 'password123',
            'confirm_password': 'password456'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Passwords do not match', [msg.message for msg in get_messages(response.wsgi_request)])
    def test_login_user_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', [msg.message for msg in get_messages(response.wsgi_request)])
    def test_forgot_password_request_email_not_exist(self):
        response = self.client.post(self.forgot_password_request_url, {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Email not found', [msg.message for msg in get_messages(response.wsgi_request)])
    def test_forgot_password_user_not_found(self):
        response = self.client.post(f"{self.forgot_password_url}?email=nonexistent@example.com", {
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', [msg.message for msg in get_messages(response.wsgi_request)])
    def test_forgot_password_mismatch(self):
        response = self.client.post(f"{self.forgot_password_url}?email={self.user_data['email']}", {
            'new_password': 'newpassword123',
            'confirm_password': 'differentpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Passwords do not match', [msg.message for msg in get_messages(response.wsgi_request)])        
