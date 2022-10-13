from django.shortcuts import render
from .models import Partie

def index(request):
    curent_user = request.user
    user = Partie.objects.filter(user=curent_user.id)
    dane = {'user': user}
    return render(request, "games.html", dane)


def partie(request, id):
    partie_user = Partie.objects.get(pk=id)
    dane = {'partie_user': partie_user}
    return render(request, "board/board.html", dane)