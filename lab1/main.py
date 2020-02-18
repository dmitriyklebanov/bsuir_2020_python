from sources.fibonacci import fibonacci
from sources.sorting import merge_sort, quick_sort
from sources.text_processing import word_counter, most_common_words

import argparse


def make_parser(parser):
    parser.add_argument('--input-file', type=str, default=None, help='path to input file')
    parser.add_argument('--output-file', type=str, default=None, help='path to output file')

    subparsers = parser.add_subparsers(dest='what')
    subparsers.required = True

    text_processing = subparsers.add_parser('text_processing')
    text_processing.add_argument(
        '--action',
        type=str,
        required=True,
        choices=['word_count', 'most_common_words'])

    sorting = subparsers.add_parser('sorting')
    sorting.add_argument('--sort-type', type=str, required=True, choices=['merge', 'quick'])

    sorting = subparsers.add_parser('fibonacci')


def main(args):
    if args.input_file is None:
        text = input()
    else:
        with open(args.input_file, 'r') as f:
            text = f.read()

    if args.what == 'text_processing':
        if args.action == 'word_count':
            res = word_counter(text)
        elif args.action == 'most_common_words':
            print('Enter the number of words to print:')
            count = int(input())
            res = most_common_words(text, count=count)

    elif args.what == 'sorting':
        res = [int(item) for item in text.split()]

        if args.sort_type == 'merge':
            merge_sort(res)
        elif args.sort_type == 'quick':
            quick_sort(res, 0, len(res))

    elif args.what == 'fibonacci':
        res = list(fibonacci(int(text)))
    elif args.what is None:
        raise ValueError('what is not defined')

    if args.output_file is None:
        print(res)
    else:
        with open(args.output_file, 'w') as f:
            f.write(str(res))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BSUIR Python lab 1')
    make_parser(parser)
    main(parser.parse_args())
