from aiogram.fsm.state import State, StatesGroup



class StartSG(StatesGroup):
    start = State()
    name = State()
    age = State()
    phone = State()
    study_format = State()
    has_studied_before = State()

