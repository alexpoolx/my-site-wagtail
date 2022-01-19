# Generated by Django 3.2.11 on 2022-01-14 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('articulos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticulosCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, help_text='Indentifica la categoria', max_length=255, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Articulo Categoria',
                'verbose_name_plural': 'Articulo Categorias',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ArticuloAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True, null=True)),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Articulo Author',
                'verbose_name_plural': 'Articulo Authors',
            },
        ),
    ]
