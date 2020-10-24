# Generated by Django 3.1.2 on 2020-10-24 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_subscriber_deleted_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 날짜')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 날짜')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='삭제 날짜')),
                ('sender', models.EmailField(max_length=320, verbose_name='보낸 이')),
                ('subject', models.CharField(max_length=255, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('success', models.BooleanField(default=False, verbose_name='전송 성공 여부')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.subscriber', verbose_name='구독자')),
            ],
            options={
                'verbose_name': '보낸 메일 내역',
                'verbose_name_plural': '보낸 메일 내역',
            },
        ),
    ]