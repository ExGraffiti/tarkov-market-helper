from mouse import get_position
from cv2 import cvtColor, threshold, COLOR_RGB2GRAY
from numpy import array
from PIL import ImageGrab
from pytesseract import image_to_string


class Scan:
    def __init__(self, screen_width, screen_height):
        """
        Scan that taking screenshot every time when MainFrame is updating and then set item_hash
        """
        try:
            self.delta_x = 11
            self.delta_y = 11

            screen_image = ImageGrab.grab()
            self.screen_image = cvtColor(array(screen_image), COLOR_RGB2GRAY)
            self.mouse_position_x, self.mouse_position_y = get_position()
            self.item_hash = None
            self.start_shade = 1
            self.start_position_x, self.start_position_y = (0, 0)
            self.item_image = None


            self.resolution = 0
            if screen_width == 1920:
                self.resolution = 1
            elif screen_width == 2560:
                self.resolution = 2

            if self.mouse_position_x < (screen_width * 0.99) and self.mouse_position_y > (screen_height * 0.01):
                self.find_start_shade()

            if not self.start_shade:
                self.find_item_image()
                self.hash_item_image()

        except OSError as error:
            print(error)



    def delta_scan(self):
        if self.resolution == 1:
            x_pix, y_pix = 11, 11
        elif self.resolution == 2:
            x_pix, y_pix = 15, 15

        else:
            x_pix, y_pix = 11, 11
        for y_pix in range(5, 35):
            for x_pix in range(5, 35):
                shade = self.screen_image[self.mouse_position_y - y_pix, self.mouse_position_x + x_pix]

                if shade == 0:
                    self.delta_x, self.delta_y = x_pix, y_pix
                    return
        self.delta_x, self.delta_y = x_pix, y_pix





    def find_start_shade(self):
        """
        Find shade that will be remembered like start position
        """
        if self.resolution != 1:
            self.delta_scan()

        self.start_position_x, self.start_position_y = self.mouse_position_x + self.delta_x, self.mouse_position_y - self.delta_y

        self.start_shade = self.screen_image[self.start_position_y, self.start_position_x]

    def find_right_corner(self):
        """
        Will search right border that equal to 87
        """
        mem = 0
        count = 0
        mem_zero = 0

        for pix in range(0, 500):
            try:
                shade = self.screen_image[self.start_position_y, self.start_position_x + pix]

                if mem == shade:
                    count += 1
                else:
                    count = 0

                if shade != 0:
                    mem = shade
                if shade == 0:
                    mem_zero += 1


                elif shade >= 87 or shade == 18 or count > 5 or (mem_zero > 5 and shade > 1):
                    return self.start_position_x + pix

                else:
                    break

            except IndexError as error:
                print(error)
                print(self.start_position_y, self.start_position_x, pix)

    def find_top_corner(self, left_corner_position_x):
        """
        Will search top border that equal to 87
        """
        mem = 0
        count = 0
        mem_zero = 0
        for pix in range(0, 300):
            shade = self.screen_image[self.start_position_y - pix, left_corner_position_x]

            if mem == shade:
                count += 1
            else:
                count = 0
            if shade != 0:
                mem = shade
            if shade == 0:
                mem_zero += 1


            elif shade >= 87 or shade == 18 or count > 5 or (mem_zero > 5 and shade > 1):
                return self.start_position_y - pix + 1

            else:
                break

    def find_item_image(self):
        """
        Method search right_corner and top_corner that needed for finding item_image
        """
        right_corner_position_x = self.find_right_corner()
        if right_corner_position_x:
            top_corner_position_y = self.find_top_corner(self.start_position_x)

            if top_corner_position_y:
                width = right_corner_position_x - self.start_position_x
                height = self.start_position_y - top_corner_position_y
                crop_screen_image = self.screen_image[top_corner_position_y:top_corner_position_y + height,
                                    self.start_position_x:self.start_position_x + width]
                ret, self.item_image = threshold(crop_screen_image, 0, 255, 0)
                self.item_image = crop_screen_image


    def name_corrector(self):
        name = str(self.item_hash)
        name = name.replace('Gen2', 'Gen.2')
        name = name.replace('@', '0')
        name = name.replace('*', '"')
        if 'WD-40' in name:
            ml = name.split('(')[1]
            name = f'WD-40 ({ml[0]}00ml)'
        name = name.replace('x5i', 'x51')
        name = name.replace('762', '7.62')
        name = name.replace('FM)', 'FMJ')
        name = name.replace('225-', '2.25-')
        name = name.replace('Sx', '9x')
        name = name.replace('Vitor', 'Vltor')
        name = name.replace('х59', 'x39')
        name = name.replace('28-round', '20-round')
        name = name.replace('KIASS', 'KlASS')

        return name


    def hash_item_image(self):
        """
        Set item_hash for item_image
        """
        if self.item_image is not None:

            try:
                string = image_to_string(self.item_image, lang='eng')
                string = str(string)[:-1]
                self.item_hash = string.replace('\n', ' ')
                self.item_hash = self.name_corrector()

                print(f'Found: {self.item_hash}')
            except:
                self.item_image = None
