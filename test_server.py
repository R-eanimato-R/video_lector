# test_server.py
from app.database import engine
from app.models import Base

print("🔍 Проверяем подключение к БД...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы, БД подключена!")
except Exception as e:
    print(f"❌ Ошибка: {e}")