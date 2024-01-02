from flask import Flask
import calendar

app = Flask(__name__)

class Dzien:
    def __init__(self, data, eventy):
        self.data = data
        self.eventy = eventy

    def __str__(self):
        return f"{self.data}: {','.join(self.eventy)}"

def odczyt_terminarza():
    terminarz = []
    with open("zajecia.txt") as zajecia_dane:
        for line in zajecia_dane:
            terminarz.append(line)
    return terminarz

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
