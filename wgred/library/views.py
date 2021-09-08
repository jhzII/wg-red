from django.shortcuts import render
import re
from .forms import UploadFileForm
from .models import File, Word, WordFreq


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            pass
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
