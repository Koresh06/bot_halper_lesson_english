from aiogram.fsm.state import State, StatesGroup



class StartSG(StatesGroup):
    start = State()
    name = State()
    age = State()
    phone = State()
    study_goal = State()
    has_studied_before = State()
    study_format = State()
    training_format = State()

