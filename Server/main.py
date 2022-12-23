from space import create_space
from request_handler import create_request_handler
from GUI import App


def main():
    space = create_space()
    request_handler = create_request_handler()
    app = App(space, request_handler)
    app.mainloop()
    space.write_waypoints("waypoints.json")


if __name__ == '__main__':
    main()
