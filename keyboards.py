from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

contact_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kontaktni ulashish☎️", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    is_persistent=True
)

def create_keyboard(books, has_previous, has_next):
    if has_previous and has_next:
        keyboard = ReplyKeyboardMarkup(
            keyboard=
                [
                    [KeyboardButton(text=book['title']) for book in books],
                    [KeyboardButton(text="🔙Oldingi"), KeyboardButton(text="Keyingi🔜")]
            ],
             resize_keyboard=True,
            is_persistent=True
        )
        return keyboard
    if has_next and has_previous is None:
        keyboard = ReplyKeyboardMarkup(
            keyboard=
                [
                    [KeyboardButton(text=book['title']) for book in books],
                    [KeyboardButton(text="Keyingi🔜")]
            ],
             resize_keyboard=True,
            is_persistent=True
        )
        return keyboard
    
    if has_next is None and has_previous:
        keyboard = ReplyKeyboardMarkup(
            keyboard=
                [
                    [KeyboardButton(text=book['title']) for book in books],
                    [KeyboardButton(text="🔙Oldingi")]
            ],
            resize_keyboard=True,
            is_persistent=True
        )
        return keyboard
    

def menu_button():
    keyboard= InlineKeyboardMarkup(
        keyboard=[
            [InlineKeyboardButton(text="Kitoblar ro'yxati", callback_data='books')],
            [InlineKeyboardButton(text='Yordam', callback_data='help')]
        ],
        resize_keyboard=True,
        is_persistent=True
    )
    return keyboard