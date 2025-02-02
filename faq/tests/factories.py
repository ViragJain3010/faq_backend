# faq/tests/factories.py
import factory
from factory.django import DjangoModelFactory
from faq.models import FAQ  # Updated import

class FAQFactory(DjangoModelFactory):
    class Meta:
        model = FAQ

    question_en = factory.Sequence(lambda n: f'Test Question {n}?')
    answer_en = factory.Sequence(lambda n: f'<p>Test Answer {n}</p>')
    question_hi = factory.Sequence(lambda n: f'परीक्षण प्रश्न {n}?')
    answer_hi = factory.Sequence(lambda n: f'<p>परीक्षण उत्तर {n}</p>')
    question_bn = factory.Sequence(lambda n: f'পরীক্ষা প্রশ্ন {n}?')
    answer_bn = factory.Sequence(lambda n: f'<p>পরীক্ষা উত্তর {n}</p>')