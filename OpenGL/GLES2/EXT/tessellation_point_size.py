'''OpenGL extension EXT.tessellation_point_size

This module customises the behaviour of the 
OpenGL.raw.GLES2.EXT.tessellation_point_size to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/tessellation_point_size.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.EXT.tessellation_point_size import *
from OpenGL.raw.GLES2.EXT.tessellation_point_size import _EXTENSION_NAME

def glInitTessellationPointSizeEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION