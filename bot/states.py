from aiogram.dispatcher.filters.state import StatesGroup, State


class StartState(StatesGroup):
    choice = State()


class SearchState(StatesGroup):
    code = State()


class SoldCommitState(StatesGroup):
    code = State()
    size = State()
    quantity = State()
