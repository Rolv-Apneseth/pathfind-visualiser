import pygame


class Dropdown():
    def __init__(self, menu_colour1, menu_colour2, option_colour1, option_colour2, x, y, width, height):

        self.menu_colour1 = menu_colour1
        self.menu_colour2 = menu_colour2
        # Two colous since the colours alternate depending on whether the mouse
        # is hovering over the option or not
        self.option_colour1 = option_colour1
        self.option_colour2 = option_colour2

        self.options = []

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def add_options(self, *options):

        # Options given should be in format ("Display name", function)
        for option in options:
            self.options.append(option)
        self.selected_option = options[0][0]

    # Display dropdown menu button
    def draw_main(self, window, font, xpos, ypos):
        if not self.is_selected_main(xpos, ypos):
            # Text
            name_label = font.render(self.selected_option,
                                     1, self.menu_colour1)
            window.blit(name_label, (self.x + (self.width // 2 - name_label.get_width() // 2),
                                     self.y + (self.height // 2 - name_label.get_height() // 2)))

        else:

            # Box
            pygame.draw.rect(window, self.menu_colour1,
                             (self.x, self.y, self.width, self.height), 0)
            # Text
            name_label = font.render(self.selected_option,
                                     1, self.menu_colour2)
            window.blit(name_label, (self.x + (self.width // 2 - name_label.get_width() // 2),
                                     self.y + (self.height // 2 - name_label.get_height() // 2)))

    # Display actual dropdown menu with options
    def draw_options(self, window, font, xpos, ypos):

        for i, option in enumerate(self.options):
            if not self.is_selected_option(xpos, ypos, i):
                option_label = font.render(option[0], 1, self.option_colour1)
                window.blit(option_label, (self.x + (self.width // 2 - option_label.get_width() // 2),
                                           self.y + (self.height // 2 - option_label.get_height() // 2) + self.height * i + self.height))

            else:
                pygame.draw.rect(window, self.option_colour1,
                                 (self.x, self.y + self.height + i * self.height, self.width, self.height), 0)

                option_label = font.render(option[0], 1, self.option_colour2)
                window.blit(option_label, (self.x + (self.width // 2 - option_label.get_width() // 2),
                                           self.y + (self.height // 2 - option_label.get_height() // 2) + self.height * i + self.height))

    # Detect when the mouse is within the 'select mode' box

    def is_selected_main(self, xpos, ypos):
        if self.x < xpos < self.x + self.width and self.y < ypos < self.y + self.height:
            return True
        else:
            return False
    # Detect when the mouse is within the option list

    def is_selected_option(self, xpos, ypos, i):
        if self.x < xpos < self.x + self.width and self.y + self.height * (i + 1) < ypos < self.y + self.height + (i + 1) * self.height:
            return True
        else:
            return False
