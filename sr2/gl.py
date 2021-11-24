import struct

# ===============================================================
# Utilities
# ===============================================================

def char(c):
  """
  Input: requires a size 1 string
  Output: 1 byte of the ascii encoded char 
  """
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  """
  Input: requires a number such that (-0x7fff - 1) <= number <= 0x7fff
         ie. (-32768, 32767)
  Output: 2 bytes
  Example:  
  >>> struct.pack('=h', 1)
  b'\x01\x00'
  """
  return struct.pack('=h', w)

def dword(d):
  """
  Input: requires a number such that -2147483648 <= number <= 2147483647
  Output: 4 bytes
  Example:
  >>> struct.pack('=l', 1)
  b'\x01\x00\x00\x00'
  """
  return struct.pack('=l', d)

def color(r, g, b):
  """
  Input: each parameter must be a number such that 0 <= number <= 255
         each number represents a color in rgb 
  Output: 3 bytes
  Example:
  >>> bytes([0, 0, 255])
  b'\x00\x00\xff'
  """
  return bytes([b, g, r])


# ===============================================================
# Constants
# ===============================================================

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

class Render(object):
    def __init__(self, filename, width, height):
        self.width = 0
        self.height = 0
        self.pixels = []
        self.current_color = BLACK
        self.filename = filename
        self.x_position = 0
        self.y_position = 0
        self.ViewPort_height = 0
        self.ViewPort_width = 0
        self.clear()

    def clear(self):
        self.pixels = [
            [self.current_color for x in range(self.width)]
            for y in range(self.height)
        ]
    

    def write(self,filename):
        f = open(self.filename,'bw')
        
        
         # File header (14 bytes)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Image header (40 bytes)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Pixel data (width x height x 3 pixels)
        for x in range(self.height):
          for y in range(self.width):
            f.write(self.pixels[x][y])

        f.close()

  
    def set_color(self, color):
        self.current_color = color
    
    
    def glColor(self, red, green, blue):
        self.current_color = color(int(round(red*255)),int(round(green*255)),int(round(blue*255)))

    
    def glpoint(self, x, y, color = None):
        self.pixels[y][x] = self.current_color

    
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    
    def glViewPort(self, x_position, y_position,  ViewPort_width, ViewPort_height):
        self.x_position = x_position
        self.y_position = y_position
        self.ViewPort_height = ViewPort_height
        self.ViewPort_width = ViewPort_width
    
    
    def glVertex(self, x, y):
        x_temp  = round((x + 1) * (self.ViewPort_width/ 2) + self.x_position)
        y_temp  = round((y + 1) * (self.ViewPort_height/2) + self.y_position)
        self.glpoint(round(x_temp ), round(y_temp ))
        
    def glFinish(self):
            self.write('Line.bmp')

    def glLine(self, x1, y1, x2, y2):
        x1 = round((x1 + 1) * (self.ViewPort_width * 0.5) + self.x_position)
        y1 = round((y1 + 1) * (self.ViewPort_height * 0.5) + self.y_position)
        x2 = round((x2 + 1) * (self.ViewPort_width * 0.5) + self.x_position)
        y2 = round((y2 + 1) * (self.ViewPort_height * 0.5) + self.y_position)
        
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        steep = dy > dx
        
        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        
        offset = 0
        threshold = dx
        
        
        y = y1
        for x in range(x1, x2 + 1):
            if steep:
                self.glpoint(y, x)
            else:
                self.glpoint(x, y)
                
            offset += dy * 2
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += 2 * dx

r = Render('Line.bmp', 200, 200)
r.glCreateWindow(100,100)
r.glViewPort(25, 25, 50 ,50)
r.clear()
r.glColor(0,1,1)
r.glVertex(0,0) 
r.glLine(-1, -1, 1, -1)
r.glLine(-0.5, -0.5, 0.5, -0.5)
r.glLine(-1, -1, 0, -0)
r.glLine(-0, -0, 1, -1)
r.glLine(-1, -0, 1, -0)
r.glFinish()