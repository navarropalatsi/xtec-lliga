from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint
import datetime

from ...models import *

faker = Faker(["es_CA","es_ES"])

class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'

    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)

    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lligues = Lliga.objects.filter(nom=titol_lliga)
        if lligues.count()>0:
            print("La lliga {} ja existeix. Esborrant equips i jugadors...".format(titol_lliga))
            for lliga in lligues.all():
                for equip in lliga.equips.all():
                    for jugador in equip.jugadors.all():
                        print("Esborrem el jugador {}".format(jugador.nom))
                        jugador.delete()
                    print("Esborrem l'equip {}".format(equip.nom))
                    equip.delete()
                lliga.delete()
            
            # print("Aquesta lliga ja està creada. Posa un altre nom.")
            # return

        print("Creem la nova lliga: {}".format(titol_lliga))
        inici_lliga = faker.date_between(start_date=datetime.date(1950,1,1), end_date=faker.date_time_this_century())
        fi_lliga = inici_lliga + timedelta(days=300)
        lliga = Lliga( nom=titol_lliga, temporada="temporada", data_inici=inici_lliga, data_fi=fi_lliga)
        lliga.save()

        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            equip = Equip(ciutat=ciutat,nom=nom, fundacio=randint(1850,2025))
            # print(equip)
            equip.save()
            lliga.equips.add(equip)

            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.first_name()
                cognoms = faker.last_name()
                data_naixement = faker.date_of_birth(minimum_age=15, maximum_age=45)
                nacionalitat = faker.country()
                dorsal = randint(1,99)

                if dorsal == 1 or dorsal == 13:
                    posicio = "porter"
                else:
                    posicio = "jugador"

                jugador = Jugador(nom=nom, cognoms=cognoms, posicio=posicio,
                    data_naixement=data_naixement, dorsal=dorsal, nacionalitat=nacionalitat,equip=equip)
                # print(jugador)
                jugador.save()

        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local!=visitant:
                    partit = Partit(local=local,visitant=visitant)
                    partit.local = local
                    partit.visitant = visitant
                    partit.lliga = lliga
                    partit.data = faker.date_time_between(
                        start_date=lliga.data_inici,
                        end_date=lliga.data_fi,
                        tzinfo=timezone.get_current_timezone()
                    )
                    partit.save()

                    for i in range(randint(0,20)):
                        tipus = faker.random_element(elements=Event.TIPUS_EVENT)[0]
                        local_o_visitant = faker.random_element(elements=["local","visitant"])
                        if local_o_visitant == "local":
                            equip = local
                        else:
                            equip = visitant
                        jugador = faker.random_element(elements=equip.jugadors.all())

                        event = Event(tipus=tipus, partit=partit, temps=faker.date_time_between(start_date=partit.data, end_date=partit.data + timedelta(minutes=90), tzinfo=timezone.get_current_timezone()), jugador=jugador, equip=equip)
                        event.save()

