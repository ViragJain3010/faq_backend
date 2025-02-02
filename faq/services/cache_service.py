from django.core.cache import cache
from django.conf import settings

class CacheService:
    def __init__(self, prefix='faq', timeout=3600):  # 1 hour default timeout
        self.prefix = prefix
        self.timeout = timeout
    
    def _get_key(self, key):
        return f"{self.prefix}:{key}"
    
    def get(self, key):
        """Get value from cache"""
        try:
            return cache.get(self._get_key(key))
        except Exception as e:
            return None
    
    def set(self, key, value):
        """Set value in cache"""
        try:
            return cache.set(self._get_key(key), value, timeout=self.timeout)
        except Exception as e:
            return None
    
    def delete(self, key):
        """Delete specific key from cache"""
        try:
            return cache.delete(self._get_key(key))
        except Exception as e:
            return None

    def clear_faq_cache(self, languages=['en', 'hi', 'bn']):
        """Clear all FAQ-related cache entries"""
        try:
            # Clear list cache for each language
            for lang in languages:
                cache.delete(self._get_key(f'faq_list_{lang}'))
            
            # If we're using Redis and want to clear pattern-based keys:
            if hasattr(cache, 'keys'):
                pattern = self._get_key('faq_*')
                keys = cache.keys(pattern)
                if keys:
                    cache.delete_many(keys)
        except Exception as e:
            return None