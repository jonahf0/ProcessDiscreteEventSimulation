from simpy import Environment
from simpy.events import Event
from pprint import pprint

class SysCall(Event):
    def __init__(self,env,name):
        super().__init__(env)
        self.name = name
        self.action = self.env.timeout

class Process:
    def __init__(self, env, pid, name, tracelist):
        self.env = env
        self.pid = pid
        self.name = name
        self.call_list = [ SysCall(env,call) for call in tracelist ]
        self.action = env.process(self._execute())

    def _execute(self):
        print(f"process {self.pid}:{self.name} executing")
        for call in self.call_list:
            print(f"call {call.name} at {self.env.now}")
            yield call.action(10) if call.name in ["accept","getpeername"] else call.action(0)


if __name__ == "__main__":

    call_list = ['ppoll', 'rt_sigprocmask', 'accept', 'fcntl', 'socketpair', 'getpeername', 'fcntl', 'fcntl', 'getpeername', 'getsockname', 'getpeername', 'getsockname', 'getpeername', 'rt_sigprocmask', 'clone', 'rt_sigprocmask', 'close', 'close', 'getrandom', 'getpid', 'getpid', 'rt_sigprocmask', 'ppoll', 'rt_sigprocmask', 'write', 'getpid', 'getpid', 'getpid', 'getpid', 'getpid', 'getpid', 'munmap', 'mmap', 'madvise', 'munmap', 'mmap', 'madvise', 'munmap', 'mmap', 'madvise', 'rt_sigprocmask', 'ppoll', 'rt_sigprocmask', 'write', 'rt_sigprocmask', 'ppoll', 'rt_sigprocmask', 'read', 'rt_sigprocmask', 'ppoll', 'rt_sigprocmask', 'read', 'close', 'rt_sigprocmask', 'ppoll', 'rt_sigreturn', 'rt_sigprocmask', 'rt_sigprocmask', 'wait4', 'wait4', 'ppoll']

    env = Environment()
    
    test = Process(env, "123", "sshd", call_list)

    print(test.call_list)

    env.run(until=100) 
