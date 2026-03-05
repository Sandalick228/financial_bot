from aiogram.fsm.state import StatesGroup, State


class AdditionAccount(StatesGroup):
    entering_the_top_up_amount = State()


class SubtractAccount(StatesGroup):
    entering_the_deduction_amount = State()



