# Generated by Django 5.1.2 on 2024-10-31 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0002_remove_award_balance_alter_award_gets_scholarship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_received', models.DecimalField(decimal_places=2, max_digits=10)),
                ('season_received', models.CharField(max_length=20)),
                ('award', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarship.award')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scholarship.student')),
            ],
        ),
    ]
