from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=2, unique=True, verbose_name="Код страны")
    name = models.CharField(max_length=30, verbose_name="Название страны")

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class Region(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name='regions',
        verbose_name="Страна"
    )
    name = models.CharField(max_length=30, verbose_name="Название региона/области")
    code = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name="Код региона"
    )

    def __str__(self):
        return f"{self.name}, {self.country.code}"

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class Address(models.Model):
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='addresses',
        verbose_name="Регион"
    )
    city = models.CharField(max_length=30, verbose_name="Город")
    street_address = models.CharField(max_length=100, verbose_name="Улица, дом, кв.")
    postal_code = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        verbose_name="Почтовый индекс"
    )

    def __str__(self):
        return f"{self.city}, {self.street_address}"

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"