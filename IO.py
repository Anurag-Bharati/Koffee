import pickle
from pickle import UnpicklingError

debugIO = False
USER = ""
loaded = {}


def init(Who):
    global USER
    USER = Who.lower()
    print(f"Hello {USER}\n")


def load():
    global debugIO

    if debugIO:
        print(">inside load()")

    global loaded

    try:
        with open("assets/saves.txt", "rb") as dataIn:
            loaded_data = pickle.load(dataIn)
            loaded = loaded_data
        if debugIO:
            print(">inside load().try:\n")
        return loaded_data

    except EOFError:
        debugIO = True
        if debugIO:
            print(">inside load().except:")
        print("[WARNING] NO PREVIOUS DATA AVAILABLE!\n")

    except FileNotFoundError:
        debugIO = True
        print("[WARNING] saves.txt NOT FOUND")
        print(">creating save.txt\n")
        f = open("assets/saves.txt", "wb")
        f.close()
        load()
    except UnpicklingError:
        debugIO = True
        print("[WARNING] FILE saves.txt IS CORRUPTED!")
        print(">recreating save.txt\n")
        f = open("assets/saves.txt", "wb")
        f.close()
        load()


def save(file):
    if debugIO:
        print(">inside save():")
        print(">DUMPED!\n")
    with open("assets/saves.txt", "wb") as dataOut:
        pickle.dump(file, dataOut)


def load_check(file, name):
    if debugIO:
        print(">inside load_check()")
    if file is not None:
        if debugIO:
            print(">inside load_check() | PREVIOUS FILE EXIST!\n")
        if name in file:
            return True
        else:
            if debugIO:
                print(">inside load_check() | CREATING NEW USER!\n")
            return False
    else:
        if debugIO:
            print(">inside load_check() | [WARNING] PREVIOUS FILE MISSING!")
            print(">now creating one..\n")
        return False


def start(init_data):

    global debugIO

    if load_check(load(), USER):
        if debugIO:
            print(">inside if: | USER EXISTS!")
            print(">now applying data in game..\n")
            print(loaded)
        for i in range(4):
            if i <= 2:
                if loaded.get(USER)[i] < init_data[i]:
                    loaded.get(USER)[i] = init_data[i]
            if i == 3:
                if loaded.get(USER)[i] < init_data[i]:
                    loaded.get(USER)[i] = init_data[i]
        save(loaded)
        debugIO = False
    else:
        if debugIO:
            print(f">inside else: | Saving {USER}'s data.\n")
        loaded[USER] = [0, 0, 0, 0]
        save(loaded)
        debugIO = False
    return loaded.get(USER)
