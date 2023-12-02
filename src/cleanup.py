import os

class CLEANUP:
    def __init__(self):
        self.base_path = '/home/winston/devel/play/golly-4.2-src/Scripts/Python/'
        self.rle_path = self.base_path + 'rles/'
        self.pattern_path = self.base_path + 'ntzfind_patterns/'

    def clear_files(self):
        self.clean_rles()
        self.clean_patterns()

    def clean_rles(self):
        print("Cleaning up rles...")
        rles = os.listdir(self.rle_path)
        for rle in rles:
            if rle.endswith('.rle'):
                os.remove(self.rle_path + rle)

    def clean_patterns(self):
        print("Cleaning up patterns...")
        patterns = os.listdir(self.pattern_path)
        for pattern in patterns:
            if pattern.endswith('.rle'):
                os.remove(self.pattern_path + pattern)
