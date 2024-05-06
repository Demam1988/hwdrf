from django.db import models

from django.conf import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, **NULLABLE, verbose_name="название")
    description = models.TextField(**NULLABLE, verbose_name="описание")
    picture = models.ImageField(upload_to="courses/", verbose_name="превью", **NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="добавил курс",
    )
    price = models.IntegerField(verbose_name="цена")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=100, **NULLABLE, verbose_name="название")
    description = models.CharField(max_length=100, **NULLABLE, verbose_name="описание")
    picture = models.ImageField(upload_to="lessons/", **NULLABLE, verbose_name="превью")
    link = models.URLField(max_length=200, **NULLABLE, verbose_name="ссылка")
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="lessons", verbose_name="курс"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="добавил урок",
    )
    price = models.IntegerField(verbose_name="цена", **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["-id"]


class Payment(models.Model):
    CASH = "Наличные"
    CARD = "Безналичные"

    PAYMENT_CHOICES = [
        (CASH, "Наличные"),
        (CARD, "Безналичные"),
    ]

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="пользователь"
    )
    date_of_payment = models.DateField(verbose_name="дата платежа")
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, **NULLABLE, verbose_name="оплаченный курс"
    )
    lesson = models.ForeignKey(
        "Lesson", on_delete=models.CASCADE, **NULLABLE, verbose_name="оплаченный урок"
    )
    amount = models.IntegerField(verbose_name="сумма платежа")
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="CARD",
        verbose_name="способ " "оплаты",
    )

    def __str__(self):
        return f"{self.date_of_payment} - {self.amount}"

    class Meta:
        verbose_name = "платёж"
        verbose_name_plural = "платежи"


class Subscription(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="курс",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="пользователь",
    )
    is_active = models.BooleanField(default=False, verbose_name="активна")

    def __str__(self):
        return f"{self.user} subscription on {self.course}: {self.is_active}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
