import logging
import asyncio
import misc
import handlers


# ------------------------------------ENABLE LOGGING------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Высокий приоритет для httpx, чтобы все запросы GET и POST логировались
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
# ---------------------------------------------------------------------------------------


async def main() -> None:
    await misc.bot.delete_webhook(
        drop_pending_updates=True
    )  # Удаляем все обновления после выключения
    await misc.dp.start_polling(
        misc.bot, allowed_updates=misc.dp.resolve_used_update_types()
    )  # Отключаем обработку сообщений, полученных до включения


if __name__ == "__main__":
    asyncio.run(main())
