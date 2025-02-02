# faq/tests/test_views.py
import pytest
from django.urls import reverse
from rest_framework import status
from faq.models import FAQ  # Updated import
from .factories import FAQFactory

@pytest.mark.django_db
class TestFAQViewSet:
    def test_list_faqs(self, api_client):
        # Create test FAQs
        FAQFactory.create_batch(3)
        
        url = reverse('faq-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_faq(self, api_client, mock_translator):
        url = reverse('faq-list')
        data = {
            'question_en': 'Test Question?',
            'answer_en': '<p>Test Answer</p>'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert FAQ.objects.count() == 1
        assert FAQ.objects.first().question_hi == 'Translated_hi_Test Question?'

    def test_get_faq_with_language(self, api_client):
        faq = FAQFactory(
            question_en='English Question',
            question_hi='हिंदी प्रश्न'
        )
        
        url = reverse('faq-detail', kwargs={'pk': faq.pk})
        
        # Test English
        response_en = api_client.get(url)
        assert response_en.data['question'] == 'English Question'
        
        # Test Hindi
        response_hi = api_client.get(f"{url}?lang=hi")
        assert response_hi.data['question'] == 'हिंदी प्रश्न'