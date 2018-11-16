import pygame, copy, sys
import numpy as np

######################################################################################################
###################################### Ustawienia początkowe zmiennych################################
######################################################################################################

font_size = 20
font_size_2 = 1.5 * font_size
lw = 2

pygame.init()

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', font_size)

clock = pygame.time.Clock()

unit = 48
font_size = unit/3

width = unit*15
height = unit*14

RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)


######################################################################################################
####################### Wczytanie grafiki i dźwieku ##################################################
######################################################################################################

pipes = (pygame.transform.scale(pygame.image.load("pipe1.png"), (unit, unit)),
         pygame.transform.scale(pygame.image.load("pipe2.png"), (unit, unit)))

pipes2 = (pygame.transform.scale(pygame.image.load("pipe1_2.png"), (unit, unit)),
          pygame.transform.scale(pygame.image.load("pipe2_2.png"), (unit, unit)))

valve = pygame.transform.scale(pygame.image.load("valve.png"), (unit, unit))
valve2 = pygame.transform.scale(pygame.image.load("valve_2.png"), (unit, unit))

outlet = pygame.transform.scale(pygame.image.load("outlet.png"), (unit, unit))
outlet2 = pygame.transform.scale(pygame.image.load("outlet_2.png"), (unit, unit))
outlet3 = pygame.transform.scale(pygame.image.load("outlet_3.png"), (unit, unit))

clangs = (pygame.mixer.Sound('clang1.wav'),
            pygame.mixer.Sound('plate1.wav'))  

VictorySmall = pygame.mixer.Sound('VictorySmall.wav')
VictoryBig =  pygame.mixer.Sound('VictoryBig.wav')
Touch = pygame.mixer.Sound('Touch.wav')

water = 'water.ogg'


######################################################################################################
####################### Deklaracja poziomów ##########################################################
######################################################################################################

AA = [
      [[1,	0,	0,	0,	0],
       [0,	0,	0,	0,	1]],

     [[0,	1,	1,	0],				
      [0,	1,	0,	1]],				
							
     [[1,	0,	1,	0],				
      [1,	0,	0,	1],				
      [0,	1,	0,	1]],				
							
     [[0,	0,	0,	0,	1,	0],		
      [0,	1,	1,	1,	0,	0],		
      [1,	0,	0,	1,	1,	1],		
      [0,	0,	0,	1,	1,	1],		
      [1,	0,	1,	0,	1,	1],		
      [0,	0,	0,	0,	0,	1]],		
							
     [[1,	0,	0,	0,	1,	0],		
      [1,	1,	1,	1,	0,	0],		
      [1,	1,	1,	1,	1,	1],		
      [1,	1,	1,	1,	1,	1],		
      [1,	1,	1,	0,	1,	1],		
      [0,	0,	0,	1,	1,	0]],		
    							
     [[1,	0,	0,	1,	1,	0,	1],	
      [0,	0,	1,	1,	1,	1,	0],	
      [0,	1,	0,	0,	1,	0,	1],	
      [0,	0,	1,	0,	0,	0,	1],	
      [1,	0,	0,	1,	1,	1,	1],	
      [1,	0,	1,	0,	0,	1,	0],	
      [0,	1,	0,	0,	1,	0,	0],	
      [1,	0,	0,	0,	0,	0,	0]],	
       		
      [[1,	0,	1,	1,	1,	0,	1,	1],
       [0,	0,	0,	0,	1,	1,	0,	0],
       [1,	1,	0,	1,	0,	1,	1,	0],
       [0,	0,	0,	0,	1,	0,	0,	0],
       [1,	0,	0,	1,	0,	1,	1,	1],
       [0,	1,	0,	1,	1,	1,	1,	1],
       [0,	0,	1,	1,	0,	0,	0,	0],
       [1,	1,	0,	0,	0,	1,	0,	0],
       [1,	0,	1,	0,	0,	0,	0,	0]],
       
      [[0,	0,	1,	0,	0,	1,	1,	0,	1],
       [0,	0,	0,	0,	1,	0,	0,	1,	0],
       [0,	0,	1,	0,	1,	1,	1,	0,	0],
       [0,	0,	1,	0,	1,	1,	1,	0,	1],
       [1,	0,	1,	0,	0,	0,	1,	0,	0],
       [0,	0,	1,	1,	1,	0,	1,	1,	0],
       [0,	0,	0,	0,	1,	1,	0,	0,	0],
       [0,	1,	0,	0,	0,	0,	0,	0,	0],
       [0,	1,	1,	0,	1,	1,	0,	0,	0],
       [1,	0,	1,	1,	0,	1,	0,	0,	0]],
       
       [[1,	0,	0,	0,	0],
        [1,	1,	1,	1,	1],
        [1,	1,	1,	1,	1],
        [1,	1,	1,	1,	1],
        [1,	1,	1,	1,	1],
        [1,	1,	1,	1,	1],
        [1,	1,	1,	1,	1],
        [1,	1,	1,	1,	1],
        [0,	0,	0,	0,	1]]
      
]

