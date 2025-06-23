from django.shortcuts import render, redirect
from django import forms
from .models import Lliga

def index(request):
    return render(request, 'lliga/index.html')

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


def taula_partits(request, lliga_id):
    # Aquí podríem fer una consulta a la base de dades per obtenir la classificació
    # de la lliga amb id=lliga_id
    # Per exemple:
    lliga = Lliga.objects.get(id=lliga_id)
    partits = lliga.partits.all()
    equips = lliga.equips.all()
    resultats = {}
    for local in equips:
        fila_local = {"local": local, "resultats": {}}
        for visitant in equips:
            # busquem el partit entre local i visitant
            partit = lliga.partits.filter(local=local, visitant=visitant).first()
            if partit:
                # si existeix, afegim el resultat
                fila_local["resultats"][visitant.nom] = {
                    "gols_local": partit.gols_local(),
                    "gols_visitant": partit.gols_visitant()
                }
            else:
                # si no existeix, afegim un resultat buit
                fila_local["resultats"][visitant.nom] = None

        resultats[local.nom] = fila_local

    # i passar-los al context del template
    return render(
        request, "futbol/taula_partits.html", {"resultats": resultats, "lliga": lliga}
    )


class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())


def taula_partits_menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /taula_partits/<lliga_id>
            return redirect("futbol:taula_partits", lliga_id=lliga.id)
    return render(request, "futbol/taula_partits_menu.html", {"form": form})


def classificacio_menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect("futbol:classificacio", lliga_id=lliga.id)
    return render(request, "futbol/classificacio_menu.html", {"form": form})
