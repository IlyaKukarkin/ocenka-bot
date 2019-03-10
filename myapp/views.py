from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
import pymorphy2
import scipy.spatial
from .models import Question
from .forms import PostForm
from . import config

morph = pymorphy2.MorphAnalyzer()

# Create your views here.
def home(request):
    recent_questions = Question.objects.order_by('-asked_date')[:5]
    if (len(config.main_bag) == 0):
        init(Question.objects.all())
    return render(request, 'myapp/home.html', {'recent_questions': recent_questions})

def question(request):
    if (len(config.main_bag) == 0):
        init(Question.objects.all())
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            my_question = form.cleaned_data['your_question']
            find_question(my_question)
            return redirect('question_result')
    else:
        form = PostForm()
    return render(request, 'myapp/question.html', {'form': form})

def answer(request, pk):
    if (len(config.main_bag) == 0):
        init(Question.objects.all())
    answer = get_object_or_404(Question, pk=pk)
    answer.asked_date = timezone.now().timestamp()
    answer.save()
    return render(request, 'myapp/answer.html', {'answer': answer})

def all(request):
    if (len(config.main_bag) == 0):
        init(Question.objects.all())
    all_questions = Question.objects.all()
    return render(request, 'myapp/all.html', {'all_questions': all_questions})

def question_result(request):
    if (len(config.main_bag) == 0):
        init(Question.objects.all())
    err = False
    res = []
    if (config.result1 != -1):
        try:
            res.append(Question.objects.get(pk=config.result1))
        except Question.DoesNotExist:
            err = True
        try:
            res.append(Question.objects.get(pk=config.result2))
        except Question.DoesNotExist:
            err = True
        try:
            res.append(Question.objects.get(pk=config.result3))
        except Question.DoesNotExist:
            err = True
    return render(request, 'myapp/question_result.html', {'question_result': res})

def tokenize(text):
    txt = clear(str(text).lower())
    return txt.split()
        
def clear(text):
    chars = ".,?!();:–-«»*\"/"
    for c in chars:
        if c in text:
            text = text.replace(c, ' ')
    return text

def find_question(qst_to_find):
    qst_to_find = get_ready_question(qst_to_find)

    min_res_bag = 1
    resIndexBag1 = -1
    resIndexBag2 = -1
    resIndexBag3 = -1
    result = config.main_bag.copy()
    result.append(qst_to_find)
    index1 = len(result) - 1
    unique_words = set(' '.join([' '.join(sent) for sent in result]).split())
    bag_vectors = [[sent.count(word) for word in unique_words] for sent in result]
    
    for i, sent in enumerate(result):
        calculate = scipy.spatial.distance.cosine(bag_vectors[index1], bag_vectors[i])
        if (calculate < min_res_bag and calculate != 0):
            resIndexBag3 = resIndexBag2
            resIndexBag2 = resIndexBag1
            resIndexBag1 = i
            min_res_bag = calculate

    if (min_res_bag != 1):
        config.result1 = resIndexBag1
        config.result2 = resIndexBag2
        config.result3 = resIndexBag3
    else:
        config.result1 = -1
        config.result2 = -1
        config.result3 = -1

def get_ready_question(question):
    tokens = []
    
    tokens = tokenize(question)
    for i in range(len(tokens)):
        tokens[i] = morph.parse(tokens[i])[0].normal_form
        
    norm_tokens = []
    for word in tokens:
        if word not in digits:
            norm_tokens.append(word)
            
    norm_tokens_final = []
    for word in norm_tokens:
        if word not in predlogs:
            norm_tokens_final.append(word)
            
    result = []
    for word in norm_tokens_final:
        if word not in stop_words:
            result.append(word)
        
    return result

def init(quesions):
    mas = []
    mas_tokens = []
    for qst in quesions:
        mas.append(str(qst))
    config.all_questions_string = mas.copy()
    for qst in mas:
        mas_tokens.append(get_ready_question(qst))
    config.main_bag = mas_tokens.copy()

stop_words = {'оценка','стоимость','предприятие','анализ'}
predlogs = {"в","без","на","до","из","к","от","по","о","перед","при","через","с","у","и","нет","за","над","для","об", "не", "а"
            "под","про","вблизи","вглубь","вдоль","возле","около","вокруг","впереди","после","посредством",
            "путем","насчет","ввиду","случаю","течение","благодаря","несмотря","спустя","а","абы","аж","ан","благо","буде",
            "будто","вроде","да","дабы","даже","едва","ежели","если","же","затем","зато","и","ибо","или","итак","кабы",
            "как","когда","коли","коль","ли","либо","лишь","нежели","но","пока",'покамест',"покуда",
            "поскольку","притом","причем","пускай","пусть","раз","разве","ровно","сиречь","словно","так","также",
            "тоже","только","точно","хоть","хотя","чем","чисто","что","чтоб","чтобы","чуть","якобы","я", "что", "он",
            "как", "этот", "они", "мы", "весь", "который", "она", "так", "свой", "вы", "ты", "такой", "его", "себя", "ее",
            "когда", "вот", "другой", "наш", "самый", "мой", "кто", "сам", "там", "какой", "их", "потом", "ничто", "каждый",
            "потому", "тогда", "здесь", "какой-то", "что-то", "всегда", "ваш", "никто", "почему", "поэтому", "свое",
            "никогда", "никакой", "некоторый", "твой", "куда", "кто-то", "как-то", "зачем", "сей", "туда", "какой-нибудь",
            "всего", "откуда", "сюда", "столь", "где-то", "что-нибудь", "почему-то", "некий", "когда-то", "чего",
            "отсюда", "чей", "нечто", "кто-нибудь", "вон", "оттуда", "какой-либо", "таков", "куда-то", "никуда", "каков",
            "таковой", "кой", "оттого", "некогда", "отчего", "нигде", "кое-что", "когда-нибудь", "чей-то", "где-нибудь",
            "такой-то", "что-либо", "всюду", "как-нибудь", "откуда-то", "ничуть", "куда-нибудь", "сколь", "тут-то",
            "этакий", "тот-то", "так-то", "кое-какой", "кое-как", "кое-кто", "зачем-то", "кое-где", "кто-либо", "некто",
            "отчего-то", "каковой", "эдакий", "нибудь", "тогда-то", "чего-то", "когда-либо", "почем", "отовсюду",
            "ничей", "доселе", "оный", "ниоткуда", "экий", "чей-нибудь", "сям", "никой", "тот", "это", "то"}
digits = {'0','1','2','3','4','5','6','7','8','9','10','1000','30','500','q','w','e','r','t','y','u','i','o','p',
          'a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m'}