BB = [
     [[0,	1,	2,	1,	2],
      [0,	3,	0,	3,	1]],

     [[1,	0,	0,	3],				
      [2,	1,	0,	2]],				
    							
      [[2,	2,	2,	1],				
      [2,	0,	0,	1],				
      [1,	2,	0,	3]],				
    							
     [[0,	3,	3,	2,	3,	0],		
      [2,	1,	2,	1,	2,	0],		
      [0,	2,	1,	2,	1,	0],		
      [0,	0,	0,	3,	2,	0],		
      [2,	0,	2,	1,	3,	3],		
      [3,	3,	3,	2,	1,	0]],		
        							
     [[1,	2,	0,	0,	0,	2],		
      [2,	1,	2,	1,	1,	1],		
      [2,	0,	1,	3,	0,	2],		
      [0,	2,	1,	3,	0,	0],		
      [1,	3,	3,	3,	2,	1],		
      [1,	3,	2,	0,	1,	1]],		
    							
     [[3,	3,	3,	0,	3,	3,	1],	
      [2,	2,	0,	2,	1,	3,	0],	
      [3,	0,	2,	2,	3,	0,	3],	
      [3,	0,	0,	3,	2,	2,	1],	
      [2,	3,	2,	3,	3,	3,	0],	
      [1,	3,	1,	0,	3,	3,	1],	
      [1,	1,	2,	1,	3,	3,	0],	
      [1,	0,	3,	1,	1,	0,	0]],	
    							
     [[1,	2,	2,	3,	1,	0,	2,	2],
      [2,	3,	2,	1,	3,	0,	0,	0],
      [1,	2,	0,	0,	3,	0,	2,	0],
      [3,	3,	1,	1,	1,	1,	2,	1],
      [2,	3,	1,	1,	1,	0,	3,	1],
      [3,	1,	3,	3,	1,	1,	3,	0],
      [3,	0,	1,	1,	2,	2,	3,	2],
      [3,	3,	1,	0,	2,	3,	1,	3],
      [3,	3,	3,	1,	2,	3,	0,	2]],
       
     [[2,   0,	1,	3,	3,	1,	0,	3,	1],
      [2,	3,	3,	3,	2,	0,	1,	0,	2],
      [2,	1,	1,	3,	0,	3,	1,	3,	2],
      [1,	3,	0,	1,	1,	3,	0,	2,	0],
      [2,	3,	3,	1,	2,	2,	0,	2,	0],
      [1,	0,	0,	2,	3,	3,	1,	1,	1],
      [2,	1,	3,	2,	2,	2,	1,	0,	3],
      [1,	1,	0,	3,	1,	2,	3,	1,	2],
      [2,	0,	3,	3,	3,	3,	2,	3,	0],
      [0,	1,	2,	2,	0,	3,	2,	3,	1]],
      
      [[0,	1,	2,	1,	2],
       [1,	1,	1,	1,	1],
       [1,	1,	1,	1,	1],
       [1,	1,	1,	1,	1],
       [1,	1,	1,	1,	1],
       [1,	1,	1,	1,	1],
       [1,	1,	1,	1,	1],
       [1,	1,	1,	1,	1],
       [0,	3,	0,	3,	1]]

]




