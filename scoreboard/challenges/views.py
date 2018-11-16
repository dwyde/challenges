from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from challenges.models import Challenge

def index(request):
    return render(request, 'challenges/index.html')

def list_challenges(request):
    challenges = Challenge.objects.all()
    solved = request.session.get('solved', [])
    points = Challenge.total_points(solved)
    context = {
        'challenges': challenges, 'solved': set(solved), 'points': points
    }
    return render(request, 'challenges/list.html', context)

def show_challenge(request, challenge_name):
    challenge = get_object_or_404(Challenge, name=challenge_name)

    if request.POST:
        # The user is submitting a solution, let's check it.
        flag = request.POST.get('flag')
        if flag:
            message = challenge.check_flag(request.session, flag)
        else:
            message = 'Please submit a flag via HTTP POST.'

        context = {'challenge': challenge, 'message': message, 'flag': flag}
        return render(request, 'challenges/solve.html', context)
    else:
        # User is requesting challenge details only.
        if challenge.id in request.session.get('solved', []):
            context = {'challenge': challenge, 'solved': True}
        else:
            context = {'challenge': challenge, 'solved': False}
        return render(request, 'challenges/show.html', context)

