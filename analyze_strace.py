from argparse import ArgumentParser
from regex import search,findall
from pprint import pprint
from pathlib import Path
from itertools import chain


#structure for creating processes and tracking their children
class ProcTree:
    def __init__(self, name, pid):
        self.pid = pid
        self.name = name
        self.children = []
        self.call_list = []
        

    def create_child(self, name, pid):
        self.children.append( (proc:=ProcTree(name, pid)) )
        return proc

    def add_call(self, call):
        self.call_list.append(call)
    
    def __str__(self):
        #return f"{self.pid}|{self.name} -- {', '.join(list(map(lambda a: f'{a.pid}|{a.name}', self.children)))}"
        return f"{self.pid}<{self.name}>: {', '.join([ f'{proc.pid}<{proc.name}>' for proc in self.children ])}" 

#takes the raw file split into lines
def create_process_tree(file):
    
    #using a map to avoid duplicating a massive file into mem
    split_lines = map(lambda line: line.split(" "), file)
    
    all_procs = dict()
    root = None
    while ( (line:=next(split_lines, None)) != None ):
        proc_sig, time, call = line[0:3]
        pid, name = proc_sig.replace(">", "").replace("<", " ").split(" ")

        sig = (pid,name)
        if not ( sig in all_procs ):
            all_procs[sig] = ProcTree(name, pid)
            root=sig if len(all_procs)==1 else root

        current_proc = all_procs[sig]
            
        #use a match in case there's other weird calls to handle
        match (call_name:=call.split("(")[0]):
            case "clone":
                #second to last item for a line that says "clone" should look like PID<PROC>;
                #if not, try assuming the original
                child_info = line[-2].strip()
                c_pid, c_name = child_info.replace(">","").replace("<", " ").split(" ")
                child = current_proc.create_child(c_name, c_pid)
                all_procs[(c_pid,c_name)] = child

            case "execve":
                new_name = call.split('("')[1].split("/")[-1].strip('",')
 
                current_proc = all_procs.pop(sig)
                all_procs[(sig[0], new_name)] = current_proc
                current_proc.name = new_name
        
        
        current_proc.add_call( (call_name, time, line[-1].replace("<","").replace(">","").strip() ) )
    
    return root,all_procs

def main(filepath,root):
    
    files = [ str(file) for file in Path(filepath).iterdir() ]
    
    #this locates the trace file for the root process first; this helps to insert it at the beginning of the list for processing
    root_file = [ file for file in files if root in file ][0]
    files.remove(root_file)
    
    combined_file = [ line for line in open(root_file) ]

    combined_file = chain.from_iterable( [combined_file] + [ [ line.strip() for line in open(f) ] for f in files ] ) 
    
    root_sig, results = create_process_tree(combined_file)

    pprint( [ str(results[proc]) for proc in results ] )

    for proc in results:
        print(results[proc].call_list)


if __name__ == "__main__":
    parser = ArgumentParser(usage="python3 analyze_strace.py <path to strace output> <root file>", description='Used to convert output from running "strace -t -T -Y -yy --always-show-pid -ff -p <target process PID> -o <output>" into a dataset')
    parser.add_argument("filepath", help="This is the target strace output file")
    parser.add_argument("root", help="This is the file for the root process (i.e., the one that you targeted with the -p flag in strace")
    args = parser.parse_args()
    
    main(args.filepath, args.root)
