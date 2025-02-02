from rest_framework import serializers
from .models import FAQ
from .services.cache_service import CacheService

class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']

    def _get_cached_content(self, obj, field_prefix, lang):
        cache_service = CacheService()
        cache_key = f'faq_{obj.id}_{field_prefix}_{lang}'
        
        # Try to get from cache
        cached_content = cache_service.get(cache_key)
        if cached_content is not None:
            return cached_content

        # Get from database
        field_name = f'{field_prefix}_{lang}'
        content = getattr(obj, field_name) or getattr(obj, f'{field_prefix}_en')
        
        # Cache the content
        cache_service.set(cache_key, content)
        return content

    def get_question(self, obj):
        lang = self.context.get('lang', 'en')
        return self._get_cached_content(obj, 'question', lang)

    def get_answer(self, obj):
        lang = self.context.get('lang', 'en')
        return self._get_cached_content(obj, 'answer', lang)

class FAQCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question_en', 'answer_en']