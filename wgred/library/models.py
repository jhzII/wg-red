from django.db import models


class File(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя файла')


class Word(models.Model):
    name = models.CharField(max_length=50, verbose_name='Слово')


class WordFreq(models.Model):
    freq = models.IntegerField(verbose_name='Частота')
    file = models.ForeignKey(File, on_delete=models.CASCADE, verbose_name='Файл')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, verbose_name='Слово')
