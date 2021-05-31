import pickle

level = ""
if not level == "":
    data_dump = open(f"assets/levels/level.dat", "wb")
    pickle.dump(level, data_dump)
    data_dump.close()
