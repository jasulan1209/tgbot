"""
Запуск Admin API отдельно от бота.
Используется в docker-compose и при локальной разработке.
"""
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.admin_api.main:app",
        host="0.0.0.0",
        port=settings.ADMIN_API_PORT,
        reload=True,
        log_level="info",
    )
