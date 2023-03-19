def help():
    PATH = __file__ if '/' in __file__ else __file__.replace("\\", "/")
    PATH = PATH[:PATH.rfind("/")]
    PATH = PATH[:PATH.rfind("/")]
    docs_url = ""
    with open(f"{PATH}/zclient/info.log", 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("docs_url :"):
                docs_url = line.split("docs_url :")[1].strip()
    print(f"Refer to this documentation link: {docs_url}")


if __name__ == "__main__":
    help()
