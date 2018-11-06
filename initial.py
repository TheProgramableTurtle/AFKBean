import shelve


def check_init():
    data = shelve.open("./data/setup/status.db")
    try:
        if data["driver_status"] == "installed":
            print("Driver Check Succesful")
        elif data["driver_status"] == "available":
            print("New drivers need to be installed, please wait")
            # setup code goes here (but I'm bored and I don't want to do that right now
            data["driver_status"] = "installed"
        elif data["driver_status"] == "corrupt":
            print("Critical error: Try reinstalling the program, or clone the repository from GitHub to see a log")
    except:
        print("bad key")
    data.close()


if __name__ == "__main__":
    check_init()
