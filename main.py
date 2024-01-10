import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy

global n, n2, light_position
n = 2
n2 = n
if n == 0:
    n2 += 1

light_position = [-3.0, 3.0, 3.0, 1.0]

# Punkty piramidy
vertices = (
    [-0.5,   0,             -1 / 3 * 3 ** 0.5 / 2], # lewy tył
    [ 0.5,   0,             -1 / 3 * 3 ** 0.5 / 2], # prawy tył
    [ 0,     0,              3 ** 0.5 / 3],         # przód
    [ 0,     3 ** 0.5 / 2,   0]                     # szpic
)

colors1 = [
    (89, 5, 5),
    (148, 3, 3),
    (181, 71, 7),
    (181, 111, 7)
]
colors2 = [
    (66, 145, 20),
    (47, 102, 15),
    (32, 71, 9),
    (14, 31, 4)
]
colors3 = [
    (68, 16, 110),  # Fioletowy
    (18, 16, 92),  # Niebieski
    (2, 0, 56),  # Granatowy
    (134, 63, 191)  # Liliowy
]
colors4 = [
    (89, 5, 5),
    (89, 5, 5),
    (89, 5, 5),
    (89, 5, 5)
]

# rysowanie piramidy z kolorowymi ścianami
def draw_pyramid(tetrahedron, colors):
    glBegin(GL_TRIANGLES)
    for i, face in enumerate([
        (tetrahedron[0], tetrahedron[1], tetrahedron[2]),  # Fioletowy
        (tetrahedron[0], tetrahedron[2], tetrahedron[3]),  # Niebieski
        (tetrahedron[0], tetrahedron[3], tetrahedron[1]),  # Granatowy
        (tetrahedron[1], tetrahedron[3], tetrahedron[2])  # Liliowy
    ]):
        glNormal3fv(numpy.cross(numpy.subtract(face[1], face[0]), numpy.subtract(face[2], face[0])))
        glColor3ub(*colors[i])
        for vertex in face:
            glVertex3fv(vertex)
    glEnd()
# rysowanie piramidy z nałożoną teksturą
def draw_pyramid_with_texture(tetrahedron):
    glBegin(GL_TRIANGLES)
    for i, face in enumerate([
        (tetrahedron[0], tetrahedron[1], tetrahedron[2]),
        (tetrahedron[0], tetrahedron[2], tetrahedron[3]),
        (tetrahedron[0], tetrahedron[3], tetrahedron[1]),
        (tetrahedron[1], tetrahedron[3], tetrahedron[2])
    ]):
        for j, vertex in enumerate(face):
            if i == 0 or i == 1:
                if j == 0:
                    glTexCoord2f(0.0, 0.0)
                elif j == 1:
                    glTexCoord2f(0.5, 0.0)
                elif j == 2:
                    glTexCoord2f(0.25, 0.5)
            elif i == 2 or i == 3:
                if j == 0:
                    glTexCoord2f(0.5, 0.5)
                elif j == 1:
                    glTexCoord2f(0.75, 1.0)
                elif j == 2:
                    glTexCoord2f(1.0, 0.5)

            glNormal3fv(numpy.cross(numpy.subtract(face[1], face[0]), numpy.subtract(face[2], face[0])))
            glVertex3fv(vertex)
    glEnd()
# załadowanie konkretnej tekstury i ustawienie odpowiednich parametrów
def load_texture():
    textureSurface = pygame.image.load('missing.jpg').convert()
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

    return texid
# ustawienie oświatlenia
def set_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    glLight(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, 40.0)
# rysowanie małego sześcianu reprezentującego lampę, jest zawsze w miejsu źródła światła
def draw_light_cube(light_position):
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(light_position[0], light_position[1], light_position[2])
    glDisable(GL_LIGHTING) # po wyłączeniu oświetlenia bardziej wygląda jakby się świeciła

    size = 0.1
    glBegin(GL_QUADS)

    glVertex3f(size, -size, -size)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)

    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)

    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(-size, -size, size)

    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)

    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, size, -size)

    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(size, -size, size)
    glEnd()

    glPopMatrix()
    glEnable(GL_LIGHTING)
