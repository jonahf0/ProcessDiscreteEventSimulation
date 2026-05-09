from argparse import ArgumentParser
from regex import search,findall
from pprint import pprint

def create_dictionary(file):
    results = {}

    for line in file:
        key = tuple(line.replace("<", " ").replace(">"," ").split()[0:2])
        
        if (not (key in results)):
            results[key] = []
        
        try:

            results[key].append( 
                [
                 item.strip("(") for item in findall("[0-9]{2}:[0-9]{2}:[0-9]{2}|[a-zA-Z0-9_]+\\(",line)[0:2] if len(item)
                 ]
            )
        except Exception as e:
            print(e)


    for key in results.keys():
        results[key] = [ item for item in results[key] if len(item) > 1 ]

    return results


def main(filepath):
    with open(filepath) as f:
        file = [ line.strip() for line in f ]
    
    results = create_dictionary(file)

    print([ result[1] for result in results[list(results.keys())[0]]])

if __name__ == "__main__":
    parser = ArgumentParser(usage="python3 analyze_strace.py <path to strace output>", description='Used to convert output from running "strace -t -Y -yy -f -p <target process PID> -o <output>" into a dataset')
    parser.add_argument("filepath", help="This is the target strace output file")
    args = parser.parse_args()

    main(args.filepath)
