# Generated by Django 5.0.4 on 2024-04-23 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], max_length=10)),
                ('description', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Transaction',
            },
        ),
    ]