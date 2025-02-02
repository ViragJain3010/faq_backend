from django.contrib import admin
from .models import FAQ
from .services.translation_service import TranslationService

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_en', 'created_at', 'updated_at')
    search_fields = ('question_en', 'answer_en')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('English Content', {
            'fields': ('question_en', 'answer_en')
        }),
        ('Hindi Translation', {
            'fields': ('question_hi', 'answer_hi'),
            'classes': ('collapse',)
        }),
        ('Bengali Translation', {
            'fields': ('question_bn', 'answer_bn'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        """ Trigger translation if the English question/answer is modified """
        if change:  # This means the object is being updated, not created
            original = FAQ.objects.get(pk=obj.pk)
            if obj.question_en != original.question_en or obj.answer_en != original.answer_en:
                translation_service = TranslationService()
                translations = translation_service.translate_faq(obj.question_en, obj.answer_en)
                
                # Assign translated values to the object
                for key, value in translations.items():
                    setattr(obj, key, value)

        super().save_model(request, obj, form, change)  # Call the default save method
