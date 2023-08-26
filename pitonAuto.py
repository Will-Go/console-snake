# # Importing the keyboard module
import keyboard as kb
import os
import time
import threading
import random
from color import Colors


def clear_console():
    if os.name == "nt":  # windows:
        os.system("cls")
    else:
        os.system("clear")


def mostrar():
    for i in space:
        print("\t\t", end="")
        for j in i:
            print(j, end="")
        print()


def crear_space(ancho, alto):
    return [[' ' for _ in range(ancho)] for _ in range(alto)]


def paredes():
    for i in range(alto):
        space[i][0] = '|'
        space[i][ancho-1] = '|'

    for i in range(ancho):
        space[0][i] = '~'
        space[alto-1][i] = '~'


def mover_snake(X, Y):
    snake.insert(0, (X, Y))
    snake.pop()


def crecer_snake(x, y):
    snake.append((x, y))


def poner_manzana():
    while True:
        numX = random.randint(0, ancho-1)
        numY = random.randint(0, alto-1)
        if (numX, numY) not in snake and numX not in (0, ancho-1) and numY not in (0, alto-1):
            space[numY][numX] = Colors.RED+"$"+Colors.RESET
            return numX, numY


def mostrar_key(e):
    global teclado
    teclado = e.name


def update_screen():
    global x, y, space, snake, alto, ancho, manzanaExiste, manzanaX, manzanaY, estaViva, stop_threads, gano, puntaje, sigue, banner, teclado
    global derecha, izquierda, abajo, arriba

    if not gano:
        # CONDICIONES PARA QUE SE MUERA LA SERPIENTE
        if y in (alto-1, 0) or x in (ancho-1, 0) or (x, y) in snake:
            estaViva = False

        # CONDICION PARA GANAR
        if puntaje+2 == (ancho-2)*(alto-2):
            gano = True

        space = crear_space(ancho, alto)

        # INGRESA LOS PAREDES AL ESPACIO
        paredes()

        # PONER MANZANA [SI LA MANZANA YA EXISTE SIGUE PONIENDO LA MANZANA EN LA POSCION]
        # SI GANA YA NO TIENE QUE PONER MAS MANZANAS
        if not gano:
            if not manzanaExiste:
                manzanaX, manzanaY = poner_manzana()
                manzanaExiste = True
            else:
                space[manzanaY][manzanaX] = Colors.RED+"$"+Colors.RESET

        # MOVER LA SERPIENTE
        mover_snake(x, y)

        # IMPRIME 'X' SI ESTA MUERTO
        for i in snake:
            space[i[1]][i[0]] = Colors.GREEN+"o"+Colors.RESET
        if estaViva:
            space[snake[0][1]][snake[0][0]] = Colors.GREEN+"@"+Colors.RESET
        else:
            space[snake[0][1]][snake[0][0]] = Colors.RED + "X" + Colors.RESET

        # DETECTAR LA MANZANA Y LA CABEZA
        if snake[0] == (manzanaX, manzanaY):
            space[snake[0][1]][snake[0][0]] = Colors.GREEN+"C"+Colors.RESET
            crecer_snake(x, y)
            puntaje += 1
            manzanaExiste = False

        if not estaViva:
            banner = Colors.BLUE+bannerPerder + Colors.RESET
    else:
        # ESTO ES CUANDO GANA
        banner = Colors.BLUE+bannerGanar + Colors.RESET
        space = crear_space(ancho, alto)
        for i in snake:
            space[i[1]][i[0]] = Colors.RED+"o"+Colors.RESET
        space[snake[0][1]][snake[0][0]] = Colors.RED+"@"+Colors.RESET
        if len(snake) != 1:
            snake.pop()
        else:
            stop_threads = True
            sigue = False
        time.sleep(0.25)

    clear_console()
    kb.on_press(mostrar_key)
    print(banner)
    mostrar()
    print("Head = x:", x, "y: ", y)
    print("Score:", puntaje)
    print("Keyboard:", teclado)
    print("Snake:", snake)

    if not gano:
        time.sleep(0.5)

    if derecha:
        x += 1
    if izquierda:
        x -= 1
    if abajo:
        y += 1
    if arriba:
        y -= 1


def comenzar():
    while not stop_threads:
        update_screen()
    if not estaViva:
        print("YOU LOSE!")
    elif gano:
        print("YOU WIN!!")
    print("END!")


