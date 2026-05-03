from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(usage="python3 analyze_strace.py <path to strace output>", description='Used to convert output from running "strace -t -Y -yy -f -p <target process PID> -o <output>" into a dataset')
    parser.add_argument("filepath", help="This is the target strace output file")
    args = parser.parse_args()

    main(args.filepath)
