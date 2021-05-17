import pygame as pg
import pyperclip
import re

pg.init()


class OverFlow:
    def __init__(self, rect, color=None):
        self.color = color
        self.rect = pg.Rect(rect)
        self.dote = []
        self.border = 0
        self.all_width = 0
        self.active = False
        self.old_pos_y = 0

    def update_1(self):
        for child in self.dote:
            self.all_width = max(self.all_width, child.rect.size[1] + child.rect.y)

    def add(self, *children):
        for child in children:
            self.dote.append(child)
        self.update_1()

    def handle_event(self, _event):
        if _event.type == pg.MOUSEBUTTONDOWN and self.all_width > self.rect.y + self.rect.size[1]:
            if _event.button == 4:
                self.border -= 30
            elif _event.button == 5:
                self.border += 30
        rect = pg.Rect(0, 0, 0, 0)
        if self.all_width > self.rect.y + self.rect.size[1]:
            rect = pg.Rect(self.rect.x + self.rect.size[0] - 10,
                           (self.border / self.all_width) * self.rect.size[1],
                           10, self.rect.size[1] ** 2 / self.all_width)
        d = False
        for child in self.dote:
            a = child.handle_event(_event)
            if not a is None:
                d = a
            if self.active and pg.mouse.get_pressed(num_buttons=3)[0] and rect.collidepoint(pg.mouse.get_pos()):
                child.active = False
        if d:
            return d

    def update(self):
        if self.all_width > self.rect.y + self.rect.size[1]:
            rect = pg.Rect(self.rect.x + self.rect.size[0] - 10,
                           (self.border / self.all_width) * self.rect.size[1],
                           10, self.rect.size[1] ** 2 / self.all_width)

            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.active = True
            else:
                self.active = False
                self.old_pos_y = pg.mouse.get_pos()[1] - rect.y

            if self.active and pg.mouse.get_pressed(num_buttons=3)[0] and rect.collidepoint(pg.mouse.get_pos()):
                self.border = (pg.mouse.get_pos()[1] - self.old_pos_y) * (self.all_width / self.rect.size[1])
            else:
                self.old_pos_y = pg.mouse.get_pos()[1] - rect.y
            if self.border < 0:
                self.border = 0
            elif self.border > self.all_width - self.rect.size[1]:
                self.border = self.all_width - self.rect.size[1]

        for child in self.dote:
            child.update()
            if self.all_width > self.rect.y + self.rect.size[1]:
                child.border = -self.border

    def draw(self, _screen):
        surf = pg.Surface((self.rect.size[0], self.rect.size[1]))
        if self.color:
            surf.fill(self.color)
        else:
            surf.set_colorkey((0, 0, 0))

        for child in self.dote:
            surf = child.draw(surf)
        _screen.blit(surf, (self.rect.x, self.rect.y))
        if self.all_width > self.rect.y + self.rect.size[1]:
            pg.draw.rect(_screen, (100, 100, 100),
                         pg.Rect(self.rect.x + self.rect.size[0] - 10,
                                 (self.border / self.all_width) * self.rect.size[1],
                                 10, self.rect.size[1] ** 2 / self.all_width))
        return _screen


