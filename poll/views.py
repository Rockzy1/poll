from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from .forms import VoteForm
from django.contrib.auth.decorators import login_required


def home(request):
    questions = Question.objects.all().order_by('-pub_date')
    return render(request, 'poll/home.html', {'questions': questions})

from .models import Question, VoteRecord

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Check if user already voted
    if VoteRecord.objects.filter(user=request.user, question=question).exists():
        return redirect('result', question_id=question.pk)

    form = VoteForm(question, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            selected_choice = form.cleaned_data['choice']
            selected_choice.votes += 1
            selected_choice.save()

            # Record the vote
            VoteRecord.objects.create(
                user=request.user,
                question=question,
                choice=selected_choice
            )
            return redirect('result', question_id=question.pk)

    return render(request, 'poll/vote.html', {'question': question, 'form': form})


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/result.html', {'question': question})

