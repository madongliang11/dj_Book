# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 16:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'db_table': 'order_item',
            },
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.BigIntegerField(unique=True, verbose_name='订单号')),
                ('pay_type', models.IntegerField(choices=[(0, '货到付款'), (1, '微信支付'), (2, '支付宝支付')], default=0, verbose_name='支付类型')),
                ('address', models.CharField(default='', max_length=200, verbose_name='订单配送地址')),
                ('phone', models.BigIntegerField(default=0, verbose_name='联系方式')),
                ('order_time', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='下单时间')),
                ('flag', models.IntegerField(default=0, verbose_name='是否隐藏')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.ArtsUser', verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户订单',
                'verbose_name_plural': '用户订单',
                'db_table': 'product_order',
            },
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.ProductOrder', verbose_name='订单号'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Art', verbose_name='商品编号'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.ArtsUser', verbose_name='购买用户'),
        ),
    ]
