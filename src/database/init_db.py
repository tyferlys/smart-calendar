from sqlalchemy import select
from src.database.configDataBase import AsyncSessionLocal
from src.database.models.models import Owner, Service
import random
import string
import secrets

# Функция для генерации случайной строки
def generate_random_string(length: int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Функция для генерации случайного номера телефона
def generate_random_phone() -> str:
    return f"+7{random.randint(9000000000, 9999999999)}"

# Список осмысленных названий услуг
SERVICE_TITLES = [
    "Стрижка",
    "Массаж",
    "Маникюр",
    "Педикюр",
    "Косметологическая процедура",
    "Фитнес-тренировка",
    "Медитация",
    "Йога",
    "Уроки музыки",
    "Консультация психолога"
]

async def generate_random_service():
    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже существующие записи в таблице Service
        result = await session.execute(select(Service))
        existing_services = result.scalars().all()

        if existing_services:
            print("Сервисы уже существуют, новые сервисы не будут созданы.")
            return

        services = []
        for _ in range(3):
            title = random.choice(SERVICE_TITLES)  # Случайное название из списка
            cost = random.randint(50, 500)  # Генерация случайной стоимости
            duration = random.randint(15, 120)  # Генерация случайной длительности в минутах
            after_pause = random.randint(5, 30)  # Генерация времени после паузы в минутах
            
            new_service = Service(
                title=title,
                cost=cost,
                duration=duration,
                after_pause=after_pause
            )
            services.append(new_service)

        # Добавление в сессию и коммит
        session.add_all(services)
        await session.commit()

        return services

async def create_admin():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Owner))
        existing_admins = result.scalars().all()

        if existing_admins:  
            print("Администратор уже существует, новый администратор не будет создан.")
            return

        last_name = generate_random_string(5)
        first_name = generate_random_string(5)
        middle_name = generate_random_string(5)
        phone = generate_random_phone()
        password = 'root'  # Замените на генерируемый пароль, если необходимо
        token = secrets.token_hex(16)

        admin = Owner(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            phone=phone,
            password=password,
            token=token
        )

        session.add(admin)
        await session.commit()