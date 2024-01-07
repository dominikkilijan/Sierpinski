import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy

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

def loadTexture():
    textureSurface = pygame.image.load('cegly.jpg').convert()
    textureData = pygame.image.tostring(textureSurface, "RGBA")
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    #glGenerateTextureMipmap(GL_TEXTURE_2D)

    return texid


def draw_tetrahedron_with_texture(tetrahedron):
    glBegin(GL_TRIANGLES)
    for i, face in enumerate([
        (tetrahedron[0], tetrahedron[1], tetrahedron[2]),  # Fioletowy dobrze
        (tetrahedron[0], tetrahedron[2], tetrahedron[3]),  # Niebieski dobrze
        (tetrahedron[0], tetrahedron[3], tetrahedron[1]),  # Granatowy pod kątem
        (tetrahedron[1], tetrahedron[3], tetrahedron[2])  # Liliowy dobrze
    ]):
        for j, vertex in enumerate(face):
            if i == 0:  # Fioletowy
                if j == 0:
                    glTexCoord2f(0.0, 0.0)
                elif j == 1:
                    glTexCoord2f(0.5, 0.0)
                elif j == 2:
                    glTexCoord2f(0.25, 0.5)
            elif i == 1:  # Niebieski
                #glTexCoord2f(j / 2.0, 1.0 - j / 2.0)
                if j == 0:
                    glTexCoord2f(0.0, 0.0)
                elif j == 1:
                    glTexCoord2f(0.5, 0.0)
                elif j == 2:
                    glTexCoord2f(0.25, 0.5)
            elif i == 2:  # Granatowy
                #glTexCoord2f(0.5 + 0.5 * vertex[0], 0.5 + 0.5 * vertex[1])
                if j == 0:
                    glTexCoord2f(0.5, 0.5)
                elif j == 1:
                    glTexCoord2f(0.75, 1.0)
                elif j == 2:
                    glTexCoord2f(1.0, 0.5)
            elif i == 3:  # Liliowy
                #glTexCoord2f(vertex[0], vertex[1])
                if j == 0:
                    glTexCoord2f(0.5, 0.5)
                elif j == 1:
                    glTexCoord2f(0.75, 1.0)
                elif j == 2:
                    glTexCoord2f(1.0, 0.5)

            glVertex3fv(vertex)
    glEnd()
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
        (tetrahedron[0], tetrahedron[1], tetrahedron[2]),  # Fioletowy
        (tetrahedron[0], tetrahedron[2], tetrahedron[3]),  # Niebieski
        (tetrahedron[0], tetrahedron[3], tetrahedron[1]),  # Granatowy
        (tetrahedron[1], tetrahedron[3], tetrahedron[2])  # Liliowy
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
    n = 0
    n2 = n
    if n == 0:
        n2 += 1

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0, 0, -3*n2**2)

    loadTexture()
    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    # glEnable(GL_COLOR_MATERIAL)
    #
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    #glFrontFace(GL_CCW)
    spinning = False
    colorsOrTex = 2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    spinning = not spinning
                if event.key == pygame.K_r:
                    glLoadIdentity()
                    glTranslatef(0, 0, 0)
                # przesuwanie piramidy
                if event.key == pygame.K_LEFT:
                    glTranslate(-1,0,0)
                if event.key == pygame.K_RIGHT:
                    glTranslate(1,0,0)
                if event.key == pygame.K_UP:
                    glTranslate(0,0.51,0)
                if event.key == pygame.K_DOWN:
                    glTranslate(0,-0.51,0)
                # obracanie piramidy
                if event.key == pygame.K_j:
                    glRotatef(10, 0, -1, 0)
                if event.key == pygame.K_l:
                    glRotatef(10, 0, 1, 0)
                if event.key == pygame.K_i:
                    glRotatef(10, -1, 0, 0)
                if event.key == pygame.K_k:
                    glRotatef(10, 1, 0, 0)
                # wyglad piramidy
                if event.key == pygame.K_1:
                    colorsOrTex = 1
                if event.key == pygame.K_2:
                    colorsOrTex = 2

        #zoomowanie
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                glScale(1.1, 1.1, 1.1)
                event.y = 0
            if event.y < 0:
                glScale(0.9, 0.9, 0.9)
                event.y = 0


        if spinning:
            glRotatef(1*n2/2, 3, 2, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_CULL_FACE)  # Enable face culling
        for tetrahedron in SiPyramid(n, 0, 0, 0):
            if (colorsOrTex == 1):
                draw_tetrahedron(tetrahedron, colors1)
            elif (colorsOrTex == 2):
                glEnable(GL_TEXTURE_2D)
                draw_tetrahedron_with_texture(tetrahedron)
                glDisable(GL_TEXTURE_2D)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
