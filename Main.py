import pygame
import random

#------------------------------------CLASES-------------------------------------

class Jugador(pygame.sprite.Sprite): #Parametro que almacena datos de imagen y posición rect
    
    #constructor
    def __init__(self): 
        
        #Llamar al metodo de inicialización de la clase padre
        super().__init__()
        
        #Definir propiedades del objeto
        self.imagen = pygame.image.load("assets/nave3.png").convert() #cargando imagen nave
        self.image = pygame.transform.scale(self.imagen,(110,110)) #redimensionando la imagen
        self.image.set_colorkey(negro) #quitando border negro de imagenes por defecto
        self.rect = self.image.get_rect() #creando objeto rect: obteniendo cuadro de sprite (posición y tamaño de la imagen, tiene metodos y atributos propios)
        self.rect.centerx = pantalla[0] // 2 #dando valor a un atributo del objeto rect (centro del objeto)
        self.rect.bottom = pantalla[1] - 10 #dando valor a un atributo del objeto rect
        self.speed_x = 0
        self.speed_y = 0
        self.shield = 100 #vida o salud de la nave
    
    def update(self):
        
        self.speed_x = 0
        self.speed_y = 0
        teclasPresionada = pygame.key.get_pressed() #arreglo de todas las teclas presionadas
        
        if teclasPresionada[pygame.K_LEFT]: #siesque hay un elemento K.LEFT en la lista entonces
            self.speed_x = -5
        if teclasPresionada[pygame.K_RIGHT]:
            self.speed_x = 5
        if teclasPresionada[pygame.K_UP]:
            self.speed_y = -5
        if teclasPresionada[pygame.K_DOWN]:
            self.speed_y = 5
            
        self.rect.x = self.rect.x + self.speed_x #incrementando la posición x para mover a la izquierda o derecha
        self.rect.y = self.rect.y + self.speed_y #incrementando la posición y para mover a arriba o abajo
        
        if self.rect.right > pantalla[0]:
            self.rect.right = pantalla[0]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > pantalla[1]:
            self.rect.bottom = pantalla[1]
    
    def shoot(self): #disparo
        bala = Bala(self.rect.centerx, self.rect.top)
        spritesAll.add(bala)
        spritesBalas.add(bala)
        sonidoLaser.play()
        
 
class Meteoro(pygame.sprite.Sprite): #Parametro que almacena datos de imagen y posición rect
    
    #constructor
    def __init__(self):
        
        #Llamar al metodo de inicialización de la clase padre
        super().__init__()
        self.image = random.choice(imgMeteoros)
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(pantalla[0] - self.rect.width)
        self.rect.y = random.randrange(-140,-100)
        self.speed_x = random.randrange(-5,5)
        self.speed_y = random.randrange(1,10)
    
    def update(self):
        self.rect.y = self.rect.y + self.speed_y
        self.rect.x = self.rect.x + self.speed_x
        
        if self.rect.top > pantalla[1] + 10 or self.rect.left < -100 or self.rect.right > pantalla[0] + 100:
            self.rect.x = random.randrange(pantalla[0] - self.rect.width)
            self.rect.y = random.randrange(-140,-100)
            self.speed_x = random.randrange(-5,5)
            self.speed_y = random.randrange(1,10)
    

class Bala(pygame.sprite.Sprite):
    
    #constructor
    def __init__(self,x,y):
        
        #Llamar al metodo de inicialización de la clase padre
        super().__init__()
        self.imagen = pygame.image.load("assets/laser1.png").convert()
        self.image = pygame.transform.scale(self.imagen,(40,50)) #redimensionando la imagen
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x #centro del objeto
        self.speed_y = -10
    
    def update(self):
        self.rect.y = self.rect.y + self.speed_y
        
        if self.rect.bottom < 0:
            self.kill() #eliminamos todas las instancias de este objeto en cualquier lista


