import EP_2019.python.pygame as pg

WIDTH = 400
HEIGHT = 400
GREEN = (0, 0, 225)

if __name__ == '__main__':
    """ First step, initialize game container/world/window """
    pg.init()
    clock = pg.time.Clock()

    window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('TaxiSimulation')

    while True:
        # refresh rendering
        window.fill(GREEN)
        pg.display.update()
