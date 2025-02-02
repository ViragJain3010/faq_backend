# faq/tests/test_models.py
import pytest
from django.utils import timezone
from faq.models import FAQ  # Updated import
from .factories import FAQFactory


@pytest.mark.django_db
class TestFAQModel:
    def test_faq_creation(self):
        faq = FAQFactory()
        assert faq.pk is not None
        assert faq.question_en.startswith('Test Question')
        assert faq.answer_en.startswith('<p>Test Answer')

    def test_auto_translation_on_create(self, mock_translator):
        faq = FAQ.objects.create(
            question_en="Test Question?",
            answer_en="<p>Test Answer</p>"
        )
        
        # Check if translations were generated
        assert faq.question_hi == "Translated_hi_Test Question?"
        assert faq.question_bn == "Translated_bn_Test Question?"
        assert "<p>Translated_hi_Test Answer</p>" in faq.answer_hi
        assert "<p>Translated_bn_Test Answer</p>" in faq.answer_bn

    def test_auto_translation_on_update(self, mock_translator):
        faq = FAQFactory()
        original_hi = faq.question_hi
        
        # Update English content
        faq.question_en = "Updated Question?"
        faq.save()
        
        # Refresh from database
        faq.refresh_from_db()
        
        # Check if translations were updated
        assert faq.question_hi != original_hi
        assert faq.question_hi == "Translated_hi_Updated Question?"

    def test_timestamps(self):
        faq = FAQFactory()
        assert isinstance(faq.created_at, timezone.datetime)
        assert isinstance(faq.updated_at, timezone.datetime)