class Text:
    def __init__(self, pos, width, text, margin_text=5, replace_on=" ", FONT=pg.font.Font(None, 17),
                 color_text=(255, 255, 255), color_back_grand=None, copy=True):
        self.active = False
        self.border = 0
        self.copy = copy
        self.margin_text = margin_text
        self.replace_on = replace_on
        self.width = width
        self.color_back_grand = color_back_grand
        self.color_text = color_text
        self.FONT = FONT
        self.text = text
        self.good_text = [""]
        self.pos = pos
        self.wights_mark = []
        self.old_click = (False, pg.mouse.get_pos())
        self.outline = {}
        self.draw_blocks = []
        self.rect = pg.Rect(0, 0, 0, 0)
        self.update_1()



    def update_1(self):
        self.good_text = [""]
        self.wights_mark = []
        self.draw_blocks = []
        self.rect = pg.Rect(0, 0, 0, 0)

        if self.replace_on == " ":
            ar = []
            for STR in self.text.split("\n"):
                if STR != "":
                    ar.append([STR])
            for i in range(len(ar)):
                for STR in ar[i][0].split(" "):
                    if STR != "":
                        ar[i].append(STR)
                ar[i].pop(0)
            for i in range(len(ar)):
                if i != 0:
                    self.good_text.append(f"")
                for j in range(len(ar[i])):
                    wood = "".join(ar[i][j])
                    width = self.FONT.render(self.good_text[-1] + " " + wood, True, (0, 0, 0)).get_width()
                    if width >= self.width:
                        self.good_text.append(f"{wood}")
                    else:
                        self.good_text[-1] += " " + wood

        elif self.replace_on == "":
            ar = []
            for STR in self.text.split("\n"):
                if STR != "":
                    ar.append([STR])
            for i in range(len(ar)):
                for j in range(len(ar[i][0])):
                    if ar[i][0][j] != "":
                        ar[i].append(ar[i][0][j])
                ar[i].pop(0)
            for i in range(len(ar)):
                if i != 0:
                    self.good_text.append(f"")
                for j in range(len(ar[i])):
                    mark = "".join(ar[i][j])
                    width = self.FONT.render(self.good_text[-1] + mark, True, (0, 0, 0)).get_width()
                    if width >= self.width:
                        self.good_text.append(f"{mark}")
                    else:
                        self.good_text[-1] += mark

        for i in range(len(self.good_text)):
            self.wights_mark.append([])
            self.wights_mark[i].append(0)
            for j in range(len(self.good_text[i])):
                text = self.good_text[i][:(j + 1)]

                self.wights_mark[i].append(self.FONT.render(text, True, (0, 0, 0)).get_width())

        text = self.FONT.render("12", True, (0, 0, 0))

        if self.color_back_grand:
            x1 = 0
            for x2 in self.wights_mark:
                x1 = max(max(x2), x1)
            surf = pg.Surface((x1 + 4,
                               (len(self.good_text) * (
                                       text.get_height() + self.margin_text) - self.margin_text) + 4))
            surf.fill(self.color_back_grand)
            self.draw_blocks.append((surf, (self.pos[0] - 2, self.pos[1] - 2)))

        for i in range(len(self.good_text)):
            y = self.pos[1] + i * (text.get_height() + self.margin_text)
            self.draw_blocks.append((self.FONT.render(self.good_text[i], True, self.color_text), (self.pos[0], y)))

        text = self.FONT.render("12", True, (0, 0, 0))
        x1 = 0
        for x2 in self.wights_mark:
            x1 = max(max(x2), x1)
        self.rect = pg.Rect(self.pos[0] - 2, self.pos[1] - 2, x1 + 4 - self.pos[0] - 2,
                            (len(self.good_text) * (
                                    text.get_height() + self.margin_text) - self.margin_text) + 4)

    def handle_event(self, _event):
        self.active = True
        if _event.type == pg.MOUSEBUTTONDOWN:
            self.outline = {}
        elif _event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if (keys[pg.K_RCTRL] or keys[pg.K_LCTRL]) and keys[pg.K_c] and self.copy:
                text = ""
                start_or_not_end = False
                last_i = 0
                for i in range(len(self.good_text)):
                    for j in range(len(self.good_text[i])):
                        if (j, i) == list(self.outline.keys())[0] and not start_or_not_end:
                            start_or_not_end = True
                            last_i = i
                        if (j, i) == list(self.outline.keys())[-1] and start_or_not_end:
                            start_or_not_end = False
                        if start_or_not_end:
                            if last_i != i:
                                last_i = i
                                text += "\n"
                            text += self.good_text[i][j]
                if not text == "":
                    pyperclip.copy(text)

    def update(self):
        if pg.mouse.get_pressed(num_buttons=3)[0] and self.copy:
            if self.old_click[0]:
                text = self.FONT.render("12", True, (0, 0, 0))
                self.outline = {}
                pos_cursor = pg.mouse.get_pos()
                stop = False
                for i in range(len(self.wights_mark)):
                    for j in range(len(self.wights_mark[i])):
                        x = self.pos[0] + self.wights_mark[i][j]
                        y = self.pos[1] + i * (text.get_height() + self.margin_text) + self.border
                        try:
                            x_1 = self.pos[0] + self.wights_mark[i][j + 1]
                            mean_x = (x_1 - x) / 2
                        except:
                            x_1 = self.pos[0] + self.wights_mark[i][j - 1]
                            mean_x = (x - x_1) / 2

                        first_rect = pg.Rect(
                            (x - mean_x + 1, y, mean_x * 2 + 2, text.get_height() + self.margin_text))
                        if first_rect.collidepoint(*pos_cursor):
                            self.outline[(j, i)] = True
                            stop = True
                            break
                        if j == 0 and pos_cursor[0] < x - mean_x + 1 and y <= pos_cursor[1] \
                                <= text.get_height() + self.margin_text + y:
                            self.outline[(j, i)] = True
                            stop = True
                            break
                        if j == len(self.wights_mark[i]) - 1 and pos_cursor[0] > x - mean_x + 1 and y <= pos_cursor[1] \
                                <= text.get_height() + self.margin_text + y:
                            self.outline[(j, i)] = True
                            stop = True
                            break

                    if stop:
                        break

                if not self.outline and pos_cursor[1] <= self.pos[1] + self.border:
                    self.outline = {(0, 0): True}
                if not self.outline and pos_cursor[1] >= self.pos[1] + (len(self.wights_mark) - 1) * \
                        (text.get_height() + self.margin_text) + text.get_height() + self.border:
                    self.outline = {(len(self.wights_mark[-1]) - 1, len(self.wights_mark) - 1): True}

                self.wights_mark.reverse()
                reverse = self.wights_mark
                self.wights_mark.reverse()

                old_pos_cursor = self.old_click[1]
                stop = False
                for i in range(len(reverse)):
                    i = len(self.wights_mark) - 1 - i
                    for j in range(len(self.wights_mark[i])):
                        j = len(self.wights_mark[i]) - 1 - j
                        x = self.pos[0] + self.wights_mark[i][j]
                        y = self.pos[1] + i * (text.get_height() + self.margin_text) + self.border
                        try:
                            x_1 = self.pos[0] + self.wights_mark[i][j + 1]
                            mean_x = (x_1 - x) / 2
                        except:
                            x_1 = self.pos[0] + self.wights_mark[i][j - 1]
                            mean_x = (x - x_1) / 2

                        first_rect = pg.Rect(
                            (x - mean_x, y, mean_x * 2, text.get_height() + self.margin_text))
                        if first_rect.collidepoint(*old_pos_cursor):
                            self.outline[(j, i)] = True
                            stop = True
                            break
                        if j == 0 and old_pos_cursor[0] < x - mean_x + 1 and y <= old_pos_cursor[1] \
                                <= text.get_height() + self.margin_text + y:
                            self.outline[(j, i)] = True
                            stop = True
                            break
                        if j == len(self.wights_mark[i]) - 1 and old_pos_cursor[0] > x - mean_x + 1 and y <= \
                                old_pos_cursor[1] <= text.get_height() + self.margin_text + y:
                            self.outline[(j, i)] = True
                            stop = True
                            break
                    if stop:
                        break
                if self.outline and old_pos_cursor[1] <= self.pos[1] + self.border:
                    self.outline = {list(self.outline.keys())[0]: True, (0, 0): True}
                if self.outline and old_pos_cursor[1] >= self.pos[1] + (len(self.wights_mark) - 1) * (
                        text.get_height() + self.margin_text) + text.get_height() + self.border:
                    self.outline = {list(self.outline.keys())[0]: True,
                                    (len(self.wights_mark[-1]) - 1, len(self.wights_mark) - 1): True}

                if len(list(self.outline.keys())) >= 2:
                    if list(self.outline.keys())[0][1] > list(self.outline.keys())[-1][1]:
                        self.outline = {list(self.outline.keys())[-1]: True, list(self.outline.keys())[0]: True}
                    elif list(self.outline.keys())[0][0] > list(self.outline.keys())[-1][0] and \
                            list(self.outline.keys())[0][1] == list(self.outline.keys())[-1][1]:
                        self.outline = {list(self.outline.keys())[-1]: True, list(self.outline.keys())[0]: True}

            self.old_click = (True, self.old_click[1])
        else:
            self.old_click = (False, pg.mouse.get_pos())
        if not self.active:
            self.outline = {}

    def draw(self, _screen):
        text = self.FONT.render("12", True, (0, 0, 0))
        x = [(0, 0), (0, 0)]
        if list(self.outline.keys()):
            x = [list(self.outline.keys())[0], list(self.outline.keys())[-1]]
        for block in self.draw_blocks:
            _screen.blit(block[0], (block[1][0], block[1][1] + self.border))

        if x[1] != (0, 0) and self.copy:
            if x[0][1] == x[1][1]:
                blue_surf = pg.Surface(
                    (self.wights_mark[x[1][1]][x[1][0]] - self.wights_mark[x[0][1]][x[0][0]], text.get_height()))
                blue_surf.set_colorkey((0, 0, 0))
                blue_surf.fill((0, 0, 255))
                blue_surf.set_alpha(100)
                _screen.blit(blue_surf,
                             (self.pos[0] + self.wights_mark[x[0][1]][x[0][0]],
                              self.pos[1] + x[0][1] * (text.get_height() + self.margin_text) + self.border))
            else:
                blue_surf = pg.Surface(
                    (self.wights_mark[x[0][1]][-1] - self.wights_mark[x[0][1]][x[0][0]], text.get_height()))
                blue_surf.set_colorkey((0, 0, 0))
                blue_surf.fill((0, 0, 255))
                blue_surf.set_alpha(100)
                _screen.blit(blue_surf,
                             (self.pos[0] + self.wights_mark[x[0][1]][x[0][0]],
                              self.pos[1] + x[0][1] * (text.get_height() + self.margin_text) + self.border))
                i = x[0][1] + 1
                while i < x[1][1]:
                    blue_rect = pg.Surface((self.wights_mark[i][-1], text.get_height()))
                    blue_rect.set_colorkey((0, 0, 0))
                    blue_rect.fill((0, 0, 255))
                    blue_rect.set_alpha(100)
                    _screen.blit(blue_rect, (
                        self.pos[0], self.pos[1] + i * (text.get_height() + self.margin_text) + self.border))
                    i += 1
                blue_rect = pg.Surface((self.wights_mark[x[1][1]][x[1][0]], text.get_height()))
                blue_rect.set_colorkey((0, 0, 0))
                blue_rect.fill((0, 0, 255))
                blue_rect.set_alpha(100)
                _screen.blit(blue_rect,
                             (self.pos[0],
                              self.pos[1] + x[1][1] * (text.get_height() + self.margin_text) + self.border))

        return _screen


