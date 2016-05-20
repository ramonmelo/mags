
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Log():
    show_debug = True
    show_log = True

    @staticmethod
    def show(color, name, *msg):
        if Log.show_log:
            print (color + bcolors.BOLD + "[%s]" + bcolors.ENDC + color + " %s" + bcolors.ENDC) % (name, " ".join(map(str, msg)))

    @staticmethod
    def i(*msg): Log.show(bcolors.OKBLUE, "INFO", *msg)

    @staticmethod
    def w(*msg): Log.show(bcolors.WARNING, "WARN", *msg)

    @staticmethod
    def e(*msg): Log.show(bcolors.FAIL, "ERRO", *msg)

    @staticmethod
    def d(*msg):
        if Log.show_debug:
            Log.show(bcolors.OKGREEN, "DBUG", *msg)
