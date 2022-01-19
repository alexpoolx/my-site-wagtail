# Generated by Django 3.2.11 on 2022-01-12 01:24

from django.db import migrations
import stream.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flexpage',
            name='content',
            field=wagtail.core.fields.StreamField([('title_and_text', wagtail.core.blocks.StructBlock([('titulo', wagtail.core.blocks.CharBlock(help_text='Añade tu titulo', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Añade tu texto aqui', required=True))])), ('full_richtext', stream.blocks.RichTextBlock()), ('simple_richtext', stream.blocks.SimpleRichTextBlock())], blank=True, null=True),
        ),
    ]
