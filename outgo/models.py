from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(verbose_name="Аватар", blank=True, null=True, upload_to="avatars")

    @property
    def text(self):
        return self.last_name if self.last_name else self.username

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subdivision(models.Model):
    subdivision_name = models.TextField(verbose_name="Название подразделения")
    subdivision_short_name = models.CharField(verbose_name="Название подразделения (короткое)", max_length=100,
                                              blank=True, null=True)
    employee_count = models.IntegerField(verbose_name="Количество сотрудников (по списку)", blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь (владелец)")

    def __str__(self):
        return self.subdivision_name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class EmployeeKind(models.Model):
    kind = models.CharField(verbose_name="Вид содрудника", max_length=255)

    def __str__(self):
        return self.kind

    class Meta:
        ordering = ('id',)
        verbose_name = 'Вид сотрудника'
        verbose_name_plural = 'Виды сотрудников'


class SheetItem(models.Model):
    item_name = models.CharField(verbose_name="Название пункта", max_length=255)
    order = models.IntegerField(verbose_name="Порядковый номер", default=0)
    sign = models.IntegerField(verbose_name="+/-", default=1)
    # is_required = models.BooleanField(verbose_name="Обязательное поле", default=True)

    def __str__(self):
        return self.item_name + ' ' + str(self.sign)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пункт расхода'
        verbose_name_plural = 'Пункты расхода'


class OutgoKind(models.Model):
    kind = models.CharField(verbose_name="Вид расхода", max_length=255)

    def __str__(self):
        return self.kind

    class Meta:
        ordering = ('id',)
        verbose_name = 'Вид расхода'
        verbose_name_plural = 'Виды расходов'


class OutgoData(models.Model):
    date_time_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")
    kind = models.ForeignKey(OutgoKind, on_delete=models.CASCADE, verbose_name="Вид расхода")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Кто создал")
    subdivision = models.ForeignKey(Subdivision, on_delete=models.CASCADE, verbose_name="Подразделение")
    outgo_date = models.DateField(verbose_name="На какую дату расход")

    def __str__(self):
        return str(self.outgo_date) + ' ' + str(self.subdivision) + ' ' + str(self.kind)

    class Meta:
        ordering = ('-outgo_date',)
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'


class Outgo(models.Model):
    outgo = models.ForeignKey(OutgoData, verbose_name="Расход", on_delete=models.CASCADE)
    sheet_item = models.ForeignKey(SheetItem, verbose_name="Пункт расхода", on_delete=models.CASCADE)
    employee_kind = models.ForeignKey(EmployeeKind, verbose_name="Вид сотрудника", on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name="Количество", default=0)
    description = models.TextField(verbose_name="Фамилии", blank=True, null=True)

    def __str__(self):
        return str(self.outgo)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Отсутствующие в расходе'
        verbose_name_plural = 'Отсутствующие в расходе'