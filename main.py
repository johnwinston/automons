from auto_ntzfind import AUTO_NTZFIND
from rle2apgcode import RLE2APGCODE

def main():
    user_input = input('Run auto-ntzfind? (y/n): ')
    if user_input.lower() == 'y':
        iterations = int(input('Number of iterations: '))
        AUTO_NTZFIND(iterations, period=4).run()

    user_input = input('Run rle2apgcode? (y/n): ')
    if user_input.lower() == 'y':
        RLE2APGCODE().run()

if __name__ == '__main__':
    main()