bannerPerder = """
 **    **   *******   **     **       **         *******    ******** ********
//**  **   **/////** /**    /**      /**        **/////**  **////// /**///// 
 //****   **     //**/**    /**      /**       **     //**/**       /**      
  //**   /**      /**/**    /**      /**      /**      /**/*********/******* 
   /**   /**      /**/**    /**      /**      /**      /**////////**/**////  
   /**   //**     ** /**    /**      /**      //**     **        /**/**      
   /**    //*******  //*******       /******** //*******   ******** /********
   //      ///////    ///////        ////////   ///////   ////////  //////// 
"""


bannerGanar = """
 **    **   *******   **     **       **       ** ** ****     **
//**  **   **/////** /**    /**      /**      /**/**/**/**   /**
 //****   **     //**/**    /**      /**   *  /**/**/**//**  /**
  //**   /**      /**/**    /**      /**  *** /**/**/** //** /**
   /**   /**      /**/**    /**      /** **/**/**/**/**  //**/**
   /**   //**     ** /**    /**      /**** //****/**/**   //****
   /**    //*******  //*******       /**/   ///**/**/**    //***
   //      ///////    ///////        //       // // //      ///    
"""

bannerSnake = Colors.BLUE + """
  ******** ****     **     **     **   ** ********
 **////// /**/**   /**    ****   /**  ** /**///// 
/**       /**//**  /**   **//**  /** **  /**      
/*********/** //** /**  **  //** /****   /******* 
////////**/**  //**/** **********/**/**  /**////  
       /**/**   //****/**//////**/**//** /**      
 ******** /**    //***/**     /**/** //**/********
////////  //      /// //      // //   // ////////  

""" + Colors.RESET

banner = ""


def main():
    global x, y, space, snake, alto, ancho, manzanaExiste, manzanaX, manzanaY, estaViva, stop_threads, gano, puntaje, sigue, banner, teclado
    global derecha, izquierda, abajo, arriba
    print("\t[\tEnter the dimensions of the grid\t]")
    while True:
        ancho = int(input("Write the width: "))+2
        alto = int(input("Write the height: "))+2

        if ancho > 3 and alto > 3:
            break
        else:
            print(Colors.RED + "\tERROR: Enter a value greater than 1" + Colors.RESET)

    estaViva = True
    gano = False
    stop_threads = False
    manzanaExiste = False
    derecha, izquierda, abajo, arriba = True, False, False, False
    sigue = True
    banner = bannerSnake

    puntaje = 0
    x, y = 1, 1
    snake = [(0, 0), (0, 0)]
    space = crear_space(ancho, alto)
    teclado = ""

    thread = threading.Thread(target=comenzar)
    thread.start()

    try:
        while sigue:
            if kb.is_pressed("right"):
                derecha, izquierda, abajo, arriba = True, False, False, False

            if kb.is_pressed("left"):
                derecha, izquierda, abajo, arriba = False, True, False, False

            if kb.is_pressed("down"):
                derecha, izquierda, abajo, arriba = False, False, True, False

            if kb.is_pressed("up"):
                derecha, izquierda, abajo, arriba = False, False, False, True

            if kb.is_pressed("esc"):
                stop_threads = True
                break

            if not estaViva:
                stop_threads = True
                break

    except KeyboardInterrupt:
        stop_threads = True

    thread.join()


if __name__ == "__main__":

    print(Colors.GREEN + """
                        __
            _______    /*_>-<
        ___/ _____ \__/ /
       <____/     \____/
        """ + Colors.RESET)
    print(Colors.CYAN + "Welcome to Snake Console" + Colors.RESET)
    print(Colors.CYAN + "Author: Wil-Go" + Colors.RESET)
    iniciado = True
    while iniciado:
        main()
        while True:
            try:
                print(Colors.CYAN +
                      "Press 'esc' to exit or 'space' to restart"+Colors.RESET)
                event = kb.read_event()

                if event.name == 'esc':
                    iniciado = False
                    break
                elif event.name == 'space':
                    clear_console()
                    print("Lets start again!")
                    break
                else:
                    print("Press a valid input!!")
            except KeyboardInterrupt:
                iniciado = False
                break

print("bye")
time.sleep(1)
