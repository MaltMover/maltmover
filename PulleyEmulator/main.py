from app import App
from fake_pulley import FakePulley


def main():
    fp = FakePulley()
    app = App(fp)
    fp.prep_length = 69
    fp.prep_time = 10
    app.update_values()
    app.mainloop()
    app.kill()


if __name__ == '__main__':
    main()
