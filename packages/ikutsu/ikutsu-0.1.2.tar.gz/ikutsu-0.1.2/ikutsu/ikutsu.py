import fire
import pendulum


def show_age(birthday):
    age = pendulum.parse(birthday).age
    print(f'You are {age} right now!!')


def main():
    fire.Fire(show_age)


if __name__ == '__main__':
    main()
