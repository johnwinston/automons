from PIL import Image, ImageDraw, ImageFont

class COMBINE:
    def __init__(self):
        self.patterns = {}
        self.patterns_path = './data/patterns.json'

        self.font_path = './fonts/FUTURE/future.ttf'

        self.template_path = './card_backgrounds/template.png'

        self.front_path = './card_backgrounds/common.png'
        self.back_path = './card_backgrounds/back.png'
        
        self.card_fronts_path = './card_fronts/'
        self.card_backs_path = './card_backs/'

        self.ships_path = './gifs/'
        self.qrs_path = './qrs/'

        self.gif_scale_factor_x = .465
        self.gif_scale_factor_y = .465
        self.qr_scale_factor_x = .36
        self.qr_scale_factor_y = .36

        self.name_font_size = 20
        self.desc_font_size = 18
        self.name_position = (63, 64)
        self.desc_position = (90, 302)

        self.ship_position = (65, 114)
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

    def merge_card_front_with_template(self):
        template_image = Image.open(self.template_path)
        x_offset = 70
        y_offset = 25
        for card_front in self.get_card_fronts_from_card_fronts_directory():
            front_image = Image.open(self.card_fronts_path + card_front)
            # Crop the left and the right sides of the card front by 21 pixels
            front_image = front_image.crop((21, 0, 279, 400))
            # Remove 8 pixels from the right side of the card front
            front_image = front_image.crop((0, 0, 249, 400))
            # Remove 21 pixels from the top of the card front
            front_image = front_image.crop((0, 21, 249, 400))
            # Remove 21 pixels from the bottom of the card front
            front_image = front_image.crop((0, 0, 249, 362))

            # Rotate the card front 90 degrees
            front_image = front_image.rotate(90, expand=True)

            template_image.paste(front_image, (x_offset, y_offset), front_image)
            x_offset += 400

        template_image.save('./front_template.png')

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

            back_image.save('./card_backs/'+qr_code[:-4]+'.png')

    def merge_ships_with_card_front(self):
        from unique_names_generator import get_random_name

        for ship in self.get_ships_from_gif_directory():
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
            name = get_random_name()
            while (len(name) >= 12):
                name = get_random_name()
            draw.text(self.name_position, name, font=font, fill=self.text_color)

            draw = ImageDraw.Draw(front_image)
            font = ImageFont.truetype(self.font_path, self.desc_font_size)
            draw.text(self.desc_position,
                    "a common\nspaceship",
                    font=font,
                    fill=self.text_color)

            front_image.save('./card_fronts/'+ship[:-4]+'.png')


