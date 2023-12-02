import os
import re
import qrcode
import json
import random
import imageio

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

class RLE2APGCODE:
    def __init__(self,lifelib):
        self.rle_path = '/home/winston/devel/play/golly-4.2-src/Scripts/Python/rles'
        self.catagolue_URL = 'https://catagolue.hatsya.com/object/'
        self.patterns = {}
        self.lifelib=lifelib

    def return_node(self):
        return {
                  "rle" : "",
                  "rule" : "",
                  "apgcode" : "",
                  "url" : ""
               }

    def extract_data(self, rle):
        try:
            match = re.search(r'rule = ([^ \n]+)', rle)
            rule = match.group(1).lower().replace('/','')

            lt = self.lifelib.load_rules(rule).lifetree(n_layers=1)
            pattern = lt.pattern(rle)
            apgcode = pattern.apgcode
        except Exception as e:
            print(e)
            return None
        return pattern, apgcode, rule

    def make_gif_and_qr(self, pattern, apgcode, rule, url):
        gif = pattern.make_gif(
                hue=random_color(),
                filename='./gifs/'+apgcode+'.gif'
                )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        img = img.resize((450,450))
        img.save('./qrs/' + apgcode + '.png')

    def run(self):
        if len(os.listdir(self.rle_path)) == 0:
            print("No rle files found")
            return

        for filename in os.listdir(self.rle_path):
            self.patterns[filename] = self.return_node()

            file_path = os.path.join(self.rle_path, filename)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                rle = f.read()

            pattern, apgcode, rule = self.extract_data(rle)
            if pattern is None:
                continue
            self.patterns[filename]["rle"] = rle
            self.patterns[filename]["rule"] = rule
            self.patterns[filename]["apgcode"] = apgcode
            self.patterns[filename]["url"] = self.catagolue_URL + apgcode + '/' + rule

            self.make_gif_and_qr(pattern, apgcode, rule, self.patterns[filename]["url"])

        with open('./data/patterns.json', 'w') as json_file:
            json.dump(self.patterns, json_file, indent=4)

        return self.patterns
