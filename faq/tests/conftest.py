# faq/tests/conftest.py
import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_translator(mocker):
    mock = mocker.patch('faq.services.translation_service.Translator')
    mock_instance = mock.return_value
    
    def mock_translate(text, dest):
        # Return mock translation in expected format
        return mocker.Mock(text=f"Translated_{dest}_{text}")
    
    mock_instance.translate.side_effect = mock_translate
    return mock_instance