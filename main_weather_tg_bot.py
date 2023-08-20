import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши мне название города и я пришлю сводку погоды!')
    
@dp.message_handler()    
async def get_weather(message: types.Message):
    
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        
        city = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        
        await message.reply(f"Погода в городе: {city}\nТемпература: {cur_weather}℃\nВлажность: {humidity}%\nДавление: {pressure} мм рт. ст.\nСкорость ветра: {wind} м/с\nВремя восхода: {sunrise_timestamp}\nВремя заката: {sunset_timestamp}\nХорошего дня!")
        
        
    except:
        await message.reply('Проверьте название города')    
    
    
if __name__ == '__main__':
    executor.start_polling(dp)