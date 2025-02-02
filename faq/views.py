# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404
# from .models import FAQ
# from .serializers import FAQSerializer, FAQCreateUpdateSerializer
# from .services.translation_service import TranslationService

# class FAQViewSet(viewsets.ModelViewSet):
#     queryset = FAQ.objects.all()
#     translation_service = TranslationService()

#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return FAQCreateUpdateSerializer
#         return FAQSerializer

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['lang'] = self.request.query_params.get('lang', 'en')
#         return context

#     # def create(self, request, *args, **kwargs):
#     #     serializer = self.get_serializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
        
#     #     # Get translations
#     #     translations = self.translation_service.translate_faq(
#     #         serializer.validated_data['question_en'],
#     #         serializer.validated_data['answer_en']
#     #     )
        
#     #     # Combine original data with translations
#     #     faq_data = {**serializer.validated_data, **translations}
        
#     #     # Create the FAQ instance
#     #     faq = FAQ.objects.create(**faq_data)
        
#     #     # Return the response with the specified language
#     #     response_serializer = FAQSerializer(faq, context=self.get_serializer_context())
#     #     return Response(response_serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
        
#         # Get translations only if English content is updated
#         if 'question_en' in serializer.validated_data or 'answer_en' in serializer.validated_data:
#             translations = self.translation_service.translate_faq(
#                 serializer.validated_data.get('question_en', instance.question_en),
#                 serializer.validated_data.get('answer_en', instance.answer_en)
#             )
#             serializer.validated_data.update(translations)
        
#         # Update the instance
#         for attr, value in serializer.validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
        
#         # Return the response with the specified language
#         response_serializer = FAQSerializer(instance, context=self.get_serializer_context())
#         return Response(response_serializer.data)

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import FAQ
from .serializers import FAQSerializer, FAQCreateUpdateSerializer
from .services.translation_service import TranslationService

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    translation_service = TranslationService()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FAQCreateUpdateSerializer
        return FAQSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'en')
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Get translations only if English content is updated
        if 'question_en' in serializer.validated_data or 'answer_en' in serializer.validated_data:
            translations = self.translation_service.translate_faq(
                serializer.validated_data.get('question_en', instance.question_en),
                serializer.validated_data.get('answer_en', instance.answer_en)
            )
            serializer.validated_data.update(translations)
        
        # Update the instance
        for attr, value in serializer.validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Return the response with the specified language
        response_serializer = FAQSerializer(instance, context=self.get_serializer_context())
        return Response(response_serializer.data)


    def perform_update(self, serializer):
        serializer.save()