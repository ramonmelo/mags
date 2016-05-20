from cmd2 import Cmd

class GSCmd(Cmd):

    prompt = "(MGS) > "

    def __init__(self, *args,  **kwarg):
        Cmd.__init__(self, *args, **kwarg)

if __name__ == "__main__":
    GSCmd().cmdloop()

