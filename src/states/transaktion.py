from aiogram.fsm.state import StatesGroup, State


class AdditionAccountInKB(StatesGroup):
    addition_account_one = State()
    addition_account_two = State()
    addition_account_three = State()
    addition_account_four = State()
