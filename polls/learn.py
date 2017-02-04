# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, get_list_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
from polls.models import Question,Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.db.models import F
# from django.utils import timezone

# def index(request):
#     # question = Question.objects.get(id=1).choice_set.all()
#     question = timezone.make_naive(Question.objects.get(id=3).pub_date)
#     # time2 = time.strftime("%Y-%m-%d %X")
#     return HttpResponse(question)

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #这个写法very风骚
    # output = '<br>'.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # 1.
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))
    # 
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_question_list = get_list_or_404(Question,)
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request,question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#   ===    
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.filter(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # selected_choice.votes += 1
        # selected_choice.save()
         
        # selected_choice.votes = F('votes')+1
        # selected_choice.save()
        selected_choice.update(votes=F('votes')+1)

# Only <QuerySet> have method update
# Only Modle.object(like Question) have method save
# filter List <QuerySet [<Question: What's up?>]>
# get Object <Question: What's up?>

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))