import math
import re
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import UploadFileForm
from .models import File, Word, WordFreq


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('by_file', kwargs={'file_id': file.pk}))
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})


# todo вынести функцию в utils
def handle_uploaded_file(f):
    file = File()
    file.name = f.name
    file.save()

    for s in f:
        for w in re.findall(r'[a-zа-я]+', s.decode('utf-8').lower()):
            word = Word.objects.filter(name=w).first()
            if not word:
                word = Word()
                word.name = w
                word.save()
                # todo создать конструктор
                word_freq = WordFreq()
                word_freq.freq = 1
                word_freq.file = file
                word_freq.word = word
            else:
                word_freq = WordFreq.objects.filter(file=file, word=word).first()
                if word_freq:
                    word_freq.freq += 1
                else:
                    word_freq = WordFreq()
                    word_freq.freq = 1
                    word_freq.file = file
                    word_freq.word = word
            word_freq.save()

    return file


def by_file(request, file_id):
    file = File.objects.get(pk=file_id)
    number_of_files = File.objects.count()

    wfs = WordFreq.objects.filter(file=file)

    words = []

    for wf in wfs:
        words.append({
            'name': wf.word.name,
            'freq': wf.freq,
            'idf': math.log(number_of_files / WordFreq.objects.filter(word=wf.word).count())
        })

    words.sort(key=lambda d: d['idf'], reverse=True)

    context = {
        'name': file.name,
        'words': words[:50],
    }
    return render(request, 'by_file.html', context)
