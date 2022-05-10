import json
from time import sleep
from random import randint as r
import requests
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
import schedule
from threading import Thread
bot = Bot(token='687742c312f7366ead0d96a0b2a2474950b6c6b97fa88cc8be8c0293093f8fceb1f5411d4f6a9a5baf5da')
qiwi_token = "27ead4bbc09c4e46edd8a695831602ce"
def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def update_money():
    import json
    with open('base.json', 'r') as f:
        templates = json.load(f)
        f.close()
    for i in templates["users"]:
        for j in range(len(list(i.values()))):
            print(list(i.values())[j][1])
        break
    with open("base.json", 'w') as f:
        json.dump(templates, f)
        f.close()
schedule.every().day.at("00:00").do(update_money)
@bot.on.message(text='Начать')
async def main(message: Message):
    with open('base.json', 'r') as f:
        templates = json.load(f)
        f.close()
    ref = str(message).split()
    ind = ref[22]
    ind = ind.split('=')
    ind = ind[1]
    user_info = await bot.api.users.get(message.from_id)
    id = str(user_info[0]).split()
    id = id[4].split('=')
    id = id[1]
    need = templates.values()

    for i in need:
        ned = i[0]
        inv = i[1]
        break
    if id not in ned.keys():
        for i in templates.values():
            for i in need:
                i[1] += 1
            ind = ind[1:-1]

            try:
                ned[ind][3] += 1
                ned[ind][0] += 3
            except:
                pass
            ned[id] = [0, 0, ind, 0, 'Start', -1,'']
        with open("base.json", 'w') as f:
            json.dump(templates, f)
            f.close()

    await message.answer(
        "Привет!\n\n Ты попал в Invest infinity🔥\n\n У нас ты сможешь заработать без вложений 💵\n\n Telegram https://vk.cc/cdqlAe с новостями, подпишись 😉")
    await message.answer(
        message=("Выберите пункт меню"),
        keyboard=(
            Keyboard(one_time=False, inline=False)
                .add(Text('🔥Инвестировать'), color=KeyboardButtonColor.POSITIVE)
                .add(Text('Профиль'), color=KeyboardButtonColor.POSITIVE)
                .row()
                .add(Text('Пополнить баланс'), color=KeyboardButtonColor.PRIMARY)
                .add(Text('Вывод средств'), color=KeyboardButtonColor.PRIMARY)
        )
    )


@bot.on.message(text='🔥Инвестировать')
async def invest(message: Message):
    with open('base.json', 'r') as f:
        templates = json.load(f)
        f.close()
    user_info = await bot.api.users.get(message.from_id)
    id = str(user_info[0]).split()
    id = id[4].split('=')
    id = id[1]
    for i in templates.values():
        ned = i[0]
        ned[id][4] = 'Invest'
    for i in templates.values():
        ned = i[0]
        balance = ned[id][0]
        invested = ned[id][1]
    with open('base.json', 'w') as f:
        json.dump(templates, f)
        f.close()

    await message.answer(
        f"💵 Вы можете инвестировать: {str(balance)}₽\n💵 Баланс инвестиций: {str(invested)}₽\n\n👉 Введите сумму для инвестирования:")


@bot.on.message(text="Профиль")
async def profile(message: Message):
    with open('base.json', 'r') as f:
        templates = json.load(f)
        f.close()
    user_info = await bot.api.users.get(message.from_id)
    id = str(user_info[0]).split()
    id = id[4].split('=')
    id = id[1]
    for i in templates.values():
        investors = i[1]
        ned = i[0]
        ned[id][4] = 'Invest'
        balance = ned[id][0]
        invested = ned[id][1]
        refs = ned[id][3]
        znach = ned[id][5]
    if balance + invested < 3:
        check = "0.00"
    else:
        check = balance + invested
    ref_link = f'https://vk.com/write-212897234?ref={id}'

    comment_need = f'{id}-{str(int(znach) + 1)}'
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + qiwi_token
    s.headers['Accept'] = "application/json"
    parameters = {'rows': 50, 'operation': "IN"}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + "79772824069 " + '/payments', params=parameters)

    reply = h.json()["data"]
    for transaction in reply:
        if transaction["comment"] == comment_need:
            if transaction["status"] == 'SUCCESS':
                for i in templates.values():
                    ned = i[0]
                    ned[id][0] += int(transaction["sum"]["amount"])
                    ned[id][5] += 1
                with open('base.json', 'w') as f:
                    json.dump(templates, f)
                    f.close()

    await message.answer(
        f"💵Ваш баланс: {balance}₽\n💵Доход в сутки: {invested * 0.1}₽\n💵Инвестировано: {invested}₽\n💵Баланс для вывода: {check}₽\n\n👤Инвесторов: {investors} человек\n🔥Статус: Игрок\n\n🗣Платим за реферала - 3₽\n\n🗣Количество рефералов:{refs} человек\n\n🗣Ваша реф.ссылка:{ref_link} ")


