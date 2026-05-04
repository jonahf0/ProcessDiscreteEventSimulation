import simpy
import random


class SysCall(simpy.events.Event):
    def __init__(self,env,name):
        super().__init__(env)
        self.name = name

class Sshd:
    def __init__(self, env):
        self.env = env
        self.sessions = []
        self.handle = simpy.Resource(env, 3)

    def new_connection(self, username):
        print(f"At time {self.env.now}, new connection from: {username}")
        yield self.env.timeout(1)
        print("Handshake successful")
        self.sessions.append(username)
        testSyscall = SysCall(self.env,"fcntl")
        yield testSyscall.succeed()
        print(f"call {testSyscall.name} succeeded")

    def exit(self, username):
        print(f"Checking for user session...")
        yield self.env.timeout(1)
        if (username in self.sessions):
            print("Session found--disconnecting")
            self.sessions.remove(username)
        else:
            print("Session not found")



class User:
    def __init__(self, env, username, server):
        self.env = env
        self.username = username
        self.server = server
        self.action = env.process(self.connect(self.server))

    def connect(self, server):
        print(f"User {self.username} wants to connect to server") 
        with self.server.handle.request() as request:
            yield request
            yield self.env.process(server.new_connection(self.username))
            print("Session established")
            yield self.env.timeout(random.randrange(0,100))
            print("Session finished after 10 seconds")
            yield self.env.process(server.exit(self.username))
            print("Session successfully disconnected")


if __name__ == "__main__":
    env = simpy.Environment()
    server = Sshd(env)
    users = [ User(env, f"user{i}", server) for i in range(0,5) ]
    env.run(until=100)
