import random


def random_color(colors=None):
    if not colors:
        colors = ['red', 'blue', 'green']
    # colors = ['red', 'grey']
    color = random.choice(colors)
    return color


if __name__ == '__main__':
    print(random_color())
