from flask import Flask, render_template, redirect, url_for
from datetime import datetime, timedelta
import csv

app = Flask(__name__)

def poczatek_tygodnia(poczatek_semestru):
    poczatek_semestru = datetime.strptime(poczatek_semestru, '%d.%m.%Y')
    ilosc_dni_do_poczatku_tygodnia = (poczatek_semestru.weekday()) % 7
    data_poczatku_tygodnia = poczatek_semestru - timedelta(days=ilosc_dni_do_poczatku_tygodnia)

    return data_poczatku_tygodnia.strftime('%d.%m.%Y')

def koniec_tygodnia(koniec_semestru):
    koniec_semestru = datetime.strptime(koniec_semestru, '%d.%m.%Y')
    ilosc_dni_do_konca_tygodnia = (6 - koniec_semestru.weekday()) % 7
    data_konca_tygodnia = koniec_semestru + timedelta(days=ilosc_dni_do_konca_tygodnia)

    return data_konca_tygodnia.strftime('%d.%m.%Y')

def generowanie_dat(poczatek_kalendarza, koniec_kalendarza):
    poczatek_kalendarza = datetime.strptime(poczatek_kalendarza, '%d.%m.%Y')
    koniec_kalendarza = datetime.strptime(koniec_kalendarza, '%d.%m.%Y')

    lista_dat = []
    iteracja_dni = poczatek_kalendarza
    while iteracja_dni <= koniec_kalendarza:
        lista_dat.append(
            #calendar.day_name[iteracja_dni.weekday()],
            iteracja_dni.strftime('%d.%m.%Y')
        )
        iteracja_dni += timedelta(days=1)
    return lista_dat

def odczyt_terminarza():

    with open('zajecia.csv', newline='') as odczyt_csv:
        terminarz = csv.DictReader(odczyt_csv, delimiter=';')
        terminarz_zajecia = {}

        for linia in terminarz:
            dzien = linia['Data rozpoczęcia']
            zajecia = linia['Temat']
            lokalizacja = linia['Lokalizacja']
            czas_rozpoczecia = linia['Czas rozpoczęcia']
            czas_zakonczenia = linia['Czas zakończenia']

            zajecia_dane = {
                'Temat': zajecia,
                'Lokalizacja': lokalizacja,
                'Czas rozpoczęcia': czas_rozpoczecia,
                'Czas zakończenia': czas_zakonczenia,
            }

            if dzien in terminarz_zajecia:
                terminarz_zajecia[dzien].append(zajecia_dane)
            else:
                terminarz_zajecia[dzien] = [zajecia_dane]
    for dzien in terminarz_zajecia:
        terminarz_zajecia[dzien] = sorted(terminarz_zajecia[dzien], key=lambda x: datetime.strptime(x['Czas rozpoczęcia'],'%H:%M:%S'))

    return terminarz_zajecia

def uzupelnienie_dnia_zajec(poczatek_kalendarza, koniec_kalendarza):
    eventy = odczyt_terminarza()
    kalendarz = generowanie_dat(poczatek_kalendarza, koniec_kalendarza)
    pelny_kalendarz = {}

    godziny_zajec = [
        '08:00-09:35',
        '09:50-11:25',
        '11:40-13:15',
        '13:30-15:05',
        '15:45-17:20',
        '17:35-19:10',
        '19:25-21:00'
    ]

    for dzien in kalendarz:
        pelny_kalendarz[dzien] = [''] * 7

    for dzien in kalendarz:
        for i, przedmiot in enumerate(dzien):
            for event in eventy.get(dzien, []):
                poczatek_zajec = datetime.strptime(event['Czas rozpoczęcia'], '%H:%M:%S').time()
                koniec_zajec = datetime.strptime(event['Czas zakończenia'], '%H:%M:%S').time()

                if i < len(godziny_zajec):
                    for godziny_slotu in godziny_zajec[i].split('-'):
                        slot_godzina = datetime.strptime(godziny_slotu, '%H:%M').time()
                        if poczatek_zajec <= slot_godzina <= koniec_zajec:
                            pelny_kalendarz[dzien][i] = event

    return pelny_kalendarz

def dzielenie_kalendarza_na_siedem(kalendarz):
    lista_kaledarza = list(kalendarz.items())
    for i in range(0, len(lista_kaledarza), 7):
        yield dict(lista_kaledarza[i:i + 7])


@app.route('/')
def widok_kalendarza():
    #reczne wpisywanie daty poczatku i konca semestru
    poczatek_semestru = '01.10.2023'
    koniec_semestru = '25.02.2024'

    #funkcje obliczające pierwszy oraz ostatni dzien kalendarza, aby móc przedstawić go w przejrzysty sposób
    poczatek_kalendarza = poczatek_tygodnia(poczatek_semestru)
    koniec_kalendarza = koniec_tygodnia(koniec_semestru)
    kalendarz = uzupelnienie_dnia_zajec(poczatek_kalendarza, koniec_kalendarza)
    kalendarz = dzielenie_kalendarza_na_siedem(kalendarz)

    return render_template('terminarz.html', kalendarz=kalendarz)

@app.route('/<przycisk>')
def przekierowanie(przycisk):
    if przycisk == 'terminarz':
        return redirect(url_for('widok_kalendarza'))
    else:
        return redirect(url_for('widok_przedmiotu', przedmiot=przycisk))

@app.route('/przedmiot/<przedmiot>')
def widok_przedmiotu(przedmiot):

    return render_template('przedmiot.html', przedmiot=przedmiot)

if __name__ == '__main__':
    app.run(debug=True)