# zmiana położenia piramidy o wektor (i,j,k)
def move_pyramid_to_different_place(i, j, k):
    return [
        [sum(x) for x in zip(vertices[0], [i, j, k])],
        [sum(x) for x in zip(vertices[1], [i, j, k])],
        [sum(x) for x in zip(vertices[2], [i, j, k])],
        [sum(x) for x in zip(vertices[3], [i, j, k])]
    ]
# rekurencyjna funkcja do generowania kolejnych współrzędnych piramid
def draw_n_pyramids(n, i, j, k):
    if n == 0:
        return [move_pyramid_to_different_place(i, j, k)]

    s = []
    for u in range(4):
        s.extend(draw_n_pyramids(n - 1, 2 ** (n - 1) * vertices[u][0] + i,
                                 2 ** (n - 1) * vertices[u][1] + j,
                                 2 ** (n - 1) * vertices[u][2] + k))
    return s

def main():

    pygame.init()
    n = int(input("n = "))
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0, 0, -3*n2**2)

    load_texture()
    set_lighting()

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    spinning = False
    lighting = True
    colorsOrTex = 4

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spinning = not spinning
                if event.key == pygame.K_s:
                    lighting = not lighting

                # przesuwanie piramidy
                if event.key == pygame.K_LEFT:
                    glTranslate(-1,0,0)
                if event.key == pygame.K_RIGHT:
                    glTranslate(1,0,0)
                if event.key == pygame.K_UP:
                    glTranslate(0,0.5,0)
                if event.key == pygame.K_DOWN:
                    glTranslate(0,-0.5,0)

                # obracanie piramidy
                if event.key == pygame.K_j:
                    glRotatef(10, 0, -1, 0)
                if event.key == pygame.K_l:
                    glRotatef(10, 0, 1, 0)
                if event.key == pygame.K_i:
                    glRotatef(10, -1, 0, 0)
                if event.key == pygame.K_k:
                    glRotatef(10, 1, 0, 0)
                if event.key == pygame.K_o:
                    glRotatef(10, 0, 0, -1)
                if event.key == pygame.K_u:
                    glRotatef(10, 0, 0, 1)

                # wyglad piramidy
                if event.key == pygame.K_1:
                    colorsOrTex = 1
                if event.key == pygame.K_2:
                    colorsOrTex = 2
                if event.key == pygame.K_3:
                    colorsOrTex = 3
                if event.key == pygame.K_4:
                    colorsOrTex = 4

                # światlo
                if event.key == pygame.K_t:
                    light_position[1] += 1.0
                if event.key == pygame.K_g:
                    light_position[1] -= 1.0
                if event.key == pygame.K_f:
                    light_position[0] -= 1.0
                if event.key == pygame.K_h:
                    light_position[0] += 1.0
                if event.key == pygame.K_r:
                    light_position[2] -= 1.0
                if event.key == pygame.K_y:
                    light_position[2] += 1.0
        #zoomowanie
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                glScale(1.1, 1.1, 1.1)
                event.y = 0
            if event.y < 0:
                glScale(0.9, 0.9, 0.9)
                event.y = 0
        # kręcenie się
        if spinning:
            glRotatef(1*n2/2, 0, 1, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_CULL_FACE)

        # czy włączone oświetlenie
        if lighting:
            glEnable(GL_LIGHTING)
            glLightfv(GL_LIGHT0, GL_POSITION, light_position)
            draw_light_cube(light_position)
        else:
            glDisable(GL_LIGHTING)

        # wygląd piramidy
        for tetrahedron in draw_n_pyramids(n, 0, 0, 0):
            if (colorsOrTex == 1):
                draw_pyramid(tetrahedron, colors1)
            elif (colorsOrTex == 2):
                draw_pyramid(tetrahedron, colors2)
            if (colorsOrTex == 3):
                draw_pyramid(tetrahedron, colors3)
            if (colorsOrTex == 4):
                glColor3f(1.0, 1.0, 1.0)
                glEnable(GL_TEXTURE_2D)
                draw_pyramid_with_texture(tetrahedron)
                glDisable(GL_TEXTURE_2D)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()