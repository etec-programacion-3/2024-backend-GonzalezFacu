# Generated by Django 5.1.1 on 2024-10-31 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shortDescripiton',
            field=models.CharField(default='', max_length=255),
        ),
    ]