import ctypes
from sdl2 import *

SDL_Init(SDL_INIT_VIDEO)
window = SDL_CreateWindow(b"Hello World",
                          SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                          592, 460, SDL_WINDOW_SHOWN)
windowsurface = SDL_GetWindowSurface(window)

image = SDL_LoadBMP(b"st-anthony-404.bmp")
SDL_BlitSurface(image, None, windowsurface, None)

SDL_UpdateWindowSurface(window)
SDL_FreeSurface(image)

running = True
event = SDL_Event()
while running:
    while SDL_PollEvent(ctypes.byref(event)) != 0:
        if event.type == SDL_QUIT:
            running = False
            break

SDL_DestroyWindow(window)
SDL_Quit()
