import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Punkty piramidy
vertices = (
    [0, 0, 0],
    [1, 0, 0],
    [0.5, 3 ** 0.5 / 2, 0],
    [0.5, 1 / 3 * 3 ** 0.5 / 2, ((3 ** 0.5 / 2) ** 2 - (1 / 3 * 3 ** 0.5 / 2) ** 2) ** 0.5]
)

def Tetron(i, j, k):
    return [
        [sum(x) for x in zip(vertices[0], [i, j, k])],
        [sum(x) for x in zip(vertices[1], [i, j, k])],
        [sum(x) for x in zip(vertices[2], [i, j, k])],
        [sum(x) for x in zip(vertices[3], [i, j, k])]
    ]


def draw_tetrahedron(tetrahedron):
    glBegin(GL_TRIANGLES)
    for face in [
        (tetrahedron[0], tetrahedron[1], tetrahedron[2]),
        (tetrahedron[0], tetrahedron[2], tetrahedron[3]),
        (tetrahedron[0], tetrahedron[3], tetrahedron[1]),
        (tetrahedron[1], tetrahedron[3], tetrahedron[2])
    ]:
        for vertex in face:
            glVertex3fv(vertex)
    glEnd()


def SiPyramid(n, i, j, k):
    if n == 0:
        return [Tetron(i, j, k)]

    s = []
    for u in range(4):
        s.extend(SiPyramid(n - 1, 2 ** (n - 1) * vertices[u][0] + i,
                           2 ** (n - 1) * vertices[u][1] + j,
                           2 ** (n - 1) * vertices[u][2] + k))
    return s


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -15)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1 )
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Adjust the range of the SiPyramid function based on your needs
        for tetrahedron in SiPyramid(3, 0, 0, 0):
            draw_tetrahedron(tetrahedron)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
