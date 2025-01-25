a = int(input("ВВедіть число"))
if a > 0:
    print("Число додатнє")
if a < 0:
    print("Число видемне")

def show_start_screen():
    start = True
    font = pygame.font.SysFont('comic sans', 24)
    small_font = pygame.font.SysFont('comic sans', 24)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_x, mouse_y):
                    start = False

        window.fill((5, 5, 20))
        text = font.render("У Вас є три життя", True, (255, 255, 255))
        play_text = small_font.render("Грати", True, (255, 255, 255))

        window.blit(text, (250 - text.get_width() // 2, 200))

        play_button = pygame.Rect(200, 300, 100, 50)
        pygame.draw.rect(window, (0, 255, 0), play_button)
        window.blit(play_text, (250 - play_text.get_width() // 2, 325 - play_text.get_height() // 2))

        pygame.display.update()

