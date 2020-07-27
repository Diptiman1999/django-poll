from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.views import generic
from .models import Question,Choice
from django.utils import timezone

# Create your views here.

# def index(request):
#     latest_question_list=Question.objects.order_by('-pub_Date')[:5]
#     # template = loader.get_template('poll/index.html')
#     context={
#         'latest_question_list':latest_question_list,
#     }
#     # return HttpResponse(template.render(context,request))
#     return render(request,'poll/index.html',context)
#
# def detail(request,question_id):
#     # try:
#     #     question=Question.objects.get(id=question_id)#In place id we can use pk
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request,'poll/detail.html',{'question':question})
#     question=get_object_or_404(Question,id=question_id)
#     return render(request,'poll/detail.html',{'question':question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'poll/results.html', {'question': question})


# Generic views
class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
    # """
    # Return the last five published questions (not including those set to be
    # published in the future).
    # """
        return Question.objects.filter(pub_Date__lte=timezone.now()).order_by('-pub_Date')[:5]
    #lte means less than equal to(Reverse serach)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'

    def get_queryset(self):
        # """
        # Excludes any questions that aren't published yet.
        # """
        return Question.objects.filter(pub_Date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))
