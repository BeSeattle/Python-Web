# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from polls.models import Choice, Question
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
# default context_object_name is 'question_list'
# for ListView, the automatically generated context variable is question_list. 
# To override this we provide the context_object_name attribute, 
# specifying that we want to use 'latest_question_list' instead.

    def get_queryset(self):
        """Return the last five published questions."""
        question_list = Question.objects.filter(pub_date__lte=timezone.now())
        return question_list.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
# <app name>/<model name>_detail.html.
# like: question_detail.html          is default templates name
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.filter(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/question_detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # selected_choice.votes += 1
        # selected_choice.save()
         
        # selected_choice.votes = F('votes')+1
        # selected_choice.save()
        selected_choice.update(votes=F('votes')+1)

# Only <QuerySet> have attribute update
# Only Modle.object(like Question) have attribute save
# filter List <QuerySet [<Question: What's up?>]>
# get Object <Question: What's up?>

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))