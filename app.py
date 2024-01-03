from flask import Flask, render_template
import calendar

app = Flask(__name__)

class Dzien:
    def __init__(self, data, eventy):
        self.data = data
        self.eventy = eventy

    def __str__(self):
        return f"{self.data}: {', '.join(self.eventy)}"

def odczyt_terminarza(file_path):
    terminarz = []
    with open(file_path, 'r') as zajecia_dane:
        for line in zajecia_dane:
            terminarz.append(line.strip().split(','))
    return terminarz

@app.route('/')
def widok_kalendarza():
    poczatek_semestru = (2023, 10, 1)
    koniec_semestru = (2024, 2, 29)

    kalendarz = calendar.monthcalendar(poczatek_semestru[0], poczatek_semestru[1])

    pierwszy_tydzien = next((week for week in kalendarz if any(day != 0 for day in week)), None)
    if pierwszy_tydzien and pierwszy_tydzien[0] != 0:
        pierwszy_tydzien = [0] * (7 - len(pierwszy_tydzien)) + pierwszy_tydzien

    data_kalendarza = []
    aktualna_data = poczatek_semestru

    while aktualna_data <= koniec_semestru:
        tydzien = []

        for dzien in pierwszy_tydzien:
            if dzien == 0:
                tydzien.append('')
            else:
                data_str = f"{aktualna_data[0]}-{aktualna_data[1]:02d}-{dzien:02d}"
                eventy = dodawanie_eventow_do_dnia(data_str, odczyt_terminarza('zajecia.txt'))
                tydzien.append(eventy)

        data_kalendarza.append(tydzien)

        #Przesunięcie do pierwszego dnia następnego miesiąca
        if aktualna_data[1] == 12:
            aktualna_data = (aktualna_data[0] + 1, 1, 1)
        else:
            aktualna_data = (aktualna_data[0], aktualna_data[1] + 1, 1)

    return render_template('kalendarz.html', data_kalendarza=data_kalendarza)

def dodawanie_eventow_do_dnia(data_str, terminarz):
    for dzien in terminarz:
        if dzien[2] == data_str:  # Zmiana na indeks kolumny z datą
            return ', '.join(dzien)
    return ''

if __name__ == '__main__':
    app.run(debug=True)
