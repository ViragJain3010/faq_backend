# Generated by Django 5.0.2 on 2025-02-01 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_alter_faq_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['-created_at'], 'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQs'},
        ),
    ]
