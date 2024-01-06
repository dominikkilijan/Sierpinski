import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Punkty piramidy
vertices = (
    [-0.5,   0,             -1 / 3 * 3 ** 0.5 / 2], # lewy tył
    [ 0.5,   0,             -1 / 3 * 3 ** 0.5 / 2], # prawy tył
    [ 0,     0,              3 ** 0.5 / 3],         # przód
    [ 0,     3 ** 0.5 / 2,   0]                     # szpic
)
colors1 = [
    (68, 16, 110),  # Fioletowy
    (18, 16, 92),  # Niebieski
    (2, 0, 56),  # Granatowy
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
        (tetrahedron[1], tetrahedron[0], tetrahedron[2]),  # jasnozolty 021,102,210 widac ale zle,
        (tetrahedron[0], tetrahedron[3], tetrahedron[2]),  # cyjanowy
        (tetrahedron[0], tetrahedron[1], tetrahedron[3]),  # niebieski
        (tetrahedron[3], tetrahedron[1], tetrahedron[2])  # liliowy 123,231,312 widac ale zolty sie przebija
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
    n = 3
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
    glEnable(GL_DEPTH_TEST)
    #glFrontFace(GL_CCW)
    spinning = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    spinning = not spinning


        if spinning:
            glRotatef(1*n2/2, 0, 1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_CULL_FACE)  # Enable face culling
        for tetrahedron in SiPyramid(n, 0, 0, 0):
            draw_tetrahedron(tetrahedron, colors1)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
