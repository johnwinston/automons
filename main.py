from src.auto_ntzfind import AUTO_NTZFIND
from src.rle2apgcode import RLE2APGCODE
from src.cleanup import CLEANUP
from src.combine import COMBINE
from submodules import lifelib

def main():
    '''
    user_input = input('Clear golly files? (y/n): ')
    if user_input.lower() == 'y':
        CLEANUP().clear_files()

    user_input = input('Run auto-ntzfind? (y/n): ')
    if user_input.lower() == 'y':
        iterations = int(input('Number of iterations: '))
        AUTO_NTZFIND(iterations, period=4).run()
    user_input = input('Run rle2apgcode? (y/n): ')
    if user_input.lower() == 'y':
        RLE2APGCODE(lifelib).run()
    '''

    user_input = input('Combine cards? (y/n): ')
    if user_input.lower() == 'y':
        COMBINE().run()

if __name__ == '__main__':
    main()