class Button:
    def __init__(self, pos, text, _type, FONT=pg.font.Font(None, 32),
                 COLOR_INACTIVE=(141, 182, 205, 255),
                 COLOR_ACTIVE=(28, 134, 238, 255)):
        self.type = _type
        self.active = False
        self.rect = pg.Rect(pos)
        self.color = COLOR_INACTIVE
        self.txt_surface = FONT.render(text, True, self.color)
        self.colors = [COLOR_INACTIVE, COLOR_ACTIVE]
        self.border = 0

    def handle_event(self, _event):
        rect = self.rect.copy()
        rect.y += self.border
        if rect.collidepoint(pg.mouse.get_pos()):
            if _event.type == pg.MOUSEBUTTONDOWN:
                if _event.button == 1 or _event.button == 2 or _event.button == 3:
                    return self
            self.color = self.colors[1]
        else:
            self.color = self.colors[0]

    def update(self):
        pass

    def draw(self, _screen):

        _screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5 + self.border))
        pg.draw.rect(_screen, self.color,
                     pg.Rect(self.rect.x, self.rect.y + self.border, self.rect.size[0], self.rect.size[1]), 2)
        return _screen


class InputBox:

    def __init__(self, pos, text='', special_symbol=True, copy=True, hidden_text="", FONT=pg.font.Font(None, 32),
                 hidden_color_text=(141, 182, 205, 255),
                 COLOR_INACTIVE=(141, 182, 205, 255),
                 COLOR_ACTIVE=(28, 134, 238, 255), max_length=None):
        self.special_symbol = special_symbol
        self.border = 0
        self.copy = copy
        self.max_length = max_length
        self.rect = pg.Rect(pos)
        self.colors = [COLOR_INACTIVE, COLOR_ACTIVE, hidden_color_text]
        self.color = COLOR_INACTIVE
        self.text = text
        self.FONT = FONT
        self.txt_surface = FONT.render(text, True, self.color)
        self.hidden_surface = FONT.render(hidden_text, True, self.colors[2])
        self.active = False
        self.cursor = 0
        self.wights = [0]
        self.outline = {}
        self.old_click = (False, ())

    def handle_event(self, _event):

        if _event.type == pg.MOUSEBUTTONDOWN:
            if _event.button == 1 or _event.button == 2 or _event.button == 3:
                self.outline = {}
                rect = self.rect.copy()
                rect.y += self.border
                if rect.collidepoint(_event.pos):
                    if len(self.wights) >= 2 and self.active:
                        for i in range(len(self.text)):
                            mean = (self.wights[i + 1] - self.wights[i]) / 2
                            if (self.wights[i] <= pg.mouse.get_pos()[0] - 5 - self.rect.x < self.wights[
                                i + 1] - mean and
                                    0 <= pg.mouse.get_pos()[1] - 5 - rect.y <= self.txt_surface.get_height()):
                                self.cursor = i
                                return
                            elif (self.wights[i] + mean <= pg.mouse.get_pos()[0] - 5 - self.rect.x < self.wights[
                                i + 1] and
                                  0 <= pg.mouse.get_pos()[1] - 5 - rect.y <= self.txt_surface.get_height()):
                                self.cursor = (i + 1)
                                return

                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = self.colors[1] if self.active else self.colors[0]
        if _event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if (keys[pg.K_RCTRL] or keys[pg.K_LCTRL]) and keys[pg.K_c] and self.copy:
                if len(list(self.outline.keys())) >= 1:
                    text = self.text[list(self.outline.keys())[0]:list(self.outline.keys())[-1]]
                    pyperclip.copy(text)
            elif self.active:
                if (keys[pg.K_RCTRL] or keys[pg.K_LCTRL]) and keys[pg.K_v] and self.copy:
                    if len(list(self.outline.keys())) >= 1:
                        text_1 = self.text[:list(self.outline.keys())[0]]
                        text_2 = self.text[list(self.outline.keys())[-1]:]
                        if self.special_symbol:
                            self.text = text_1 + pyperclip.paste() + text_2
                        else:
                            self.text = re.sub(r'[^a-zA-Z0-9А-Яа-я]', r"", f"{text_1 + pyperclip.paste() + text_2}")
                    else:
                        text_1 = self.text[:self.cursor]  # += event.unicode
                        text_2 = self.text[self.cursor:]
                        if self.special_symbol:
                            self.text = text_1 + pyperclip.paste() + text_2
                        else:
                            self.text = re.sub(r'[^a-zA-Z0-9А-Яа-я ]', r"", f"{text_1 + pyperclip.paste() + text_2}")
                        self.cursor += len(pyperclip.paste())
                    self.outline = {}

                elif (keys[pg.K_RCTRL] or keys[pg.K_LCTRL]) and keys[pg.K_x] and self.copy:
                    if len(list(self.outline.keys())) >= 1:
                        text = self.text[list(self.outline.keys())[0]:list(self.outline.keys())[-1]]
                        pyperclip.copy(text)

                        text_1 = self.text[:list(self.outline.keys())[0]]
                        text_2 = self.text[list(self.outline.keys())[-1]:]
                        self.text = text_1 + text_2
                        self.outline = {}

                elif _event.key == pg.K_LEFT:
                    self.cursor -= 1
                    self.outline = {}
                elif _event.key == pg.K_RIGHT:
                    self.cursor += 1
                    self.outline = {}
                elif _event.key == pg.K_BACKSPACE:
                    if self.cursor - 1 >= 0:
                        text_1 = self.text[:self.cursor - 1]
                        text_2 = self.text[self.cursor:]
                        self.text = (text_1 + text_2)
                        self.cursor -= 1
                elif _event.key == pg.K_DELETE:
                    text_1 = self.text[:self.cursor]
                    text_2 = self.text[self.cursor + 1:]
                    self.text = (text_1 + text_2)
                elif _event.unicode != "":
                    if self.max_length is None or self.max_length > len(self.text):
                        text_1 = self.text[:self.cursor]  # += event.unicode
                        text_2 = self.text[self.cursor:]
                        if self.special_symbol:
                            self.text = text_1 + _event.unicode + text_2
                        else:
                            self.text = re.sub(r'[^a-zA-Z0-9А-Яа-я]', r"", f"{text_1 + _event.unicode + text_2}")
                        if not (_event.key == pg.K_RCTRL or _event.key == pg.K_LCTRL):
                            self.cursor += 1

                # Re-render the text.

        if self.cursor > len(self.text):
            self.cursor = len(self.text)

        if self.cursor < 0:
            self.cursor = 0

    def update(self):
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        # Resize the box if the text is too long.
        width = max(300, self.txt_surface.get_width() + 10)
        self.rect.w = width
        self.wights = [0]
        for i in range(len(self.text)):
            text = self.text[:(i + 1)]
            self.wights.append(self.FONT.render(text, True, (0, 0, 0)).get_width())

        if pg.mouse.get_pressed(num_buttons=3)[0] and self.copy:
            if self.old_click[0]:
                if len(self.wights) >= 2:
                    self.outline = {}
                    for i in range(len(self.text)):
                        first_rect = pg.Rect((0, 0,
                                              pg.mouse.get_pos()[0] - self.old_click[1][0],
                                              pg.mouse.get_pos()[1] - self.old_click[1][1]))
                        second_rect = pg.Rect((self.wights[i] + 5 + self.rect.x - self.old_click[1][0],
                                               5 + self.rect.y - self.old_click[1][1] + self.border,
                                               self.wights[i] + 5 + self.rect.x - self.old_click[1][0] +
                                               self.wights[i + 1] - self.wights[i],
                                               self.txt_surface.get_height() + 5 + self.rect.y - self.old_click[1][
                                                   1] + self.border))
                        if first_rect.colliderect(second_rect):
                            self.outline[i] = True
                            self.outline[i + 1] = True

            self.old_click = (True, self.old_click[1])
        else:
            self.old_click = (False, pg.mouse.get_pos())

    def draw(self, _screen):
        if self.text == "":
            _screen.blit(self.hidden_surface, (self.rect.x + 5, self.rect.y + 5 + self.border))
        else:
            _screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5 + self.border))
        if self.active:
            cursor = pg.Surface((1, self.txt_surface.get_height()))
            cursor.fill((255, 255, 255))

            x = self.wights[self.cursor]
            _screen.blit(cursor, (self.rect.x + 5 + x, self.rect.y + 5 + self.border))
        if len(list(self.outline.keys())) > 1 and self.copy:
            outline = list(self.outline.keys())
            outline.sort()
            extreme_points = (self.wights[outline[0]], self.wights[outline[-1]])
            blue_surf = pg.Surface((extreme_points[1] - extreme_points[0], self.txt_surface.get_height()))
            blue_surf.set_colorkey((0, 0, 0))
            blue_surf.fill((0, 0, 255))
            blue_surf.set_alpha(100)
            _screen.blit(blue_surf, (self.rect.x + 5 + extreme_points[0], self.rect.y + 5 + self.border))
        pg.draw.rect(_screen, self.color,
                     pg.Rect(self.rect.x, self.rect.y + self.border, self.rect.size[0], self.rect.size[1]), 2)

        return _screen


