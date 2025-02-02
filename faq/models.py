# faq/models.py
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from .services.cache_service import CacheService
from .services.translation_service import TranslationService

class FAQ(models.Model):
    question_en = models.TextField(verbose_name="Question (English)")
    answer_en = RichTextField(verbose_name="Answer (English)")
    
    question_hi = models.TextField(verbose_name="Question (Hindi)", blank=True, null=True)
    answer_hi = RichTextField(verbose_name="Answer (Hindi)", blank=True, null=True)
    
    question_bn = models.TextField(verbose_name="Question (Bengali)", blank=True, null=True)
    answer_bn = RichTextField(verbose_name="Answer (Bengali)", blank=True, null=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question_en[:100]
    
    def has_english_content_changed(self):
        """Check if English content has changed"""
        if not self.pk:
            return True
            
        try:
            old_instance = FAQ.objects.get(pk=self.pk)
            return (
                old_instance.question_en != self.question_en or 
                old_instance.answer_en != self.answer_en
            )
        except FAQ.DoesNotExist:
            return True

@receiver(post_save, sender=FAQ)
def translate_faq(sender, instance, created, **kwargs):
    """Signal handler to translate FAQ content"""
    if created or instance.has_english_content_changed():
        translation_service = TranslationService()
        cache_service = CacheService()
        
        # Get translations
        translations = translation_service.translate_faq(
            instance.question_en,
            instance.answer_en
        )
        
        # Update instance without triggering save
        FAQ.objects.filter(pk=instance.pk).update(**translations)
        
        # Clear cache
        cache_service.clear_faq_cache()