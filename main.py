# Никулин Максим 368594

import pyaudio, json, requests, random
from vosk import Model, KaldiRecognizer

rec = KaldiRecognizer(Model('vosk-model-small-ru-0.4'), 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

req = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/rub.json').json()
more = sum((1 for i in req['rub'].values() if i < 1))
less = sum((1 for i in req['rub'].values() if i > 1))

while True:
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data) and (len(data) > 0):
        question = json.loads(rec.Result())['text']
        if len(question) > 0:
            match question:
                case "доллар":
                    print(f"Курс рубля к доллару: {req['rub']['usd']}")
                case "евро":
                    print(f"Курс рубля к евро: {req['rub']['eur']}")
                case "лира":
                    print(f"Курс рубля к лире: {req['rub']['try']}")
                case "случайный":
                    rnd = random.choice(list(req['rub']))
                    print(f"Курс рубля к {rnd}: {req['rub'][rnd]}")
                case "дороже":
                    print(f"Количество валют дороже рубля: {more}")
                case "дешевле":
                    print(f"Количество валют дешевле рубля: {less}")
                case _:
                    print("Ошибка, повторите запрос.")