class TextAria:
    def __init__(self, pos, width, FONT=pg.font.Font(None, 34), margin_text=5, color_text=(255, 255, 255)):
        self.color_text = color_text
        self.margin_text = margin_text
        self.FONT = FONT
        self.pos = pos
        self.width = width
        self.text = ""
        self.draw_blocks = []
        self.good_text = [""]
        self.wights_mark = []
        self.wights_mark_2 = []
        self.cursor = [0, 0]
        self.old_click = [False, pg.mouse.get_pos()]
        self.outline = {}
        self.update()

    def handle_event(self, _event):
        if _event.type == pg.KEYDOWN:
            keys_1 = list(self.outline.keys())
            keys = pg.key.get_pressed()
            stop = False
            if len(keys_1) >= 2 and _event.unicode != "" and not (_event.key == pg.K_c and keys[pg.K_LCTRL]):
                arr_text_1 = self.text.split("\n")
                if keys_1[0][1] == keys_1[1][1]:
                    text_1_1 = arr_text_1[keys_1[0][1]][:keys_1[0][0]]
                    text_2_1 = arr_text_1[keys_1[0][1]][keys_1[1][0]:]
                    arr_text_1[keys_1[0][1]] = text_1_1 + text_2_1
                    self.text = "\n".join(arr_text_1)
                    self.cursor = [keys_1[0][0], keys_1[0][1]]
                else:
                    text_1_1 = arr_text_1[keys_1[0][1]][:keys_1[0][0]]
                    text_2_1 = arr_text_1[keys_1[1][1]:]
                    text_2_1[0] = text_2_1[0][keys_1[1][0]:]
                    text_2_1 = "\n".join(text_2_1)
                    arr_text_1[keys_1[0][1]] = text_1_1 + text_2_1
                    arr_text_1 = arr_text_1[:keys_1[0][1] + 1]
                    self.text = "\n".join(arr_text_1)
                    self.cursor = [keys_1[0][0], keys_1[0][1]]
                stop = True

            if (_event.unicode == "\r" or _event.unicode == "\n") and (keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]):
                arr_text = self.text.split("\n")
                text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                arr_text[self.cursor[1]] = text_1 + "\n" + text_2
                self.text = "\n".join(arr_text)
                self.cursor[1] += 1
                self.cursor[0] = 0
                self.outline = {}
            elif (_event.unicode == "\r" or _event.unicode == "\n") and not (keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]):
                return self.text
            elif _event.unicode == "\t":
                arr_text = self.text.split("\n")
                text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                arr_text[self.cursor[1]] = text_1 + "    " + text_2
                self.text = "\n".join(arr_text)
                self.cursor[0] += 4
                self.outline = {}
            elif _event.key == pg.K_c and keys[pg.K_LCTRL]:
                arr_text = self.text.split("\n")
                if keys_1[0][1] == keys_1[1][1]:
                    text_1 = arr_text[keys_1[0][1]][keys_1[0][0]:keys_1[1][0]]
                    pyperclip.copy(text_1)
                else:
                    text_1 = arr_text[keys_1[0][1]][keys_1[0][0]:]
                    text_2 = arr_text[keys_1[0][1] + 1:keys_1[1][1] + 1]
                    if text_2:
                        text_2[-1] = text_2[-1][:keys_1[1][0]]
                    pyperclip.copy("\n".join([text_1] + text_2).replace("\n", "\r\n"))
            elif _event.key == pg.K_v and keys[pg.K_LCTRL]:
                paste = pyperclip.paste().replace("\r\n", "\n")
                paste = paste.replace("\r", "\n")
                arr_text = self.text.split("\n")
                text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                arr_text[self.cursor[1]] = text_1 + paste + text_2
                self.text = "\n".join(arr_text)
                self.cursor[1] += len(paste.split("\n")) - 1
                self.cursor[0] += len(paste.split("\n")[-1])
                self.outline = {}
            elif _event.key == pg.K_BACKSPACE:
                if not stop:
                    arr_text = self.text.split("\n")
                    text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                    text_2 = arr_text[self.cursor[1]][self.cursor[0]:]

                    if text_1 == "" and self.cursor[1] != 0:
                        arr_text_1 = arr_text[:self.cursor[1] - 1]
                        arr_text_1.append(arr_text[self.cursor[1] - 1] + arr_text[self.cursor[1]])
                        arr_text_1 += arr_text[self.cursor[1] + 1:]
                        arr_text = arr_text_1

                        self.cursor[1] -= 1
                        self.cursor[0] = len(arr_text[self.cursor[1]])
                    else:
                        arr_text[self.cursor[1]] = text_1[:-1] + text_2
                        self.cursor[0] -= 1

                    self.text = "\n".join(arr_text)
                self.outline = {}
            elif _event.key == pg.K_DELETE:
                if not stop:
                    arr_text = self.text.split("\n")
                    text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                    text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                    if text_2 == "" and self.cursor[1] + 1 < len(arr_text):
                        arr_text_1 = arr_text[:self.cursor[1]]
                        arr_text_1.append(arr_text[self.cursor[1]] + arr_text[self.cursor[1] + 1])
                        arr_text_1 += arr_text[self.cursor[1] + 2:]
                        arr_text = arr_text_1
                    else:
                        arr_text[self.cursor[1]] = text_1 + text_2[1:]

                    self.text = "\n".join(arr_text)
                self.outline = {}
            elif _event.key == pg.K_LEFT:
                self.cursor[0] -= 1
                if self.cursor[0] < 0 <= self.cursor[1] - 1:
                    self.cursor[1] -= 1
                    self.cursor[0] = len(self.text.split("\n")[self.cursor[1]])
                self.outline = {}
            elif _event.key == pg.K_RIGHT:
                self.cursor[0] += 1
                if self.cursor[0] > len(self.text.split("\n")[self.cursor[1]]) and \
                        self.cursor[1] + 1 < len(self.text.split("\n")):
                    self.cursor[1] += 1
                    self.cursor[0] = 0
                self.outline = {}
            elif _event.unicode != "":
                arr_text = self.text.split("\n")
                text_1 = arr_text[self.cursor[1]][:self.cursor[0]]
                text_2 = arr_text[self.cursor[1]][self.cursor[0]:]
                arr_text[self.cursor[1]] = text_1 + _event.unicode + text_2
                self.text = "\n".join(arr_text)
                self.cursor[0] += 1
                self.outline = {}

            if self.cursor[0] < 0:
                self.cursor[0] = 0
            if self.cursor[1] < 0:
                self.cursor[1] = 0
            if self.cursor[0] > len(self.text.split("\n")[self.cursor[1]]):
                self.cursor[0] = len(self.text.split("\n")[self.cursor[1]])
            if self.cursor[1] > len(self.text.split("\n")):
                self.cursor[1] = len(self.text.split("\n"))
        elif _event.type == pg.MOUSEBUTTONDOWN:
            self.outline = {}
            if _event.button == 1:
                height = self.FONT.render("12", True, (0, 0, 0)).get_height() + self.margin_text
                mouse_pos = pg.mouse.get_pos()
                for i in range(len(self.wights_mark_2)):
                    for j in range(len(self.wights_mark_2[i])):
                        margin_1 = 0
                        margin_2 = 0
                        if j != 0:
                            margin_1 = max((self.wights_mark_2[i][j][0] - self.wights_mark_2[i][j - 1][0]) / 2, 0)
                        if j != len(self.wights_mark_2[i]) - 1:
                            margin_2 = max((self.wights_mark_2[i][j + 1][0] - self.wights_mark_2[i][j][0]) / 2, 0)

                        rect = pg.Rect(self.wights_mark_2[i][j][0] - margin_1,
                                       self.wights_mark_2[i][j][1],
                                       margin_1 + margin_2 + 1,
                                       height)

                        if rect.collidepoint(*mouse_pos):
                            self.cursor = [j, i]

                        if j != 0 and j != len(self.wights_mark_2[i]) - 1 and \
                                self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j - 1][1]:
                            y = self.wights_mark_2[i][j][1]
                            x = self.pos[0]
                            margin = (self.wights_mark_2[i][j][0] - x) / 2
                            rect_1 = pg.Rect(x, y, margin + 1, height)
                            rect_2 = pg.Rect(self.wights_mark_2[i][j][0] - margin,
                                             self.wights_mark_2[i][j + 1][1],
                                             margin + 1, height)
                            if rect_1.collidepoint(*mouse_pos):
                                self.cursor = [j - 1, i]

                            if rect_2.collidepoint(*mouse_pos):
                                self.cursor = [j, i]

                        if j == len(self.wights_mark_2[i]) - 1 or \
                                self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j + 1][1]:
                            if self.wights_mark_2[i][j][1] <= mouse_pos[1] <= self.wights_mark_2[i][j][1] + \
                                    height and self.wights_mark_2[i][j][0] <= mouse_pos[0]:
                                self.cursor = [j, i]

    def update(self):
        self.good_text = [""]
        self.wights_mark = []
        self.wights_mark_2 = []
        self.draw_blocks = []

        ar = []
        for STR in self.text.split("\n"):
            ar.append([STR])

        for i in range(len(ar)):
            for j in range(len(ar[i][0])):
                if ar[i][0][j] != "":
                    ar[i].append(ar[i][0][j])
            ar[i].pop(0)
        for i in range(len(ar)):
            if i != 0:
                self.good_text.append(f"")
            for j in range(len(ar[i])):
                mark = "".join(ar[i][j])
                width = self.FONT.render(self.good_text[-1] + mark, True, (0, 0, 0)).get_width()
                if width >= self.width:
                    self.good_text.append(f"{mark}")
                else:
                    self.good_text[-1] += mark

        text = self.FONT.render("12", True, (0, 0, 0))

        for i in range(len(self.good_text)):
            y = self.pos[1] - (len(self.good_text) - 1 - i) * (text.get_height() + self.margin_text)
            self.wights_mark.append([(0, y)])
            for j in range(len(self.good_text[i])):
                text_1 = self.good_text[i][:(j + 1)]

                self.wights_mark[i].append((self.FONT.render(text_1, True, (0, 0, 0)).get_width(), y))
        col_mark = 0

        for i in range(len(self.text.split("\n"))):
            y = self.pos[1] - (len(self.good_text) - 1 - col_mark) * (text.get_height() + self.margin_text)

            self.wights_mark_2.append([(self.pos[0], y)])

            ar = [""]

            for j in range(len(self.text.split("\n")[i])):
                mark = "".join(self.text.split("\n")[i][j])
                width = self.FONT.render(ar[-1] + mark, True, (0, 0, 0)).get_width()
                if width >= self.width:
                    ar.append(f"{mark}")
                    col_mark += 1
                else:
                    ar[-1] += mark
                x = self.FONT.render(ar[-1], True, (0, 0, 0)).get_width() + self.pos[0]
                y = self.pos[1] - (len(self.good_text) - 1 - col_mark) * (text.get_height() + self.margin_text)

                self.wights_mark_2[i].append((x, y))

            col_mark += 1

        if self.cursor[1] + 1 > len(self.text.split("\n")):
            self.cursor[1] = len(self.text.split("\n")) - 1
        if self.cursor[0] - 1 >= len(self.text.split("\n")[self.cursor[1]]) and self.text.split("\n")[
            self.cursor[1]]:
            self.cursor[0] = len(self.text.split("\n")) - 1

        for i in range(len(self.good_text)):
            y = self.pos[1] - (len(self.good_text) - 1 - i) * (text.get_height() + self.margin_text)
            self.draw_blocks.append((self.FONT.render(self.good_text[i], True, self.color_text), (self.pos[0], y)))

        if pg.mouse.get_pressed(num_buttons=3)[0] and pg.mouse.get_focused():
            if self.old_click[0]:
                self.outline = {}
                height = self.FONT.render("12", True, (0, 0, 0)).get_height() + self.margin_text
                for n in [1, 2]:
                    pos = ()
                    if n == 1:
                        pos = pg.mouse.get_pos()
                    if n == 2:
                        pos = self.old_click[1]

                    stop = False
                    if pos[1] < self.wights_mark_2[0][0][1]:
                        self.outline[(0, 0)] = True
                        continue
                    max_i = len(self.wights_mark_2) - 1
                    max_j = len(self.wights_mark_2[max_i]) - 1
                    if pos[1] > self.wights_mark_2[max_i][max_j][1] + height:
                        self.outline[(max_j, max_i)] = True
                        continue
                    for i in range(len(self.wights_mark_2)):
                        if stop:
                            break
                        for j in range(len(self.wights_mark_2[i])):
                            margin_1 = 0
                            margin_2 = 0
                            if j != 0:
                                margin_1 = max((self.wights_mark_2[i][j][0] - self.wights_mark_2[i][j - 1][0]) / 2,
                                               0)
                            if j != len(self.wights_mark_2[i]) - 1:
                                margin_2 = max((self.wights_mark_2[i][j + 1][0] - self.wights_mark_2[i][j][0]) / 2,
                                               0)

                            rect = pg.Rect(self.wights_mark_2[i][j][0] - margin_1,
                                           self.wights_mark_2[i][j][1],
                                           margin_1 + margin_2 + 1,
                                           height)

                            if rect.collidepoint(*pos):
                                self.outline[(j, i)] = True
                                stop = True
                                break

                            if j != 0 and j != len(self.wights_mark_2[i]) - 1 and \
                                    self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j - 1][1]:
                                y = self.wights_mark_2[i][j][1]
                                x = self.pos[0]
                                margin = (self.wights_mark_2[i][j][0] - x) / 2
                                rect_1 = pg.Rect(x, y, margin + 1, height)
                                rect_2 = pg.Rect(self.wights_mark_2[i][j][0] - margin,
                                                 self.wights_mark_2[i][j + 1][1],
                                                 margin + 1, height)
                                if rect_1.collidepoint(*pos):
                                    self.outline[(j - 1, i)] = True
                                    stop = True
                                    break

                                if rect_2.collidepoint(*pos):
                                    self.outline[(j, i)] = True
                                    stop = True
                                    break

                            if j == len(self.wights_mark_2[i]) - 1 or \
                                    self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j + 1][1]:
                                if self.wights_mark_2[i][j][1] <= pos[1] <= self.wights_mark_2[i][j][1] + \
                                        height and self.wights_mark_2[i][j][0] <= pos[0]:
                                    self.outline[(j, i)] = True
                                    stop = True
                                    break

                            if j == 0 or self.wights_mark_2[i][j][1] != self.wights_mark_2[i][j - 1][1]:
                                if self.wights_mark_2[i][j][1] <= pos[1] <= self.wights_mark_2[i][j][1] + \
                                        height and self.wights_mark_2[i][j][0] >= pos[0]:
                                    self.outline[(max(j - 1, 0), i)] = True
                                    stop = True
                                    break
                keys = list(self.outline.keys())
                if len(keys) > 1 and (
                        keys[0][1] > keys[1][1] or (keys[0][0] > keys[1][0] and keys[0][1] >= keys[1][1])):
                    self.outline = {keys[1]: True, keys[0]: True}
            self.old_click[0] = True
        else:
            self.old_click = [False, pg.mouse.get_pos()]

    def draw(self, _screen):
        text = self.FONT.render("12", True, (0, 0, 0))

        for block in self.draw_blocks:
            _screen.blit(block[0], (block[1][0], block[1][1]))
        surf = pg.Surface((1, text.get_height()))
        surf.fill(self.color_text)
        _screen.blit(surf, self.wights_mark_2[self.cursor[1]][self.cursor[0]])

        keys = list(self.outline.keys())
        if len(keys) > 1:
            extreme_angles = [self.wights_mark_2[keys[0][1]][keys[0][0]],
                              self.wights_mark_2[keys[1][1]][keys[1][0]]]
            if extreme_angles[0][1] == extreme_angles[1][1]:
                blue_surf = pg.Surface((extreme_angles[1][0] - extreme_angles[0][0], text.get_height()))
                blue_surf.set_colorkey((0, 0, 0))
                blue_surf.fill((0, 0, 255))
                blue_surf.set_alpha(100)
                _screen.blit(blue_surf, extreme_angles[0])
            else:
                start_pos = ()
                draw = False
                for i in range(len(self.wights_mark_2)):
                    for j in range(len(self.wights_mark_2[i])):
                        if (j, i) == keys[0]:
                            draw = True
                            start_pos = (j, i)
                        if (j, i) == keys[1]:
                            draw = False
                            blue_surf = pg.Surface(
                                (extreme_angles[1][0] - self.pos[0], text.get_height()))
                            blue_surf.set_colorkey((0, 0, 0))
                            blue_surf.fill((0, 0, 255))
                            blue_surf.set_alpha(100)
                            _screen.blit(blue_surf, [self.pos[0], extreme_angles[1][1]])

                        if draw:
                            start_cell = self.wights_mark_2[start_pos[1]][start_pos[0]]
                            now_cell = self.wights_mark_2[i][j]
                            next_cell = now_cell
                            new_line = False
                            if j + 1 >= len(self.wights_mark_2[i]):
                                new_line = True
                            else:
                                next_cell = self.wights_mark_2[i][j + 1]

                            if new_line or start_cell[1] != next_cell[1]:
                                if extreme_angles[0][1] != now_cell[1]:
                                    blue_surf = pg.Surface(
                                        (now_cell[0] - self.pos[0], text.get_height()))
                                    blue_surf.set_colorkey((0, 0, 0))
                                    blue_surf.fill((0, 0, 255))
                                    blue_surf.set_alpha(100)
                                    _screen.blit(blue_surf, [self.pos[0], start_cell[1]])
                                else:
                                    blue_surf = pg.Surface(
                                        (now_cell[0] - start_cell[0], text.get_height()))
                                    blue_surf.set_colorkey((0, 0, 0))
                                    blue_surf.fill((0, 0, 255))
                                    blue_surf.set_alpha(100)
                                    _screen.blit(blue_surf, start_cell)

                                if not new_line:
                                    start_pos = (j + 1, i)

        return _screen
