from aiogram.fsm.state import State, StatesGroup


class VideoState(StatesGroup):
    waiting_overlay = State()
