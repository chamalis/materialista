import threading

from fotocasa import FotoCasaClient
from idealista import IdeaListaClient


def main():
    idea_cli = IdeaListaClient()
    foto_cli = FotoCasaClient()

    t1 = threading.Thread(target=idea_cli.find_new).start()
    # t2 = threading.Thread()

    # idea_cli.refresh_listings()
    t1.join()


if __name__ == "__main__":
    main()
