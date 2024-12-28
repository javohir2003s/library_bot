from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class SignUp(StatesGroup):
    username = State()
    first_name = State()
    last_name = State()
    phone_number = State()
    photo = State()