######################################################################################################
################################################ GRA #################################################
######################################################################################################


def main_game(nr_gry):

    # Układ rur będę reprezentował jako dwie macierze:
    # Macierz kształtów rur A
    # Macierz orienracji rur B - elementy macierzy b reprezentyją krotność obrotu o 90 stopni względem pozycji wyjściowej
    

    A = AA[nr_gry]
    B = copy.deepcopy(BB[nr_gry])

    m = len(A)
    n = len(A[0])
    
    predkosc = 3*(m*n)**(1/2)  # Prędkosc napelniania się rur 
                               # - proporcjonalna do redniej geometrycznej wymiarów planszy
    predkosc2 = 3

    x_start = width/2 - n * unit/2
    y_start = 2*unit


    
    # Połączenia poszczególnych rur przechowuję w postaci wektorów logiczny.
    # Wartość True oznacza, że rura łączy się w danym kierunku, kolejno w górę, w prawo, w dół, w lewo.
    # Tablica P reprezentuje połączenia w wyjściowej pozycji (obrót 0 stopni)

    P = [[True, True, False, False],
         [False, True, False, True]]


    # Inicjacja planszy

    screen = pygame.display.set_mode((width, height))
    
    screen.blit(myfont.render('Poziom ' + str(nr_gry + 1) + ".", False, GREEN), (width / 2 - font_size_2/4, 0))

    screen.blit(valve, (x_start, y_start - unit))
    screen.blit(outlet, (x_start + (n - 1) * unit, y_start + m * unit))

    for k in range(m):
        for l in range(n):
            pipe = pygame.transform.rotate(pipes[A[k][l]], -90 * B[k][l])
            screen.blit(pipe, (x_start + l * unit, y_start + k * unit))


    done = False
    quit_game = False

    x = x_start
    y = y_start

    i = 0
    j = 0
    
    change = True  # Nie wprowadzać zmiany na ekranie tylko w przypadku faktycznych zmian 
                   # (nie wypisywać wielokrotnie tego samego). Upłynniło to dziłania pętlo.
                   # Pewnie można lepiej/prosciej/inaczej.

    while not (done or quit_game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                pygame.quit()
                sys.exit()                

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_RETURN]: done = True

        if pressed[pygame.K_SPACE]: 
            B[i][j] = (B[i][j] + 1) % 4
            clangs[0].play()
            change = True
            
        if pressed[pygame.K_LCTRL]: 
            B[i][j] = (B[i][j] - 1) % 4
            clangs[1].play()
            change = True

        if pressed[pygame.K_RIGHT]: 
            j = min(j + 1, n - 1)
            Touch.play()
            change = True
        if pressed[pygame.K_LEFT]:  
            j = max(j - 1, 0)
            Touch.play()
            change = True
        if pressed[pygame.K_DOWN]:  
            i = min(i + 1, m - 1)
            Touch.play()
            change = True
        if pressed[pygame.K_UP]:    
            i = max(i - 1, 0)
            Touch.play()
            change = True

        if pressed[pygame.K_ESCAPE]:
            break
        
        if change:  # Skoro niczego nie zmienilimy to po co nanosić modyfikacje?
            
            screen.blit(pipe, (x, y))
            
            x = x_start + j * unit
            y = y_start + i * unit
    
            pipe = pygame.transform.rotate(pipes[A[i][j]], -90*B[i][j])
            screen.blit(pipe, (x, y))
            pygame.draw.lines(screen, GREEN, True, [[x, y], [x+unit-lw, y], [x+unit-lw, y+unit-lw], [x, y+unit-lw]], lw)
            pygame.display.update()

            change = False
            
        clock.tick(7)


