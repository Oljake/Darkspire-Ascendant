import pygame


class Player:
    def __init__(self, x, y, width, height, speed, image_path="images/player/Thomas.png"):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

        raw_img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(raw_img, (width, height))

    def move(self, keys, collision):
        dx = dy = 0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed

        if dx and not collision.check(self.rect.x + dx, self.rect.y):
            self.rect.x += dx
        if dy and not collision.check(self.rect.x, self.rect.y + dy):
            self.rect.y += dy

    def get_pos(self):
        return self.rect.x, self.rect.y

    def draw(self, screen, offset):
        screen.blit(self.image, (self.rect.x - offset[0], self.rect.y - offset[1]))