class Explosion(pygame.sprite.Sprite):
    
    #constructor
    def __init__(self,center):
        
        #Llamar al metodo de inicialización de la clase padre
        super().__init__()
        self.image = animacionExplosion[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 #servira para moverse entre todas las imagenes de las explosiones
        self.last_update = pygame.time.get_ticks() #ver en que punto es el relof que esta corriendo a 60
        self.frame_rate = 50 #velocidad de la explosión entre mas grande el numero mas tardar la explosion
    
    def update(self):
        now = pygame.time.get_ticks() #ver en que punto es el relof que esta corriendo a 60
        if now - self.last_update > self.frame_rate: #cada 50 milisengudos pasara por este if
            self.last_update = now #reiniciar el tiempo del atributo last_update (necesario)
            self.frame = self.frame + 1 #incrementaar cada vez que se llame a update
            
            #si ya termine de animar la explosion osea las 8 img entonces eliminalas para que no ocupen mas memoria
            if self.frame == len(animacionExplosion):
                self.kill()
            else:
                #animando la exploción
                center = self.rect.center
                self.image = animacionExplosion[self.frame] #cambiando de imagen
                self.rect = self.image.get_rect() #colocanda la imagen en turno en un rectangulo
                self.rect.center = center #

#-----------------------------------FUNCIONES----------------------------------

def Texto(surface,text,size,x,y):
    font = pygame.font.SysFont("serif",size) #creando texto con pygame
    text_surface = font.render(text, True, blanco) #añadiendo el texto y algunos atributos
    text_rect = text_surface.get_rect() #añadiendo el texto en un rectangulo para tener mejores coordenadas y medidas
    text_rect.midtop = (x,y) #colocando el texto en la posición x,y referente a su centro de arriba
    surface.blit(text_surface,text_rect) #colocando el texto en la ventana en las posiciones del rect


def BarraSalud(surface,x,y,percentage):
    bar_width = 100
    bar_height = 10
    fill = (percentage/100) * bar_width
    border = pygame.Rect(x,y,bar_width,bar_height) #creando rectangulo de borde
    fillP = pygame.Rect(x,y,fill,bar_height) #creando rectangulo de vida
    
    pygame.draw.rect(surface,verde,fillP) #colocando rectangulo en la ventana
    pygame.draw.rect(surface,blanco,border,2) #colocando rectangulo en la ventana
    

def VentanaGameOver():
    ventana.blit(fondoS,(0,0))
    Texto(ventana,"NAVES",65,pantalla[0]//2,pantalla[1]//4)
    Texto(ventana,"Instruciones",27,pantalla[0]//2,pantalla[1]//2)
    Texto(ventana,"Presione una tecla para iniciar",20,pantalla[0]//2,pantalla[1]*3/4)
    pygame.display.flip()
    iniciar = False
    
    while iniciar == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                iniciar = True
                
        reloj.tick(60)

#------------------------------------MAIN--------------------------------------

#definiendo algunas variables
pantalla = [1000,600] # w, h
negro = (0,0,0)
blanco = (255,255,255)
verde = (0,255,0)
game_over = True
fin = False

pygame.init()
pygame.mixer.init() #nos servira para los sonidos
ventana = pygame.display.set_mode((pantalla[0],pantalla[1])) #creando ventana
pygame.display.set_caption("Juego Naves")
reloj = pygame.time.Clock() #creando reloj del juego


#Cargar imagen de fondo
fondo = pygame.image.load("assets/fondo.jpg").convert()
fondoS = pygame.transform.scale(fondo,(pantalla[0],pantalla[1]))


#Cargar lista de todos los tipos de meteoros
imgMeteoros = []
listaMeteoros = ["assets/meteorGrey_big1.png","assets/meteorGrey_big2.png","assets/meteorGrey_big3.png",
                 "assets/meteorGrey_big4.png","assets/meteorGrey_med1.png","assets/meteorGrey_med2.png",
                 "assets/meteorGrey_small1.png","assets/meteorGrey_small2.png","assets/meteorGrey_tiny1.png",
                 "assets/meteorGrey_tiny2.png"]

for img in listaMeteoros:
    imgMeteoros.append(pygame.image.load(img).convert())

#Cargar explosión imagenes
animacionExplosion = []
for i in range(8): #tomando todas las imagenes de la explosion
    file = "assets/regularExplosion0{}.png".format(i) #reemplazando el valor de los parentesis por el de i
    img = pygame.image.load(file).convert()
    img.set_colorkey(negro)
    img_scale = pygame.transform.scale(img,(70,70))
    animacionExplosion.append(img_scale)

#Cargar sonidos
sonidoLaser = pygame.mixer.Sound("assets/laser5.ogg")
sonidoExplosion = pygame.mixer.Sound("assets/explosion.wav")

pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.4) #controlando el nivel del volumen de la musica

pygame.mixer.music.play(loops=-1) #reproducir la musica infinitamente

#--------------------------------BUCLE INFINITO--------------------------------

while not fin:
    
    if game_over == True:
        
        VentanaGameOver()
        
        game_over = False
        
        #creando un grupo de sprites para todos los obtejos
        spritesAll = pygame.sprite.Group()
        
        #creando un grupo de sprites para los meteoros
        spritesMeteoros = pygame.sprite.Group()
        
        #creando un gruop de sprites para las balas
        spritesBalas = pygame.sprite.Group()
        
        #creando un objeto jugador
        jugador = Jugador() 
        
        #añadir clase jugador al conjunto de sprites
        spritesAll.add(jugador) 
        
        #crear y añadir clase meteoro al conjunto de spritesAll y spritesMeteoros
        for i in range(8):
            meteoro = Meteoro()
            spritesAll.add(meteoro)
            spritesMeteoros.add(meteoro)
        
        puntaje = 0
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fin = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.shoot()
    
    #Llama e invoca a todos los metodos update de todas las clases en el grupo de sprites
    spritesAll.update()
    
    #colisiones - meteoros - balas
    listaColisiones = pygame.sprite.groupcollide(spritesMeteoros,spritesBalas,True,True) #metodo especial que detecta coliones entre dos grupos de sprites y borra ambos por el true , true
    for colision in listaColisiones:
        puntaje = puntaje + 10
        explosion = Explosion(colision.rect.center)
        meteoro = Meteoro()
        spritesAll.add(meteoro)
        spritesMeteoros.add(meteoro)
        spritesAll.add(explosion)
        
        sonidoExplosion.play()
    
    #colisiones - jugador - meteoros
    listaColisiones2 = pygame.sprite.spritecollide(jugador,spritesMeteoros,True) #metodo especial para detectar colisiones, cualquier meteoro que le choque a la nave se agregara en la lista y se borrara el obtejoq que choco
    
    for colision in listaColisiones2: #siques hay algun elemento en la lista entonces
        jugador.shield = jugador.shield - 25
        meteoro = Meteoro()
        spritesAll.add(meteoro)
        spritesMeteoros.add(meteoro)
        if jugador.shield <= 0:
            game_over = True
    
    #colocando la imagen de fondo a la ventana desde la posición 0,0
    ventana.blit(fondoS,[0,0])
    
    #dibujando todos los elementos sprite que esten en el grupo en la ventana
    spritesAll.draw(ventana) 
    
    #marcador
    Texto(ventana,str(puntaje),25,pantalla[0] // 2, 10)
    
    #Escudo o barra de salud
    BarraSalud(ventana,5,5,jugador.shield)
    
    pygame.display.flip()
    reloj.tick(60)
    
pygame.quit()












