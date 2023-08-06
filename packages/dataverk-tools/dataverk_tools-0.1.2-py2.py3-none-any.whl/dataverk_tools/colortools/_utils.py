
import colorlover as cl

def hex_to_RGB(hex):
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def hex_to_rgb_cl(hex):
  a = [int(hex[i:i+2], 16) for i in range(1,6,2)]
  return f'({a[0]},{a[1]},{a[2]})'

def RGB_to_hex(RGB):
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def cl_to_hex(s):
  s = s[s.find("(")+1:s.find(")")].replace(' ','').split(',')
  rgb = [int(x) for x in s]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in rgb])


def createTabeleauPalette(colors, name='name', type='regular'):
    xml = '<color-palette name="' + name + '" type="' + type + '">\n'
    for color in colors:
        xml += '<color>' + cl_to_hex(color) + '</color>\n'
    xml += '</color-palette>'
    return xml


def linear_gradient(s, f='rgb(255,255,255)', n=10):
  liste = [s]
  s = s[s.find("(")+1:s.find(")")].replace(' ','').split(',')
  f = f[f.find("(")+1:f.find(")")].replace(' ','').split(',') 
  s = [int(x) for x in s]
  f = [int(x) for x in f]
  resliste = []
  for t in range(1, n):
    res = 'rgb('
    for j in range(2):
        res += str(int(s[j] + (float(t)/(n-1))*(f[j]-s[j]) )) + ','
    res += str(int(s[2] + (float(t)/(n-1))*(f[2]-s[2]))) + ')'    
    resliste .append(res)

  return resliste 


def saturation(s, n=50): 
  s = cl.to_hsl([s])[0] 
  liste = [s]
  s = s[s.find("(")+1:s.find(")")].replace(' ','').replace('%','').split(',')
  s = [int(x) for x in s]
  s0 = s[2]
  for t in range(1, n+1):
       s[2] = s0 + t * ((100-s0)/n)
       res = 'hsl(' + str(int(s[0])) + ',' +  str(int(s[1])) + '%,' + str(int(s[2])) + '%)'      
       liste.append(res)

  return cl.to_rgb(liste)


def lightness(s, n=5): 
  s = cl.to_hsl([s])[0] 
  liste = []
  s = s[s.find("(")+1:s.find(")")].replace(' ','').replace('%','').split(',')
  s = [int(x) for x in s]
  res = 'hsl(' + str(int(s[0])) + ',0%,' + str(int(s[2])) + '%)'      
  liste.append(res)
  for t in range(1, n+1):
       s[1] = t * ((100)/n)
       res = 'hsl(' + str(int(s[0])) + ',' +  str(int(s[1])) + '%,' + str(int(s[2])) + '%)'      
       liste.append(res)

  return cl.to_rgb(liste)