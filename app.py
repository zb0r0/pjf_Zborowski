from flask import Flask, render_template
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
            iteracja_dni.strftime('%d.%m.%Y')  # Formatowanie dat do 'dd.mm.yyyy'
        )
        iteracja_dni += timedelta(days=1)
    return lista_dat

def odczyt_terminarza():

    with open('zajecia.csv', newline='') as zajecia_dane:
        terminarz = csv.reader(zajecia_dane, delimiter=';')

    return terminarz

def dzielenie_kalendarza_na_siedem(kalendarz):
    for i in range(0, len(kalendarz), 7):
        yield kalendarz[i:i + 7]

@app.route('/')
def widok_kalendarza():
    #reczne wpisywanie daty poczatku i konca semestru
    poczatek_semestru = '01.10.2023'
    koniec_semestru = '25.02.2024'

    #funkcje obliczające pierwszy oraz ostatni dzien kalendarza, aby móc przedstawić go w przejrzysty sposób
    poczatek_kalendarza = poczatek_tygodnia(poczatek_semestru)
    koniec_kalendarza = koniec_tygodnia(koniec_semestru)
    kalendarz = generowanie_dat(poczatek_kalendarza, koniec_kalendarza)
    kalendarz = dzielenie_kalendarza_na_siedem(kalendarz)

    with open('zajecia.csv', newline='') as zajecia_dane:
        terminarz = csv.reader(zajecia_dane, delimiter=';')
        zajecia = list(terminarz)

    return render_template('kalendarz.html', kalendarz=kalendarz, zajecia=zajecia)

if __name__ == '__main__':
    app.run(debug=True)
