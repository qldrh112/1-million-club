# Generated by Django 4.2.8 on 2024-05-24 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepositOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.CharField(max_length=20)),
                ('intr_rate_type', models.CharField(max_length=2, null=True)),
                ('intr_rate', models.FloatField(null=True)),
                ('intr_rate2', models.FloatField(null=True)),
                ('save_trm', models.CharField(max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DepositProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('fin_prdt_nm', models.CharField(max_length=50)),
                ('kor_co_nm', models.CharField(max_length=20)),
                ('max_limit', models.PositiveIntegerField(null=True)),
                ('join_way', models.CharField(max_length=50)),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('etc_note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_co_no', models.CharField(max_length=20)),
                ('intr_rate_type', models.CharField(max_length=2, null=True)),
                ('rsrv_type', models.CharField(max_length=2)),
                ('intr_rate', models.FloatField(null=True)),
                ('intr_rate2', models.FloatField(null=True)),
                ('save_trm', models.CharField(max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SavingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('fin_prdt_nm', models.CharField(max_length=50)),
                ('kor_co_nm', models.CharField(max_length=20)),
                ('max_limit', models.PositiveIntegerField(null=True)),
                ('join_way', models.CharField(max_length=50)),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('spcl_cnd', models.TextField()),
                ('etc_note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='StockProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prdt_cd', models.CharField(max_length=10)),
                ('prdt_name', models.CharField(max_length=60)),
                ('end_price', models.IntegerField()),
                ('fluctuation_rate', models.FloatField()),
                ('trade_amount', models.IntegerField()),
                ('trade_price_amount', models.IntegerField()),
                ('capitalization', models.IntegerField()),
                ('shared_amount', models.IntegerField()),
                ('idx_bztp_mcls_cd_name', models.CharField(blank=True, max_length=60)),
                ('one_before_end_price', models.IntegerField(blank=True, null=True)),
                ('one_before_end_rate', models.FloatField(blank=True, null=True)),
                ('two_before_end_price', models.IntegerField(blank=True, null=True)),
                ('two_before_end_rate', models.FloatField(blank=True, null=True)),
                ('three_before_end_price', models.IntegerField(blank=True, null=True)),
                ('three_before_end_rate', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockProductBuyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('buy_date', models.DateField(auto_now_add=True)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.stockproduct')),
            ],
        ),
        migrations.CreateModel(
            name='SavingProductJoinInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_payment', models.PositiveIntegerField()),
                ('is_prime_rate', models.BooleanField()),
                ('join_date', models.DateField(auto_now_add=True)),
                ('saving_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.savingoption')),
            ],
        ),
        migrations.AddField(
            model_name='savingoption',
            name='saving',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.savingproduct'),
        ),
        migrations.CreateModel(
            name='DepositProductJoinInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.PositiveIntegerField()),
                ('is_prime_rate', models.BooleanField()),
                ('join_date', models.DateField(auto_now_add=True)),
                ('deposit_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.depositoption')),
            ],
        ),
        migrations.AddField(
            model_name='depositoption',
            name='deposit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.depositproduct'),
        ),
        migrations.CreateModel(
            name='CorporationDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crno', models.CharField(max_length=30)),
                ('corpNm', models.CharField(max_length=300)),
                ('enpPbanCmpyNm', models.CharField(max_length=500)),
                ('enpDtadr', models.CharField(max_length=500)),
                ('enpHmpgUrl', models.CharField(max_length=300)),
                ('enpTlno', models.CharField(max_length=100)),
                ('enpEstbDt', models.CharField(max_length=8)),
                ('enpEmpeCnt', models.IntegerField()),
                ('enpPn1AvgSlryAmt', models.FloatField()),
                ('enpMainBizNm', models.CharField(max_length=1000)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finances.stockproduct')),
            ],
        ),
    ]