#####################################################################################################
################################ Sprawdzenie poprawnosci rozwiązania ################################
#####################################################################################################        


    if done and not quit_game:
        
        screen.blit(pipe, (x, y))
        pygame.display.update()
        
        pygame.mixer.music.load(water)
        pygame.mixer.music.play()
        
        clock.tick(2)

        # Zdefiniujemy funkcje, które pozwolą nam ustalać połączenia rur po ich obrocie,
        def rotate_pipe(p_i):
            return [p_i[3], p_i[0], p_i[1], p_i[2]]


        def rotate_pipe_k(p_i, k):
            for r in range(k):
                p_i = rotate_pipe(p_i)
            return p_i


        D = np.array([  # Możliwe kierunki podróży
            [-1, 0],  # Góra
            [0, 1],  # Prawo
            [1, 0],  # Dół
            [0, -1]])  # Lewo


        direction = np.array([True, False, False, False])  # direction z ktorego dolatuje woda (na poczatku od gory)

        # Test dla pierwszej rury

        a = A[0][0]
        b = B[0][0]

        p = P[a]
        p = rotate_pipe_k(p, b)
        pipe = pygame.transform.rotate(pipes[a], -90 * b)
        
        
        # Zmienne mówiąca o zwycięstwie bądź porażce w grze, chciałbym, aby gra również miała do nich dostęp
        
        global victory
        victory = False
        loss = False

        if not p[0]:
            loss = True

        k = 0
        l = 0
        
        x = x_start + l * unit
        y = y_start + k * unit


        screen.blit(valve2, (x_start, y_start - unit))
        pygame.display.update()


        while not (loss or victory or quit_game):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    pygame.quit()
                    sys.exit()
            
            x = x_start + l * unit
            y = y_start + k * unit

            a = A[k][l]  # kształt k-l-tej rury
            b = B[k][l]  # orientacja k-l-tej rury

            p = P[a]
            p = rotate_pipe_k(p, b)

            pipe = pygame.transform.rotate(pipes2[a], -90 * b)

            screen.blit(pipe, (x, y))
            pygame.display.update()
            

            direction = np.logical_xor(p, direction)  # direction, w którym da się płynąć, inny niż powrótny
            nastepnik = [k, l] + D[direction]
            [k_n, l_n] = [nastepnik[0][0], nastepnik[0][1]]

            direction = np.array(
                rotate_pipe_k(direction, 2))  # direction wyplywania staje sie kierunkiem wplywania dla nastepnika


            if np.any(nastepnik < [0, 0]) | np.any(nastepnik > [m - 1, n - 1]): # Nie chcemy wyjsc poza planszę
                if k == m - 1 and l == n - 1 and p[2]: # Obsługa ostatniego elementu
                    victory = True
                else:
                    loss = True

            else:
                a_n = A[k_n][l_n]  # kształt nastepnika
                b_n = B[k_n][l_n]  # orientacja nastepnika
                p_n = rotate_pipe_k(P[a_n], b_n)

                if ~np.any(direction & p_n):
                    loss = True

            [k, l] = [k_n, l_n]  # Przechodzimy do nastepnika

            pygame.display.update()
            clock.tick(predkosc)
            
        pygame.mixer.music.stop()
        
        if loss and not quit_game:
            for it in range(3):
                screen.blit(pipe, (x, y))
                pygame.display.update()

                clock.tick(2)
                pygame.draw.lines(screen, RED, True,
                                  [[x + lw + 0, y + lw - 0],
                                   [x + unit - lw - 2, y + lw - 0],
                                   [x + unit - lw - 2, y + unit - lw - 2],
                                   [x + lw + 0, y + unit - lw - 2]], 3 * lw)
                pygame.display.update()

                clock.tick(predkosc2)
        elif not quit_game:
            VictorySmall.play()
            for it in range(3):
                screen.blit(outlet2, (x_start + (n - 1) * unit, y_start + m * unit))
                pygame.display.update()
                clock.tick(predkosc2)
                screen.blit(outlet3, (x_start + (n - 1) * unit, y_start + m * unit))
                pygame.display.update()

                clock.tick(predkosc2)




