#!/usr/bin/env python

from idealista import IdealistaClient


def main():
    # add threads if more clients (e.g fotocasa) are implemented
    idea_cli = IdealistaClient()
    status = 0

    try:
        idea_cli.find_new()
    except Exception as e:
        status = 1
        print(e)
        raise e
    finally:
        idea_cli.exit(status)


if __name__ == "__main__":
    main()
