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
        self.rlePath = '/home/winston/devel/play/golly-4.2-src/Scripts/Python/rles'
        self.catagolueURL = 'https://catagolue.hatsya.com/object/'
        self.patterns = {}
        self.lifelib=lifelib

    def returnNode(self):
        return {
                  "rle" : "",
                  "rule" : "",
                  "apgcode" : "",
                  "url" : ""
               }

    def run(self):
        if not os.path.exists('./patterns.json'):
            for filename in os.listdir(self.rlePath):
                self.patterns[filename] = self.returnNode()
                file_path = os.path.join(self.rlePath, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        rle = f.read()
                    match = re.search(r'rule = ([^ \n]+)', rle)
                    if match:
                        rule = match.group(1).lower().replace('/','')
                    lt = self.lifelib.load_rules(rule).lifetree(n_layers=1)
                    pattern = lt.pattern(rle)
                    apgcode = pattern.apgcode
                    gif = pattern.make_gif(hue=random_color())
                    imageio.mimsave('./gifs/' + apgcode + str(rule) + '.gif', gif, fps=60)
                    url = self.catagolueURL + apgcode + '/' + rule
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
                    
                    self.patterns[filename]["rle"] = rle
                    self.patterns[filename]["rule"] = rule
                    self.patterns[filename]["apgcode"] = apgcode
                    self.patterns[filename]["url"] = url
            with open('patterns.json', 'w') as json_file:
                json.dump(self.patterns, json_file, indent=4)
        else:
            with open('patterns.json', 'r') as json_file:
                self.patterns = json.load(json_file)
