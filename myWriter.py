import pygame.font
pygame.font.init()
class writerMine:
    def __init__(self, fonter = 't'):
        self.fonts = []
        for i in range(0, 100):
            self.fonts.append(i)
            #print(i)
        self.fontuse = fonter

    def addFont(self, size):
        self.fonts[size - 1] = pygame.font.SysFont(self.fontuse, size)

    def write(self, size, text):
        #print(str(size) + ', ' + text)
        if self.fonts[size - 1] == size - 1: self.addFont(size)
        disper = self.fonts[size - 1].render(text, True, (255, 255 , 255))
        return disper