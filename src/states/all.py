from aiogram.fsm.state import StatesGroup, State


class EntryAccountInKB(StatesGroup):
    add_an_invoice = State()
    entry_account = State()