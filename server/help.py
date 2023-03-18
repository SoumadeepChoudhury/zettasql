def help():
    docs_url = ""
    with open("./client/info.log", 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("docs_url :"):
                docs_url = line.split("docs_url :")[1].strip()
    print(f"Refer to this documentation link: {docs_url}")


if __name__ == "__main__":
    help()
