import sdl2
import sdl2.ext
import sdl2.mouse
import ctypes


def get_mouse_position():
    mx, my = ctypes.c_int(0), ctypes.c_int(0)
    sdl2.mouse.SDL_GetMouseState(ctypes.byref(mx), ctypes.byref(my))
    return mx.value, my.value
