import asyncio

SERVER_HOST = "localhost"  # Адрес сервера
SERVER_PORT = 9090  # Порт сервера


async def async_echo_client():
    """
    Асинхронная функция для установления соединения с сервером,
    отправки сообщений и получения ответов.
    """
    reader = None
    writer = None

    event_loop = asyncio.get_running_loop()

    try:
        # Попытка подключения к серверу с повтором при неудаче
        while True:
            try:
                reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
                print(f"Успешно подключено к {SERVER_HOST}:{SERVER_PORT}")
                break
            except ConnectionRefusedError:
                print(
                    f"Ошибка подключения к {SERVER_HOST}:{SERVER_PORT}. Повтор через 5 секунд..."
                )
                await asyncio.sleep(5)

        while True:
            # Получаем пользовательский ввод без блокировки основного цикла
            user_msg = await event_loop.run_in_executor(
                None, input, "Введите сообщение (для выхода введите 'exit'): "
            )
            if user_msg.lower() == "exit":
                print("Инициировано завершение соединения.")
                break

            # Отправляем введённое сообщение на сервер
            writer.write(user_msg.encode())
            await writer.drain()

            # Ожидаем ответ от сервера
            response = await reader.read(100)
            if not response:
                print("Соединение с сервером было закрыто.")
                break
            print(f"Эхо от сервера: {response.decode()!r}")

    except KeyboardInterrupt:
        print("\nПрервано пользователем (Ctrl+C).")
    except ConnectionResetError:
        print("Связь с сервером разорвана.")
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()
        print("Клиент завершил работу.")


if __name__ == "__main__":
    asyncio.run(async_echo_client())
