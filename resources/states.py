# Состояния для FSM и клавиатур
from aiogram.fsm.state import State, StatesGroup


# Выбор кастомной категории затрат
class CustomCategories(StatesGroup):
    wait_name = State()
    choose_to_change = State()


# Добавление/выбор скидочной карты
class DiscountCard(StatesGroup):
    wait_photo = State()
    wait_name = State()


# Предоставление доступка к таблице
class TableAccess(StatesGroup):
    wait_email = State()


# Выбор категории при вручном внесении траты
class ChooseCategory(StatesGroup):
    wait_category = State()
