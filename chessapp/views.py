from django.shortcuts import render
from django.views.generic import CreateView
from .models import Partie
from .forms import GameForm
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    current_user = request.user
    user = Partie.objects.filter(user=current_user.id)
    dane = {'user': user}
    return render(request, "games.html", dane)


def partie(request, id):
    partie_user = Partie.objects.get(pk=id)
    dane = {'partie_user': partie_user}
    return render(request, "board/board.html", dane)


class AddPostView(LoginRequiredMixin, CreateView):

    model = Partie
    form_class = GameForm
    template_name = 'board/Game.html'

    def game_form(self, request):
        if request.method == "POST":
            form = GameForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = GameForm()
            return render(request, "board/Game.html", {'form': form})

    def get_initial(self):
        return {'user': self.request.user}