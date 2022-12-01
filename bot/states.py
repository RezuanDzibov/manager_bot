from aiogram.dispatcher.filters.state import StatesGroup, State


class StartState(StatesGroup):
    choice = State()


class SearchState(StatesGroup):
    code = State()


class SoldCommitState(StatesGroup):
    code = State()
    size = State()
    quantity = State()


class ProductAddState(StatesGroup):
    name = State()
    color = State()
    quantity = State()
    pack_quantity = State()
    wholesale_price = State()
    retail_price = State()
    supply_date = State()
    sizes = State()


class ProductAddImagesState(StatesGroup):
    image = State()