######################################################################################################
################################################ MENU ################################################
######################################################################################################

quit_game = False
lvl = open("lvl.txt", "r")
lvl_numb = int(lvl.read())
lvl.close()

all_lvls = len(AA)

indent = width/5
ind2 = width / 10

def messege(text, y, x = width / 2 - indent):
    screen.blit(myfont.render(text, False, GREEN), (x, y * font_size_2))

def messege1(text, y = 1/3):
    screen = pygame.display.set_mode((width, height))
    screen.blit(myfont.render(text, False, GREEN), 
                (width / 2 - len(text)*font_size/4, height*(y)))
    pygame.display.update()
    clock.tick(2)
    
def messege2(text, y = 1/3):
    screen.blit(myfont.render(text, False, GREEN), 
                (width / 2 - len(text)*font_size/4, height*(y)))
    pygame.display.update()
    clock.tick(2)
    

first_time = True # To będzie znacznik czy jestem w pętli while po raz pierwszy. 
                  # Nie będę wielokrotnie wypisywał tych samych stanów na ekranie. Znacznie upłynniło to prace MUNU.

global victory
victory = False
        
while not quit_game:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
            pygame.quit()
            quit()
    
    if first_time:
        screen = pygame.display.set_mode((width, height))
        messege("Menu:", 1)
        
        second_line = 3
        messege('[1] - Zagraj w grę', second_line)
        messege('[2] - Instrukcja', second_line + 1)
        messege('[Esc] - Wyjście', second_line + 3)
        messege('Naciśnij podany przycisk, aby wybrać opcję', second_line + 6)
        pygame.display.update()

        first_time = False


    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_ESCAPE]:
        quit_game = True
        quit()

    if pressed[pygame.K_2]:
        Touch.play()
        first_time = True
        
        while not quit_game:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    pygame.quit()
                    quit()
            
            if first_time:
                screen = pygame.display.set_mode((width, height))
                messege('Instrukcja', 1, width/2 - 10*font_size/4)
                messege('Zadaniem gracza jest stworzenie z kawałków rur połączenia', 3, ind2)
                messege('pomiędzy zaworem a ujściem.', 4, ind2)
                messege('W tym celu należy obracać poszczególne fragmenty tak długo, ', 5, ind2)
                messege('aż uzyska się nieprzerwany ciąg pomiędzy początkiem a końcem.', 6, ind2)
                messege('Kontrola odbywa się wyłącznie przy pomocy klawiatury.', 7, ind2)
                
                messege('Do zabawy służą następujące klawisze:', 9, ind2)
                messege('Strzałki - przemieszczanie się pomiędzy fragmentami rur', 10, ind2)
                messege('[Spacja] - obrót elementu zgodnie z ruchem wskazówek zegara', 11, ind2)
                messege('[Lewy CTRL] - obrót elementu przeciwnie do ruchu wskazówek zegara', 12, ind2)
                messege('[ENTER] - akceptacja układu i odkręcenie wody', 13, ind2)
                
                messege('Aby odblokować kolejny poziom gracz musi pomyślnie ukończyć bieżący.', 14, ind2)
                messege('Gra automatycznie zapamiętuje postep gry.', 15, ind2)
                
                messege('[Esc] - Powrót', 17, width/2 - 10*font_size/4)
                pygame.display.update()
                first_time = False
            
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_ESCAPE]:
                Touch.play()
                first_time = True
                break
                    

    if pressed[pygame.K_1]:
        Touch.play()
        first_time = True
        while not quit_game:
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                    pygame.quit()
    
            if first_time:
                screen = pygame.display.set_mode((width, height))
                screen.blit(myfont.render('Zagraj w grę:', False, GREEN), (width / 2 - indent, font_size_2))
                screen.blit(myfont.render('[1] - Wybierz poziom', False, GREEN), (width / 2 - indent, 3 * font_size_2))
                screen.blit(myfont.render('[2] - Zrestartuj postęp', False, GREEN), (width / 2 - indent, 4 * font_size_2))
                screen.blit(myfont.render('[3] - Odblokuj wszystkie poziomy', False, GREEN), (width / 2 - indent, 5 * font_size_2))
                screen.blit(myfont.render('      (opcja dla leniuchów)', False, GREEN), (width / 2 - indent, 6 * font_size_2))

                screen.blit(myfont.render('[Esc] - Powrót', False, GREEN), (width / 2 - indent, 8 * font_size_2))
                pygame.display.update()

                first_time = False

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_ESCAPE]:
                Touch.play()
                first_time = True
                break
            
            if pressed[pygame.K_2]:
                Touch.play()
                first_time = True
                lvl_numb = 0
                lvl = open("lvl.txt", "w")
                lvl.write("0")
                lvl.close()
                                                                                            
                messege1("Zrestartowano postęp gry")
                clock.tick(1)
                
        
            if pressed[pygame.K_3]:
                Touch.play()
                first_time = True
                lvl_numb = all_lvls - 1
                lvl = open("lvl.txt", "w")
                lvl.write(str(all_lvls - 1))
                lvl.close()
                
                messege1("Odblokowano wszystkie poziomy")
                clock.tick(1)
                
            
            if pressed[pygame.K_1]:
                Touch.play()
                first_time = True
                while not quit_game:
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit_game = True
                            pygame.quit()
                            quit()
            
                    if first_time: 
                        screen = pygame.display.set_mode((width, height))
                        screen.blit(myfont.render('Wybierz poziom:', False, GREEN), (width / 2 - indent, font_size_2))
                        for lvls in range(lvl_numb + 1):
                            screen.blit(myfont.render("[" + str(lvls+1) + "] - Poziom " + str(lvls+1) + ".",
                                                      False, GREEN), (width / 2 - indent, (lvls + 2) * font_size_2))
                        screen.blit(myfont.render('[Esc] - Powrót', False, GREEN), (width / 2 - indent, (lvl_numb + 4) * font_size_2))
                        pygame.display.update()

                        first_time = False
    
                    pressed = pygame.key.get_pressed()

                    if pressed[pygame.K_ESCAPE]:
                        Touch.play()
                        first_time = True
                        break
                    
                    if pressed[pygame.K_1] or pressed[pygame.K_2] or pressed[pygame.K_3] or \
                        pressed[pygame.K_4] or pressed[pygame.K_5] or pressed[pygame.K_6] or \
                        pressed[pygame.K_7] or pressed[pygame.K_8] or pressed[pygame.K_9]:
                        
                        Touch.play()
                        first_time = True

                        if pressed[pygame.K_1]: nr_gry = 0
                        if pressed[pygame.K_2]: nr_gry = 1
                        if pressed[pygame.K_3]: nr_gry = 2
                        if pressed[pygame.K_4]: nr_gry = 3
                        if pressed[pygame.K_5]: nr_gry = 4
                        if pressed[pygame.K_6]: nr_gry = 5
                        if pressed[pygame.K_7]: nr_gry = 6
                        if pressed[pygame.K_8]: nr_gry = 7
                        if pressed[pygame.K_9]: nr_gry = 8
                        
                        if nr_gry <= lvl_numb:
                            main_game(nr_gry)
                        
                            if victory:
                                lvl_numb = min(lvl_numb + 1, all_lvls - 1)
    
                                lvl = open("lvl.txt", "w")
                                lvl.write(str(lvl_numb))
                                lvl.close()
                                
                                if nr_gry == all_lvls - 1:
    
                                    quit_loop = False
                                    
                                    VictoryBig.play()
                                    while not quit_loop:
                                        
                                        screen = pygame.display.set_mode((width, height))
                                        messege2('Jesteś zwycięzcą!')
                                        clock.tick(1.3)
                                        messege2('Nacinij dowolny przycisk, aby kontynuować!', 2/3)
                                        
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                quit_loop = True
                                                quit()
                                            if event.type == pygame.KEYDOWN:
                                                quit_loop = True
                                        
                                        
        clock.tick(1.3)
                                
    
    

