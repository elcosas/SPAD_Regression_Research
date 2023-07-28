import graph_test.main as test
from sys import argv, exit

def main():
    if len(argv) != 4:
        print('SyntaxError: Must provide 4 valid arguments')
        print('Usage: python3 hist_test_run {mod_name} {method_name} {set #}') 
        exit(1)

    if argv[2] == 'single':
        test.single_hist_test(argv[1], int(argv[3]))
        exit(0)
    if argv[2] == 'multi':
        test.multi_hist_test(argv[1])
        exit(0)
    if argv[2] == 'all':
        test.all_hist_test(argv[1])
        exit(0)

    print('SyntaxError: Invalid method name')
    exit(1)

if __name__ == '__main__':
    main()
