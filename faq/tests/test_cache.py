# faq/tests/test_cache.py
import pytest
from django.core.cache import cache
from faq.services.cache_service import CacheService  # Updated import

class TestCacheService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.cache_service = CacheService(prefix='test')
        yield
        cache.clear()

    def test_set_and_get(self):
        self.cache_service.set('key1', 'value1')
        assert self.cache_service.get('key1') == 'value1'

    def test_delete(self):
        self.cache_service.set('key1', 'value1')
        self.cache_service.delete('key1')
        assert self.cache_service.get('key1') is None

    def test_clear_faq_cache(self):
        # Set multiple cache entries
        self.cache_service.set('faq_list_en', ['faq1', 'faq2'])
        self.cache_service.set('faq_list_hi', ['faq1_hi', 'faq2_hi'])
        self.cache_service.set('faq_list_bn', ['faq1_bn', 'faq2_bn'])
        
        # Clear cache
        self.cache_service.clear_faq_cache()
        
        # Verify all entries are cleared
        assert self.cache_service.get('faq_list_en') is None
        assert self.cache_service.get('faq_list_hi') is None
        assert self.cache_service.get('faq_list_bn') is None