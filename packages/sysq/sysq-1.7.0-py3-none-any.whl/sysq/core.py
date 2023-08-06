import sys

__version__ = "1.7.0"


def query_executable():
    return sys.executable


def query_platform():
    return sys.platform


def query_path():
    return sys.path


def main():
    res = __version__
    print(f"version: {res}")

    print("")

    res = query_executable()
    print(f"sys.executable: {res}")

    print("")

    res = query_platform()
    print(f"sys.platform: {res}")

    print("")

    res = query_path()
    print(f"sys.path: {res}")

    print("")

    # prevoir PYTHONPATH


# if __name__ == '__main__':
# main()
