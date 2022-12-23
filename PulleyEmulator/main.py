from app import App
from fake_pulley import FakePulley


def main():
    fp = FakePulley()
    app = App(fp)
    app.mainloop()


if __name__ == '__main__':
    main()
