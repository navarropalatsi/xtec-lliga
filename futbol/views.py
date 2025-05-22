from django.shortcuts import render, redirect
from django import forms
from .models import Lliga


# Create your views here.
def classificacio(request, lliga_id):
    # Aquí podríem fer una consulta a la base de dades per obtenir la classificació
    # de la lliga amb id=lliga_id
    # Per exemple:
    lliga = Lliga.objects.get(id=lliga_id)
    equips = lliga.equips.all()
    # i passar-los al context del template

    classi = []

    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partits.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partits.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        classi.append((punts, equip.nom))
    # ordenem llista
    classi.sort(reverse=True)
    return render(request, 'futbol/classificacio.html', {'classificacio': classi, 'lliga': lliga})


class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())

def classificacio_menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect("futbol:classificacio", lliga_id=lliga.id)
    return render(request, "futbol/classificacio_menu.html", {"form": form})