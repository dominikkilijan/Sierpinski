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
colors = [
    (182, 209, 92),  # Jasnozolty
    (11, 144, 156),  # Cyjanowy
    (21, 11, 156),  # Niebieski
    (134, 63, 191)  # Liliowy
]
def Tetron(i, j, k):
    return [
        [sum(x) for x in zip(vertices[0], [i, j, k])],
        [sum(x) for x in zip(vertices[1], [i, j, k])],
        [sum(x) for x in zip(vertices[2], [i, j, k])],
        [sum(x) for x in zip(vertices[3], [i, j, k])]
    ]


def draw_tetrahedron(tetrahedron, colors):
    glBegin(GL_TRIANGLES)
    for i, face in enumerate([
        (tetrahedron[0], tetrahedron[2], tetrahedron[1]),  # jasnozolty
        (tetrahedron[0], tetrahedron[3], tetrahedron[2]),  # cyjanowy
        (tetrahedron[0], tetrahedron[1], tetrahedron[3]),  # niebieski
        (tetrahedron[1], tetrahedron[2], tetrahedron[3])  # liliowy
    ]):
        glColor3ub(*colors[i])
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
    n = 2
    n2 = n
    if n == 0:
        n2 += 1

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-n2*2, -n2*1.2, -9*n2)

    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    # glEnable(GL_COLOR_MATERIAL)
    #
    # glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 4, 3, 2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_CULL_FACE)  # Enable face culling
        for tetrahedron in SiPyramid(n, 0, 0, 0):
            draw_tetrahedron(tetrahedron, colors)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
