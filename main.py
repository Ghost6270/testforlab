import random
import os
import pickle

dir = os.path.abspath(os.curdir)
balance = pickle.load(open("config/balance.txt", "rb"))

totalcardplayer = []
totalcardbot = []

total = 0
totalbot = 0
timebot = 1
time = 1
secondcardbot = ""


def isint(request):
    while True:
        try:
            value = int(input(request))
            return value
            break
        except(ValueError):
            print("Введено не число")
            continue


def truevalue(request):
    while True:
        request = request + "(Да/Нет): "
        value = input(request)
        if value in ("Да", "да"):
            return True
        elif value in ("нет", "Нет"):
            return False
        else:
            print("Ответ указан некорректно")
            continue
        break


def game():
    global bet
    global total
    global balance
    global time
    global totalcard

    while True:
        maste = random.randint(1, 4)
        number = random.randint(0, 8)

        if maste == 1:
            maste = "Бубна"
        elif maste == 2:
            maste = "Черви"
        elif maste == 3:
            maste = "Крести"
        else:
            maste = "Пика"

        numbercard = dec[maste][number]
        if numbercard == 0: continue
        dec[maste][number] = 0
        break

    if numbercard == 2:
        cardname = "Валет"
    elif numbercard == 3:
        cardname = "Дама"
    elif numbercard == 4:
        cardname = "Король"
    elif numbercard == 11:
        cardname = "Туз"
    else:
        cardname = numbercard
    while True:
        if numbercard == 11:
            numbercard = isint("Вам выпал туз, какое значение ему присвоить? (1/11): ")

            if numbercard not in (1, 11):
                print("Введите число 1 или 11")
                numbercard = 11
                continue
        break
    text = "Ваша " + str(time) + " карта: " + str(cardname) + " " + maste + "(" + str(numbercard) + ")"
    print(text)
    totalcardplayer.append(text)
    total += numbercard
    print("Сумма очков:", total, "\n")
    time += 1
    if time == 2:
        game()


def botgame():
    global totalbot
    global timebot
    global secondcardbot
    while True:
        while True:
            maste = random.randint(1, 4)
            number = random.randint(0, 8)
            if maste == 1:
                maste = "Бубна"
            elif maste == 2:
                maste = "Черви"
            elif maste == 3:
                maste = "Крести"
            else:
                maste = "Пика"
            numbercard = dec[maste][number]
            if numbercard == 0: continue
            dec[maste][number] = 0
            break
        if numbercard == 2:
            cardname = "Валет"
        elif numbercard == 3:
            cardname = "Дама"
        elif numbercard == 4:
            cardname = "Король"
        elif numbercard == 11:
            cardname = "Туз"
        else:
            cardname = numbercard
        if numbercard == 11 and totalbot > 10:
            numbercard = 1
        if timebot != 2:
            text = str(timebot) + " карта у дилера: " + str(cardname) + " " + str(maste) + "(" + str(numbercard) + ")"
            print(text)
        else:
            print(timebot, "карта у дилера перевернута.\n")
            secondcardbot = str(cardname) + " " + str(maste)+ "(" + str(numbercard) + ")"
        totalcardbot.append(str(cardname) + " " + str(maste)+ "(" + str(numbercard) + ")")
        totalbot += numbercard
        timebot += 1
        if timebot == 2:
            botgame()
        break


# старт проги

print("Привет, ты зашел в игру 21")
print("Правила игры: ")
while True:
    difficulty = isint("Введите уровень сложности (1/2): ")
    if difficulty not in (1, 2):
        print("Введите число от 1 до 2х.")
        continue
    break

print("Ваш баланс текущий баланс:", balance)
addbal = isint("Это тестовая версия, доступно добавление денег. Введите значение, которое хотите добавить: ")
balance += addbal
pickle.dump(balance, open("config/balance.txt", "wb"))

while True:
    dec = pickle.load(open("config/dec.txt", "rb"))
    print("Ваш баланс текущий баланс:", balance)
    while True:
        bet = isint("Введите ставку на матч: ")
        if bet <= 0:
            print("Введите число больше 0")
            continue
        elif bet > balance:
            print("У вас нет столько денег, ваш баланс:", balance)
            continue
        break

    print("Начинаем игру... дилер перемешивает колоду и дает вам 2 карты.\n")
    game()
    botgame()
    while True:
        if truevalue("Хотите взять ещё карту?"):
            game()
            continue
        else:
            break
    print("Диллер переворачивает вторую карты и там", secondcardbot)
    while totalbot < 17:
        botgame()

    if difficulty == 2:
        while 21 >= total > totalbot:
            botgame()
    print("Кол во очков", total)
    print("Кол во очков у дилера", totalbot, "\n")
    if total > 21 and totalbot > 21:
        print("Ничья, у всех перебор")
    elif total > 21 and totalbot <= 21:
        print("Вы проиграли, у вас перебор")
        balance -= bet
    elif total <= 21 and totalbot > 21:
        print("Вы выиграли, у дилера перебор.")
        balance += bet
    elif total == totalbot:
        print("Ничья, у вас одинаковое количество очков с дилером")
    elif total < totalbot and totalbot <= 21:
        print("Вы проиграли.")
        balance -= bet
    elif total > totalbot and total <= 21:
        print("Вы выиграли")
        balance += bet
    pickle.dump(balance, open("config/balance.txt", "wb"))
    print("Ваш баланс:", balance, '\n')
    while True:
        if truevalue("Хотите увидеть краткий отчет по игре?"):
            b = 1
            print("Краткая сводка по игре: ")
            for b in range(0, len(totalcardplayer)):
                print("Ваша", b + 1, "карта:", totalcardplayer[b])
            print("Ваше количество очков:", total)
            print("\n")
            for b in range(0, len(totalcardbot)):
                print(b + 1, "карта дилера:", totalcardbot[b])
            print("Количество очков дилера:", totalbot)
            break
        else:
            break

    if truevalue("Хотите сыграть ещё раз?"):
        totalbot = 0
        total = 0
        timebot = 1
        time = 1
        totalcardplayer = []
        totalcardbot = []
        continue
    else:
        break
print("Очень жаль, что вы так быстро(")
input("Нажмите Enter для закрытия программы")