@bot.on.message(text="Пополнить баланс")
async def donate(message: Message):
    user_info = await bot.api.users.get(message.from_id)
    id = str(user_info[0]).split()
    id = id[4].split('=')
    id = id[1]
    with open('base.json', 'r') as f:
        templates = json.load(f)
        f.close()
    for i in templates.values():
        ned = i[0]
        ned[id][4] = 'Donate'
    with open('base.json', 'w') as f:
        json.dump(templates, f)
        f.close()
    await message.answer("Введите сумму для инвестирования")

@bot.on.message(text="Вывод средств")
async def withdraw(message: Message):
    user_info = await bot.api.users.get(message.from_id)
    id = str(user_info[0]).split()
    id = id[4].split('=')
    id = id[1]
    with open('base.json', 'r') as f:
        templates = json.load(f)
        f.close()
    for i in templates.values():
        ned = i[0]
        ned[id][4] = 'Withdraw'
    with open('base.json', 'w') as f:
        json.dump(templates, f)
        f.close()
    await message.answer("Внимание! Вывод происходит только на платежную систему Qiwi\nВведите ваш номер телефона (7xxxxxxxxxx)")


@bot.on.message()
async def check_sums(message: Message):
    try:
        a = int(message.text)
    except:
        return 0
    with open('base.json', 'r') as f:
        templates = json.load(f)
        f.close()
    user_info = await bot.api.users.get(message.from_id)
    id = str(user_info[0]).split()
    id = id[4].split('=')
    id = id[1]
    for i in templates.values():
        ned = i[0]
        balance = ned[id][0]
        invested = ned[id][1]
        check = ned[id][4]
        znach = ned[id][5]
        znach = str(int(znach)+1)
    if check == 'Donate':
        Qiwi_phone = "79772824069"
        kop = "00"
        comment = f'{id}-{znach}'
        url = f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={Qiwi_phone}&amountInteger={a}&" \
              f"amountFraction={kop}&extra%5B%27comment%27%5D={comment}&currency=643&blocked[0]=account&blocked[1]=comment&blocked[2]=sum&extra%5B%27accountType%27%5D=nickname"
        await message.answer(url)
    elif check == "Withdraw":
        for i in templates.values():
            ned = i[0]
            ned[id][6] = message.text
            ned[id][4] = "final_withdraw"
        with open('base.json', 'w') as f:
            json.dump(templates, f)
            f.close()
        await message.answer("Введите сумму для вывода")
    elif check == "final_withdraw":
        if float(message.text) > balance:
            await message.answer(f"Ошибка! На вашем счету недостаточно средств. У вас {invested} рублей")
            return 0
        elif float(message.text) < 15:
            await message.answer("Ошибка! Минимальная сумма вывода - 15 рублей")
            return 0
        for i in templates.values():
            ned = i[0]
            tel = ned[id][6]
            ned[id][1]-=int(message.text)
            ned[id][4]=''
        await message.answer("Ваша заявка принята. Ожидайте")
        await bot.api.messages.send(
            peer_id=521775887,
            random_id=int(r(1,10**10)),

            message=f"Тел:{tel}\nСумма:{message.text}"
        )
        with open('base.json', 'w') as f:
            json.dump(templates, f)
            f.close()
        return 0
    elif check == "Invest":

        if float(message.text) > balance:
            await message.answer("Ошибка, на вашем счету недостаточно средств")
            return 0
        elif float(message.text) < 15:
            await message.answer("Ошибка, минимальная сумма инвестиций составляет 15 рублей")
            return 0
        else:
            ned[id][0] -= float(message.text)
            ned[id][1] += float(message.text)
            ned[id][4] = ''
            await message.answer("Успешно!")
            with open('base.json', 'w') as f:
                json.dump(templates, f)
                f.close()


if __name__ == "__main__":
    scheduleThread = Thread(target=schedule_checker)
    scheduleThread.daemon = True
    scheduleThread.start()
    bot.run_forever()
