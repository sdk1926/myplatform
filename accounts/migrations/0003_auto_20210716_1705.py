# Generated by Django 3.2.5 on 2021-07-16 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_accounts_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='KakaoAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kakao_id', models.CharField(max_length=128, unique=True)),
                ('email', models.EmailField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '카카오 계정',
                'verbose_name_plural': '카카오 계정',
                'ordering': ['-created'],
            },
        ),
        migrations.AlterModelOptions(
            name='accounts',
            options={'ordering': ['-created'], 'verbose_name': '계정', 'verbose_name_plural': '계정'},
        ),
    ]
