import asyncio, pygame

async def run_client(client):
    clock = pygame.time.Clock()
    while client.running:
        if client.game_started:
            client.run_game()  # This blocks until the game ends
        else:
            client.draw_lobby()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    client.close()
                    return  # Avoid sys.exit to return to menu
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if client.input_text:
                            client.send_message(client.input_text)
                            client.input_text = ""
                        else:
                            client.toggle_ready()
                    elif event.key == pygame.K_BACKSPACE:
                        client.input_text = client.input_text[:-1]
                    elif event.unicode.isprintable():
                        client.input_text += event.unicode

        pygame.display.flip()
        await asyncio.sleep(1 / 60)

    client.close()
    return
