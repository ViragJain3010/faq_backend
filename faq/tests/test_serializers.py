# tests/test_serializers.py
import pytest
from ..serializers import FAQSerializer, FAQCreateUpdateSerializer
from .factories import FAQFactory

@pytest.mark.django_db
class TestFAQSerializers:
    def test_faq_serializer_output(self):
        faq = FAQFactory()
        serializer = FAQSerializer(faq)
        data = serializer.data
        
        assert 'question' in data
        assert 'answer' in data
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_faq_serializer_language_fallback(self):
        faq = FAQFactory(
            question_en='English Question',
            question_hi='',  # Empty Hindi translation
        )
        
        serializer = FAQSerializer(faq, context={'lang': 'hi'})
        assert serializer.data['question'] == 'English Question'  # Should fallback to English

    def test_create_update_serializer(self):
        data = {
            'question_en': 'Test Question',
            'answer_en': '<p>Test Answer</p>'
        }
        
        serializer = FAQCreateUpdateSerializer(data=data)
        assert serializer.is_valid()