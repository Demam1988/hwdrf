# Generated by Django 5.0.4 on 2024-04-25 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="название"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="описание"),
                ),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="courses/",
                        verbose_name="превью",
                    ),
                ),
                ("price", models.IntegerField(verbose_name="цена")),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="название"
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="описание"
                    ),
                ),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="lessons/",
                        verbose_name="превью",
                    ),
                ),
                ("link", models.URLField(blank=True, null=True, verbose_name="ссылка")),
                (
                    "price",
                    models.IntegerField(blank=True, null=True, verbose_name="цена"),
                ),
            ],
            options={
                "verbose_name": "урок",
                "verbose_name_plural": "уроки",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_of_payment", models.DateField(verbose_name="дата платежа")),
                ("amount", models.IntegerField(verbose_name="сумма платежа")),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("Наличные", "Наличные"),
                            ("Безналичные", "Безналичные"),
                        ],
                        default="CARD",
                        max_length=20,
                        verbose_name="способ оплаты",
                    ),
                ),
            ],
            options={
                "verbose_name": "платёж",
                "verbose_name_plural": "платежи",
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="активна"),
                ),
            ],
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
            },
        ),
    ]
