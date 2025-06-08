import asyncio

HOST_ADDRESS = "localhost"  # Серверный адрес
PORT_NUMBER = 9090  # Серверный порт


async def run_echo_client():
    """
    Асинхронный клиент для подключения к серверу,
    отправки сообщений и получения ответов.
    """
    reader_stream = None
    writer_stream = None

    loop = asyncio.get_running_loop()

    try:
        # Пытаемся подключиться к серверу с повтором при ошибке подключения
        while True:
            try:
                reader_stream, writer_stream = await asyncio.open_connection(
                    HOST_ADDRESS, PORT_NUMBER
                )
                print(
                    f"Подключение к серверу {HOST_ADDRESS}:{PORT_NUMBER} успешно установлено."
                )
                break
            except ConnectionRefusedError:
                print(
                    f"Не удалось подключиться к {HOST_ADDRESS}:{PORT_NUMBER}. Попытка повторного подключения через 5 секунд..."
                )
                await asyncio.sleep(5)

        while True:
            # Получаем ввод пользователя без блокировки event loop
            message_to_send = await loop.run_in_executor(
                None, input, "Введите сообщение ('exit' — выход): "
            )
            if message_to_send.lower() == "exit":
                print("Закрываем соединение по запросу пользователя.")
                break

            # Отправляем сообщение серверу
            writer_stream.write(message_to_send.encode())
            await writer_stream.drain()

            # Получаем ответ от сервера
            server_response = await reader_stream.read(100)
            if not server_response:
                print("Соединение с сервером было закрыто.")
                break
            print(f"Ответ сервера: {server_response.decode()!r}")

    except KeyboardInterrupt:
        print("\nКлиент прерван пользователем (Ctrl+C).")
    except ConnectionResetError:
        print("Связь с сервером была неожиданно прервана.")
    finally:
        if writer_stream:
            writer_stream.close()
            await writer_stream.wait_closed()
        print("Клиент завершил работу.")


if __name__ == "__main__":
    asyncio.run(run_echo_client())
