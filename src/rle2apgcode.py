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
    def __init__(self,lifelib,period):
        self.period = str(period)
        self.rle_path = '/home/winston/devel/play/golly/Scripts/Python/rles/' + str(period)
        self.pythlib_path = './submodules/lifelib/pythlib/'
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
        if not os.path.exists('./gifs/'+self.period):
            os.makedirs('./gifs/'+self.period)

        gif = pattern.make_gif(
                hue=random_color(),
                filename='./gifs/'+self.period+'/'+apgcode+'.gif'
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

    def cleanup_shared_objects(self):
        for filename in os.listdir(self.pythlib_path):
            if filename.endswith(".so"):
                os.remove(os.path.join(self.pythlib_path, filename))

    def run(self):
        if len(os.listdir(self.rle_path)) == 0:
            print("No rle files found. Run automons.py in Golly")
            return False

        for filename in os.listdir(self.rle_path):
            self.patterns[filename] = self.return_node()

            file_path = os.path.join(self.rle_path, filename)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                rle = f.read()

            try:
                pattern, apgcode, rule = self.extract_data(rle)
            except Exception as e:
                print(e)
                continue
            if pattern is None:
                continue
            self.patterns[filename]["rle"] = rle
            self.patterns[filename]["rule"] = rule
            self.patterns[filename]["apgcode"] = apgcode
            self.patterns[filename]["url"] = self.catagolue_URL + apgcode + '/' + rule

            self.make_gif_and_qr(pattern, apgcode, rule, self.patterns[filename]["url"])
            self.cleanup_shared_objects()

        if not os.path.exists('./data/' + self.period):
            os.makedirs('./data/' + self.period)
        with open('./data/' + self.period + '/patterns.json', 'w') as json_file:
            json.dump(self.patterns, json_file, indent=4)

        return self.patterns
