from aiogram.fsm.state import StatesGroup, State


class EntryAccountInKB(StatesGroup):
    entry_account_name = State()
    entry_account_amount = State()