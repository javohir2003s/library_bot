from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from keyboards import contact_button, create_keyboard, menu_button
import states
import os
from database import create_user, get_user
from aiohttp import ClientSession



BACKEND_API = 'http://localhost:8000/api/v1/books'

async def start_command_reply(message: Message, bot: Bot, state: FSMContext) -> None:
    signed_user = get_user(telegram_id=message.from_user.id)
    if signed_user:
        await message.answer("Bosh sahifa")
    else:
        await bot.send_message(message.from_user.id, "Salom botga xush kelibsiz! Botdan foydalanish uchun ro'yxatdan o'ting", reply_markup=contact_button)
        await state.set_state(states.SignUp.username)

async def stop_command_state(message: Message, bot: Bot, state: FSMContext):
    this_state = await state.get_state()
    if this_state == "None":
        await message.answer("Bekor qilish uchun ariza mavjud emas")
    else:
        await state.clear()
        await message.answer("Joriy ariza bekor qilindi")


async def new_command_answer(message: Message, bot: Bot, state: FSMContext):
    if message.contact:
        await state.update_data(phone_number=message.contact.phone_number)
        if message.from_user.username:
            await state.update_data(username=message.from_user.username)
        if message.contact.first_name:
            await state.update_data(first_name=message.contact.first_name)
        if message.contact.last_name:
            await state.update_data(last_name=message.contact.last_name)

        user_id = message.contact.user_id
        user_photos = await bot.get_user_profile_photos(user_id=user_id)

        if user_photos.total_count > 0:
            photo = user_photos.photos[0][0]
            file = await bot.get_file(photo.file_id)
            file_path = file.file_path
            local_file_path = os.path.join('media', 'user_photo', f'{user_id}_photo.jpg')
            await state.update_data(photo=local_file_path)
            await bot.download_file(file_path, local_file_path)
        data = await state.get_data()
        user = create_user(
            telegram_id=user_id,
            first_name=data.get('first_name', None),
            last_name=data.get('last_name', None),
            phone_number=data.get('phone_number', None),
            username=data.get('username', None),
            photo_url=data.get('photo', None)
            )
        if user:
            menu = menu_button()
            await message.answer("Muvaffaqqiyatli ro'yxatdan o'tdingiz✅", reply_markup=menu)
            await state.clear()
        else:
            await message.answer("Ro'yxatdan o'tishda xatolik!", reply_markup=contact_button)
    else:
        await message.answer("Iltimos kontaktni ulashing", reply_markup=contact_button)





async def fetch_books(page):
    url = f"http://localhost:8000/api/v1/books?page={page}"
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json() 
            return None

current_page = 1

async def show_books_command(message: Message, bot: Bot):
    global current_page
    books_data = await fetch_books(page=current_page)

    if books_data and "results" in books_data:
        books = books_data['results']
        has_previous = books_data['previous']
        has_next = books_data['next']

        keyboard = create_keyboard(books=books, has_previous=has_previous, has_next=has_next)

        await message.answer("Kitoblardan birini tanlang", reply_markup=keyboard)
    
    else:
        await message.answer("Kitoblarni yuklashda xatolik yuz berdi.")


async def handle_message(message: Message, bot: Bot):
    global current_page
    if message.text == "🔙Oldingi":
        if current_page > 1:
            current_page -=1
    elif message.text == "Keyingi🔜":
        current_page +=1

    else:
        book_title = message.text
        books_data = await fetch_books(page=current_page)
        if books_data and "results" in books_data:
            book_info = next((b for b in books_data['results'] if b['title'] == book_title), None)
            if book_info:
                caption_text = (f"""
                        📚 **{book_info['title']}**\n\n{book_info['description'].strip()}\n\nNarxi: {book_info['price'].strip()}so'm\n\n
                    """

                )
                if len(caption_text) > 1024:
                    await message.answer(
                        caption_text[:1024],
                    )
                    await message.answer(caption_text[1024:])
                    return
                await message.answer(
                        caption_text
                    )
                return
        await message.answer("Kitob topilmadi.")
        return

    books_data = await fetch_books(page=current_page)
    if books_data and "results" in books_data:
        books = books_data['results']
        has_previous = books_data['previous']
        has_next = books_data['next']

        keyboard = create_keyboard(books=books, has_previous=has_previous, has_next=has_next)
        await message.answer("Kitoblardan birini tanlang:", reply_markup=keyboard)
    else:
        await message.answer("Kitoblarni yuklashda xatolik yuz berdi.")