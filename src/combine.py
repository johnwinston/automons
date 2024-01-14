from PIL import Image, ImageDraw, ImageFont
import os

class COMBINE:
    def __init__(self,period):
        self.period = period
        self.patterns = {}
        self.patterns_path = './data/' + str(period) + '/patterns.json'

        self.font_path = './fonts/FUTURE/future.ttf'

        self.template_path = './card_backgrounds/template.png'
        self.common_path = './card_backgrounds/common/'
        self.uncommon_path = './card_backgrounds/uncommon/'
        self.rare_path = './card_backgrounds/rare/'
        self.legendary_path = './card_backgrounds/legendary/'
        
        self.common_text = "a common\nspaceship"
        self.uncommon_text = "an uncommon\n    spaceship"
        self.rare_text = "   a rare\nspaceship"
        self.legendary_text = "a legendary\n   spaceship"
        self.golden_text = " the golden\n      glider"
        self.golden_front_path = './card_backgrounds/golden.png'

        if not os.path.exists(self.common_path):
            os.makedirs(self.common_path)
        if not os.path.exists(self.uncommon_path):
            os.makedirs(self.uncommon_path)
        if not os.path.exists(self.rare_path):
            os.makedirs(self.rare_path)
        if not os.path.exists(self.legendary_path):
            os.makedirs(self.legendary_path)

        if period == '4':
            self.rarity_path = self.common_path + 'common_'
            self.text = self.common_text
            self.front_path = './card_backgrounds/common.png'
            self.desc_position = (285, 915)
            self.desc_font_size = 48
        elif period == '5':
            self.rarity_path = self.uncommon_path + 'uncommon_'
            self.text = self.uncommon_text
            self.front_path = './card_backgrounds/uncommon.png'
            self.desc_position = (240, 915)
            self.desc_font_size = 48
        elif period == '6':
            self.rarity_path = self.rare_path + 'rare_'
            self.text = self.rare_text
            self.front_path = './card_backgrounds/rare.png'
            self.desc_position = (285, 915)
            self.desc_font_size = 48
        else:
            self.rarity_path = self.legendary_path + 'legendary_'
            self.text = self.legendary_text
            self.front_path = './card_backgrounds/legendary.png'
            self.desc_position = (245, 915)
            self.desc_font_size = 48
        
        self.back_path = './card_backgrounds/back.png'
        
        self.card_fronts_path = './card_fronts/' + str(period) + '/'
        self.card_backs_path = './card_backs/' + str(period) + '/'

        self.ships_path = './gifs/' + str(period) + '/'
        self.qrs_path = './qrs/' + str(period) + '/'
        
        if not os.path.exists(self.card_fronts_path):
            os.makedirs(self.card_fronts_path)
        if not os.path.exists(self.card_backs_path):
            os.makedirs(self.card_backs_path)
        if not os.path.exists(self.ships_path):
            os.makedirs(self.ships_path)
        if not os.path.exists(self.qrs_path):
            os.makedirs(self.qrs_path)

        self.gif_scale_factor_x = 1.39
        self.gif_scale_factor_y = 1.39
        self.qr_scale_factor_x = .36
        self.qr_scale_factor_y = .36

        self.name_font_size = 55
        self.name_position = (185, 194)

        self.ship_position = (195, 344)
        self.qr_position = (66, 141)

        self.name_center_position = (145, 75)
        self.text_color = (0, 0, 0) # Black

    def load_patterns(self):
        import json
        try:
            with open(self.patterns_path) as f:
                return json.load(f)
        except:
            print("Error loading patterns.json")
        return None

    def run(self):
        self.patterns = self.load_patterns()
        if self.patterns is None:
            return
        self.merge_ships_with_card_front()
        self.merge_qr_codes_with_card_back()
        self.merge_card_front_with_template()
        self.merge_card_back_with_template()

    def get_ships_from_gif_directory(self):
        import os
        ships = []
        for file in os.listdir(self.ships_path):
            if file.endswith(".gif"):
                ships.append(file)
        return ships

    def get_qr_codes_from_qr_directory(self):
        import os
        qr_codes = []
        for file in os.listdir(self.qrs_path):
            if file.endswith(".png"):
                qr_codes.append(file)
        return qr_codes

    def get_card_fronts_from_card_fronts_directory(self):
        import os
        card_fronts = []
        for file in os.listdir(self.card_fronts_path):
            if file.endswith(".png"):
                card_fronts.append(file)
        return card_fronts

    def get_card_backs_from_card_backs_directory(self):
        import os
        card_backs = []
        for file in os.listdir(self.card_backs_path):
            if file.endswith(".png"):
                card_backs.append(file)
        return card_backs

    def merge_card_back_with_template(self):
        template_image = Image.open(self.template_path)
        x_offset = 3300 - 150 - 750
        y_offset = 375
        i = 0
        page = 1
        for card_back in self.get_card_backs_from_card_backs_directory():
            if i % 4 == 0 and i != 0:
                y_offset += 1087
                x_offset = 3300 - 150 - 750
            if i % 16 == 0 and i != 0:
                template_image.save(self.rarity_path + 'back_' + str(page) + '.png')
                page = page + 1
                template_image = Image.open(self.template_path)
                y_offset = 375
            back_image = Image.open(self.card_backs_path + card_back)
            # Crop the left and the right sides of the card back by 21 pixels
            back_image = back_image.crop((21, 0, 279, 400))
            # Remove 8 pixels from the right side of the card back
            back_image = back_image.crop((0, 0, 249, 400))
            # Remove 21 pixels from the top of the card back
            back_image = back_image.crop((0, 21, 249, 400))
            # Remove 21 pixels from the bottom of the card back
            back_image = back_image.crop((0, 0, 249, 362))
            width, height = back_image.size
            width = width + 3
            height = height + 1
            back_image = back_image.resize((int(width * 3), int(height * 3)))
            template_image.paste(back_image, (x_offset, y_offset), back_image)
            x_offset -= 750
            i = i + 1

        template_image.save(self.rarity_path + 'back_' + str(page) + '.png')


    def merge_card_front_with_template(self):
        template_image = Image.open(self.template_path)
        x_offset = 150
        y_offset = 375
        i = 0
        page = 1
        for card_front in self.get_card_fronts_from_card_fronts_directory():
            if i % 4 == 0 and i != 0:
                y_offset += 1087
                x_offset = 150
            if i % 16 == 0 and i != 0:
                template_image.save(self.rarity_path + 'front_' + str(page) + '.png')
                page = page + 1
                template_image = Image.open(self.template_path)
                y_offset = 375
            front_image = Image.open(self.card_fronts_path + card_front)
            width, height = front_image.size
            # Crop all sides of the card front by 63 pixels
            width = width - 63
            height = height - 63
            front_image = front_image.crop((63, 63, width, height))

            template_width = 750
            template_height = 1088
            front_image = front_image.resize((int(template_width), int(template_height)))
            template_image.paste(front_image, (x_offset, y_offset), front_image)
            x_offset += 750
            i = i + 1

        template_image.save(self.rarity_path + 'front_' + str(page) + '.png')

    def merge_qr_codes_with_card_back(self):
        for qr_code in self.get_qr_codes_from_qr_directory():
            back_image = Image.open(self.back_path)
            qr_code_image = Image.open(self.qrs_path + qr_code)

            width, height = qr_code_image.size
            scaled_width = int(width * self.qr_scale_factor_x)
            scaled_height = int(height * self.qr_scale_factor_y)
            qr_code_image = qr_code_image.resize((scaled_width, scaled_height))

            qr_code_image = qr_code_image.convert('RGBA')
            back_image.paste(qr_code_image, self.qr_position, qr_code_image)

            back_image.save(self.card_backs_path+qr_code[:-4]+'.png')

    def merge_ships_with_card_front(self):
        from unique_names_generator import get_random_name

        for ship in self.get_ships_from_gif_directory():
            if ship == 'glider.gif':
                front_image = Image.open(self.golden_front_path)
            else:
                front_image = Image.open(self.front_path)
            ship_image = Image.open(self.ships_path + ship)

            width, height = ship_image.size
            scaled_width = int(width * self.gif_scale_factor_x)
            scaled_height = int(height * self.gif_scale_factor_y)
            ship_image = ship_image.resize((scaled_width, scaled_height))

            ship_image = ship_image.convert('RGBA')
            front_image.paste(ship_image, self.ship_position, ship_image)

            draw = ImageDraw.Draw(front_image)
            font = ImageFont.truetype(self.font_path, self.name_font_size)
            if self.period == "life":
                name = ship[:-4]
                name = name.replace("_", " ")
            else:
                name = get_random_name()
                while (len(name) >= 11):
                    name = get_random_name()
            draw.text(self.name_position, name, font=font, fill=self.text_color)

            draw = ImageDraw.Draw(front_image)
            font = ImageFont.truetype(self.font_path, self.desc_font_size)
            if ship == 'glider.gif':
                draw.text(self.desc_position,
                    self.golden_text,
                    font=font,
                    fill=self.text_color)
            else:
                draw.text(self.desc_position,
                        self.text,
                        font=font,
                        fill=self.text_color)

            front_image.save(self.card_fronts_path + ship[:-4] + '.png')


