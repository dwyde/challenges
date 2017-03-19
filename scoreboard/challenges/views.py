from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from challenges.models import Challenge

def index(request):
    return render(request, 'challenges/index.html')

def list_challenges(request):
    challenges = Challenge.objects.all()
    solved, points = Challenge.solved_by_user(request.user)
    context = {'challenges': challenges, 'solved': solved, 'points': points}

    return render(request, 'challenges/list.html', context)

def show_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, pk=challenge_id)

    if request.POST:
        # User is submitting a solution, let's check it.
        flag = request.POST.get('flag')

        if flag:
            message = challenge.check_flag(request.user, flag)
        else:
            message = 'Please submit a flag via HTTP POST.'

        context = {'challenge': challenge, 'message': message, 'flag': flag}
        return render(request, 'challenges/solve.html', context)

    else:
        # User is requesting challenge details only.

        if challenge.solved.filter(pk=request.user.pk):
            context = { 'challenge': challenge, 'solved': True }
        else:
            context = { 'challenge': challenge, 'solved': False }

        if challenge.instructions:
            context['instructions'] = "instructions/" + challenge.instructions + ".html"

        return render(request, 'challenges/show.html', context)
