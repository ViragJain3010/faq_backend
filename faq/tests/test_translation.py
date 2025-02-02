# faq/tests/test_translation.py
import pytest
from bs4 import BeautifulSoup
from faq.services.translation_service import TranslationService  # Updated import

@pytest.mark.django_db
class TestTranslationService:
    def test_translate_text(self, mock_translator):
        service = TranslationService()
        text = "Hello World"
        result = service.translate_text(text, 'hi')
        assert result == f"Translated_hi_{text}"

    def test_translate_html(self, mock_translator):
        service = TranslationService()
        html = "<p>Hello</p><p>World</p>"
        result = service.translate_html(html, 'hi')
        
        # Parse both results to compare structure
        original_soup = BeautifulSoup(html, 'html.parser')
        result_soup = BeautifulSoup(result, 'html.parser')
        
        assert len(original_soup.find_all('p')) == len(result_soup.find_all('p'))
        assert "Translated_hi_Hello" in result
        assert "Translated_hi_World" in result

    def test_complex_html_translation(self, mock_translator):
        service = TranslationService()
        html = """
        <div class="content">
            <h1>Title</h1>
            <p>First paragraph</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </div>
        """
        result = service.translate_html(html, 'hi')
        
        # Check structure preservation
        result_soup = BeautifulSoup(result, 'html.parser')
        assert result_soup.find('h1') is not None
        assert result_soup.find('p') is not None
        assert len(result_soup.find_all('li')) == 2
        
        # Check translations
        assert "Translated_hi_Title" in result
        assert "Translated_hi_First paragraph" in result
        assert "Translated_hi_Item 1" in result
        assert "Translated_hi_Item 2" in result