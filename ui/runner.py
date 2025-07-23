import asyncio, pygame


# Asynchronous main loop for the client
async def run_client(client):
    clock = pygame.time.Clock()  # Used to control frame rate
    while client.running:  # Loop while the client is active
        if client.game_started:
            client.run_game()  # Blocking call: handles game logic until it ends
        else:
            client.draw_lobby()  # Render the lobby UI

            # Handle all user input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    client.close()  # Clean up resources
                    return  # Exit without terminating the full app
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if client.input_text:
                            client.send_message(client.input_text)  # Send chat/input message
                            client.input_text = ""  # Clear input
                        else:
                            client.toggle_ready()  # Toggle ready status
                    elif event.key == pygame.K_BACKSPACE:
                        client.input_text = client.input_text[:-1]  # Delete last character
                    elif event.unicode.isprintable():
                        client.input_text += event.unicode  # Append typed character

        pygame.display.flip()  # Update display
        await asyncio.sleep(1 / 60)  # Cap loop to ~60 FPS

    client.close()  # Ensure client cleanup
    return
