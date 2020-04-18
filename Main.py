import argparse
from Allcodefiles.training import training
from Allcodefiles.testing import testing
from Allcodefiles.Exceptionhandling import handle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Fake Job Prediction')
    parser.add_argument('-r', '--return_object', choices = ['train', 'test'],
                        default = 'train', type = str,
                        help = 'Select what task to be done')

    args = parser.parse_args()
    var_args = vars(args)

try:
    if(var_args['return_object'] == 'train'):
        training()
    else:
        testing()

except Exception as e:
    handle('Main file')
