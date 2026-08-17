from aiogram import Router,F,Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from aiogram.filters import CommandStart,Command

import asyncio
from nutrition_database import get_nutrition
from yolo import detect_photo
from aiogram import Router


calories = Router()

class CalorieState(StatesGroup):
    waiting_for_weght = State()



@calories.message(F.photo)
async def handle_photo(message:Message,bot:Bot,state:FSMContext):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    save_path = f"temp/{photo.file_id}.jpg"
    await bot.download_file(file.file_path,save_path)
    
    detected_classes = detect_photo(save_path)
    if not detected_classes:
        await message.answer("I can't recognize the photo 😢")
        return
    
    await state.update_data(detected_classes=detected_classes)
    await state.set_state(CalorieState.waiting_for_weght)
    await message.answer(f"Recognized: {','.join(detected_classes)}\nEnter weight in grams:")

@calories.message(CalorieState.waiting_for_weght)
async def handle_weight(message:Message,state:FSMContext):
    try:
        weight = int(message.text)
    except ValueError:
        await message.answer("Please enter a number🔢")
        return
    
    data = await state.get_data()
    reply_lines = []
    for cls in data["detected_classes"]:
        nutrition = get_nutrition(cls)
        if nutrition and nutrition["calories"]:
            total_kcal = nutrition["calories"] * weight/100
            reply_lines.append(f"• {cls}: {total_kcal:.0f} kcal ({weight}g)")
        else:
            reply_lines.append(f"• {cls}: No data in database")
    
    await message.answer("\n".join(reply_lines))
    await state.clear()