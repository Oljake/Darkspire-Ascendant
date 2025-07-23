import pygame, asyncio, sys
from network.server import get_local_ip, get_public_ip, is_port_open
from network.async_utils import start_server
from network.client import ClientApp
from ui.runner import run_client
from network.config import PORT

async def main_menu():
    pygame.init()
    pygame.key.set_repeat(500, 50)  # Enable key repeat: 500ms delay, 50ms interval
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Game Menu")
    font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)
    options = ["Singleplayer", "Multiplayer"]
    button_rects = [pygame.Rect(200, 200 + i * 80, 200, 50) for i in range(len(options))]
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            print("Singleplayer mode (not implemented)")
                        elif i == 1:
                            await multiplayer_menu(screen)
                            screen = pygame.display.set_mode((600, 600))
                            pygame.display.set_caption("Game Menu")

        screen.fill((30, 30, 30))
        for i, option in enumerate(options):
            rect = button_rects[i]
            is_hovered = rect.collidepoint(mouse_pos)
            bg_color = (0, 100, 0) if is_hovered else (50, 50, 50)
            text_color = (255, 255, 255) if is_hovered else (200, 200, 200)
            pygame.draw.rect(screen, bg_color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
            surf = button_font.render(option, True, text_color)
            text_rect = surf.get_rect(center=rect.center)
            screen.blit(surf, text_rect)
        pygame.display.flip()

    pygame.quit()

async def multiplayer_menu(screen):
    pygame.display.set_caption("Multiplayer Menu")
    font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)
    options = ["Create Server", "Join Server", "Back"]
    button_rects = [pygame.Rect(200, 200 + i * 80, 200, 50) for i in range(len(options))]
    server_loop = None
    server = None
    state = "main"
    input_active = False
    input_text = ""
    input_type = None
    ip_input_text = ""
    username_input_text = ""
    error_message = ""
    running = True

    host_rect = pygame.Rect(150, 400, 150, 50)
    join_rect = pygame.Rect(150, 400, 150, 50)
    back_rect = pygame.Rect(310, 400, 150, 50)
    input_rect = pygame.Rect(50, 250, 500, 40)  # Username input for create_server
    ip_input_rect = pygame.Rect(50, 250, 500, 40)  # IP input for join_server
    username_input_rect = pygame.Rect(50, 350, 500, 40)  # Username input for join_server

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if server_loop and server:
                    server.close()
                    server_loop.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "main":
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(mouse_pos):
                            if i == 0:
                                if is_port_open(PORT):
                                    error_message = f"Port {PORT} already in use. Cannot start server."
                                else:
                                    try:
                                        server_loop, server = start_server()
                                        local_ip = get_local_ip()
                                        public_ip = get_public_ip()
                                        print(
                                            f"Server started on:\n"
                                            f"Local IP: {local_ip}:{PORT}\n"
                                            f"Public IP: {public_ip}:{PORT}\n\n"
                                            f"To play over the internet:\n"
                                            f"- Port forward {PORT} to {local_ip} in your router.\n"
                                            f"- Share the public IP above with friends."
                                        )
                                        ip_input_text = local_ip
                                        state = "create_server"
                                        input_type = "username"
                                        input_active = True
                                        input_text = username_input_text
                                        error_message = ""
                                    except Exception as e:
                                        error_message = f"Failed to start server: {str(e)}"
                            elif i == 1:
                                state = "join_server"
                                input_type = "ip"
                                input_active = True
                                input_text = ip_input_text
                                error_message = ""
                            elif i == 2:
                                running = False
                                return None, None
                elif state == "create_server":
                    if host_rect.collidepoint(mouse_pos):
                        username_input_text = input_text or "Guest"
                        input_active = False
                        try:
                            client = ClientApp(ip_input_text, username_input_text, screen, is_host=True, server_loop=server_loop, server=server)
                            await run_client(client)
                            screen = pygame.display.set_mode((600, 600))
                            pygame.display.set_caption("Game Menu")
                            return server_loop, server
                        except Exception as e:
                            error_message = f"Failed to connect: {str(e)}"
                            state = "main"
                            input_text = ""
                            username_input_text = ""
                            if server_loop and server:
                                server.close()
                                server_loop.close()
                                server_loop = None
                                server = None
                    elif back_rect.collidepoint(mouse_pos):
                        state = "main"
                        input_active = False
                        input_text = ""
                        username_input_text = ""
                        error_message = ""
                        if server_loop and server:
                            server.close()
                            server_loop.close()
                            server_loop = None
                            server = None
                    elif input_rect.collidepoint(mouse_pos):
                        input_active = True
                        input_type = "username"
                        input_text = username_input_text
                elif state == "join_server":
                    if join_rect.collidepoint(mouse_pos):
                        if input_type == "ip":
                            ip_input_text = input_text or "127.0.0.1"
                            input_text = username_input_text
                            input_type = "username"
                            input_active = True
                            error_message = ""
                        elif input_type == "username":
                            username_input_text = input_text or "Guest"
                            input_active = False
                            try:
                                client = ClientApp(ip_input_text, username_input_text, screen, is_host=False)
                                await run_client(client)
                                screen = pygame.display.set_mode((600, 600))
                                pygame.display.set_caption("Game Menu")
                                return None, None
                            except Exception as e:
                                error_message = f"Failed to connect: {str(e)}"
                                state = "main"
                                input_text = ""
                                ip_input_text = ""
                                username_input_text = ""
                        elif ip_input_rect.collidepoint(mouse_pos):
                            input_active = True
                            input_type = "ip"
                            input_text = ip_input_text
                        elif username_input_rect.collidepoint(mouse_pos):
                            input_active = True
                            input_type = "username"
                            input_text = username_input_text
                    elif back_rect.collidepoint(mouse_pos):
                        state = "main"
                        input_active = False
                        input_text = ""
                        input_type = None
                        ip_input_text = ""
                        username_input_text = ""
                        error_message = ""
                    elif ip_input_rect.collidepoint(mouse_pos):
                        input_active = True
                        input_type = "ip"
                        input_text = ip_input_text
                    elif username_input_rect.collidepoint(mouse_pos):
                        input_active = True
                        input_type = "username"
                        input_text = username_input_text
            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    if state == "create_server":
                        username_input_text = input_text or "Guest"
                        input_active = False
                        try:
                            client = ClientApp(ip_input_text, username_input_text, screen, is_host=True, server_loop=server_loop, server=server)
                            await run_client(client)
                            screen = pygame.display.set_mode((600, 600))
                            pygame.display.set_caption("Game Menu")
                            return server_loop, server
                        except Exception as e:
                            error_message = f"Failed to connect: {str(e)}"
                            state = "main"
                            input_text = ""
                            username_input_text = ""
                            if server_loop and server:
                                server.close()
                                server_loop.close()
                                server_loop = None
                                server = None
                    elif state == "join_server" and input_type == "ip":
                        ip_input_text = input_text or "127.0.0.1"
                        input_text = username_input_text
                        input_type = "username"
                        input_active = True
                        error_message = ""
                    elif state == "join_server" and input_type == "username":
                        username_input_text = input_text or "Guest"
                        input_active = False
                        try:
                            client = ClientApp(ip_input_text, username_input_text, screen, is_host=False)
                            await run_client(client)
                            screen = pygame.display.set_mode((600, 600))
                            pygame.display.set_caption("Game Menu")
                            return None, None
                        except Exception as e:
                            error_message = f"Failed to connect: {str(e)}"
                            state = "main"
                            input_text = ""
                            ip_input_text = ""
                            username_input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    if input_type == "ip":
                        ip_input_text = ip_input_text[:-1]
                        input_text = ip_input_text
                    elif input_type == "username":
                        username_input_text = username_input_text[:-1]
                        input_text = username_input_text
                elif event.unicode.isprintable():
                    if input_type == "ip":
                        ip_input_text += event.unicode
                        input_text = ip_input_text
                    elif input_type == "username":
                        username_input_text += event.unicode
                        input_text = username_input_text

        screen.fill((30, 30, 30))
        if state == "main":
            pygame.display.set_caption("Multiplayer Menu")
            for i, option in enumerate(options):
                rect = button_rects[i]
                is_hovered = rect.collidepoint(mouse_pos)
                bg_color = (0, 100, 0) if is_hovered else (50, 50, 50)
                text_color = (255, 255, 255) if is_hovered else (200, 200, 200)
                pygame.draw.rect(screen, bg_color, rect, border_radius=10)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
                surf = button_font.render(option, True, text_color)
                text_rect = surf.get_rect(center=rect.center)
                screen.blit(surf, text_rect)
        elif state == "create_server":
            pygame.display.set_caption("Creating Server")
            title_surf = font.render("Creating Server", True, (255, 255, 255))
            screen.blit(title_surf, (50, 100))
            prompt_surf = font.render("Enter your username:", True, (255, 255, 255))
            screen.blit(prompt_surf, (50, 200))
            username_border_color = (0, 255, 0) if input_type == "username" and input_active else (255, 255, 255)
            pygame.draw.rect(screen, username_border_color, input_rect, 2, border_radius=5)
            input_surf = font.render(input_text, True, (255, 255, 255))
            input_text_rect = input_surf.get_rect(topleft=(60, 260))
            screen.blit(input_surf, input_text_rect)
            is_host_hovered = host_rect.collidepoint(mouse_pos)
            host_bg_color = (0, 100, 0) if is_host_hovered else (50, 50, 50)
            host_text_color = (255, 255, 255) if is_host_hovered else (200, 200, 200)
            pygame.draw.rect(screen, host_bg_color, host_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), host_rect, 2, border_radius=10)
            host_surf = button_font.render("Host", True, host_text_color)
            host_text_rect = host_surf.get_rect(center=host_rect.center)
            screen.blit(host_surf, host_text_rect)
            is_back_hovered = back_rect.collidepoint(mouse_pos)
            back_bg_color = (100, 0, 0) if is_back_hovered else (50, 50, 50)
            back_text_color = (255, 255, 255) if is_back_hovered else (200, 200, 200)
            pygame.draw.rect(screen, back_bg_color, back_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), back_rect, 2, border_radius=10)
            back_surf = button_font.render("Back", True, back_text_color)
            back_text_rect = back_surf.get_rect(center=back_rect.center)
            screen.blit(back_surf, back_text_rect)
        elif state == "join_server":
            pygame.display.set_caption("Joining Server")
            title_surf = font.render("Joining Server", True, (255, 255, 255))
            screen.blit(title_surf, (50, 100))
            ip_prompt_surf = font.render("Server IP:", True, (255, 255, 255))
            screen.blit(ip_prompt_surf, (50, 200))
            ip_border_color = (0, 255, 0) if input_type == "ip" and input_active else (255, 255, 255)
            pygame.draw.rect(screen, ip_border_color, ip_input_rect, 2, border_radius=5)
            ip_surf = font.render(ip_input_text, True, (255, 255, 255))
            ip_text_rect = ip_surf.get_rect(topleft=(60, 260))
            screen.blit(ip_surf, ip_text_rect)
            username_prompt_surf = font.render("Username:", True, (255, 255, 255))
            screen.blit(username_prompt_surf, (50, 300))
            username_border_color = (0, 255, 0) if input_type == "username" and input_active else (255, 255, 255)
            pygame.draw.rect(screen, username_border_color, username_input_rect, 2, border_radius=5)
            username_surf = font.render(username_input_text, True, (255, 255, 255))
            username_text_rect = username_surf.get_rect(topleft=(60, 360))
            screen.blit(username_surf, username_text_rect)
            is_join_hovered = join_rect.collidepoint(mouse_pos)
            join_bg_color = (0, 100, 0) if is_join_hovered else (50, 50, 50)
            join_text_color = (255, 255, 255) if is_join_hovered else (200, 200, 200)
            pygame.draw.rect(screen, join_bg_color, join_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), join_rect, 2, border_radius=10)
            join_surf = button_font.render("Join Server", True, join_text_color)
            join_text_rect = join_surf.get_rect(center=join_rect.center)
            screen.blit(join_surf, join_text_rect)
            is_back_hovered = back_rect.collidepoint(mouse_pos)
            back_bg_color = (100, 0, 0) if is_back_hovered else (50, 50, 50)
            back_text_color = (255, 255, 255) if is_back_hovered else (200, 200, 200)
            pygame.draw.rect(screen, back_bg_color, back_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), back_rect, 2, border_radius=10)
            back_surf = button_font.render("Back", True, back_text_color)
            back_text_rect = back_surf.get_rect(center=back_rect.center)
            screen.blit(back_surf, back_text_rect)

        if error_message:
            error_surf = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surf, (50, 500))

        pygame.display.flip()

    return server_loop, server
