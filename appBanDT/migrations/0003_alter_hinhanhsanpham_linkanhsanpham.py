# Generated by Django 5.1.6 on 2025-03-06 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBanDT', '0002_dungluong_mausac_hinhanhsanpham_giasanpham'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hinhanhsanpham',
            name='LinkAnhSanPham',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
