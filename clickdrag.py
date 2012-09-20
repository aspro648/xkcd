
'''
Script to grab image tiles from XKCD's "click and drag" web comic at
http://xkcd.com/1110/
- stores original 2048x2048 in results/
- resizes thumbnails in thumbnails/
- creates "composite.png" from thumbnails.
- creates "clickdrag.html" which shows thumbnails and links to originals.

At 300 dpi, this picture would be 16' x 40'.
Zoomable example (not mine) at http://xkcd-map.rent-a-geek.de/

Remarkably similar to
"The Planiverse: Computer Contact with a Two-Dimensional World"
by A.K. Dewdney

Notable tiles:
- 1n48e.png "Wonder where I'll float next". Reference to original comic
  http://xkcd.com/1/
- 9n2e.png "Huston, we have a problem". Apollo 13 reference.
- 5n12e.png "Daisy, Daisy ...". 2001 Space Odesy reference.
- 8n6e.png "Red Five". Star Wars
= 8s17w.png "Copy Gold leader". Another Star Wars.
- 13n1e.png Falling whales. Douglas Adams Reference?


'''

import Image, ImageDraw, ImageFont
import os, sys, urllib

def get(o, targetImg):
    global missing
    
    baseURL = 'http://imgs.xkcd.com/clickdrag'
    found = False
    if os.path.exists('originals/%s' % targetImg) or targetImg in missing:
        if targetImg in missing:
            print targetImg, 'already missing'
        else:
            print targetImg, 'exists'
            found = True
    else:
        try:
            f = o.retrieve('%s/%s' % (baseURL, targetImg),
                           'originals/%s' % targetImg)
            print targetImg, 'success'
            found = True
        except IOError:
            if targetImg not in missing:
                missing.append(targetImg)
            print targetImg, 'missing'
    return found

o = urllib.URLopener({})

# Be nice to xkcd, copy 'missing' list here to avoid 404s on those already
# if you stop and restart the script.
missing = []

maxW = [34, 0] # [search_to, found]
maxE = [50, 0]
maxN = [14, 0]
maxS = [21, 0]

# make directories if not present
if not os.path.isdir('originals'):
    os.mkdir('originals')
if not os.path.isdir('thumbnails'):
    os.mkdir('thumbnails')

 # get the image files
if False:
    for v in range(maxN[0], 0, -1):
        for h in range(maxE[0], 0, -1):
            if get(o, '%sn%se.png' % (v, h)):
                if h > maxE[1]: maxE[1] = h
                if v > maxN[1]: maxN[1] = v
        for h in range(1, maxW[0]):
            if get(o, '%sn%sw.png' % (v, h)):
                if h > maxW[1]: maxW[1] = h                
                if v > maxN[1]: maxN[1] = v
        print 'row=%sN, w=%s, e=%s, n=%s, s=%s' % (v, maxW[1], maxE[1],
                                                   maxN[1], maxS[1])
    for v in range(1, maxS[0]):
        for h in range(maxE[0], 0, -1):
            if get(o, '%ss%se.png' % (v, h)):
                if h > maxE[1]: maxE[1] = h
                if v > maxS[1]: maxS[1] = v
        for h in range(1, maxW[0]):
            if get(o, '%ss%sw.png' % (v, h)):    
                if h > maxW[1]: maxW[1] = h
                if v > maxS[1]: maxS[1] = v
        print 'row=%sS, w=%s, e=%s, n=%s, s=%s' % (v, maxW[1], maxE[1],
                                                   maxN[1], maxS[1])
#row=20S, w=33, e=48, n=13, s=19
maxW = [34, 33] # [search_to, found]
maxE = [50, 48]
maxN = [14, 13]
maxS = [21, 19]

# make blank black and white tiles for missing images
if False:
    im = Image.new('1', (2048, 2048), 0)
    im.save('originals/blank_b.png')
    im = Image.new('1', (2048, 2048), 255)
    im.save('originals/blank_w.png')

# resize the originals to a usable size
tile = 512
if False:
    files = os.listdir(os.path.join(os.getcwd(),'originals'))
    size = (tile, tile)
    for img in files:
        print 'resizing %s' % (img)
        im = Image.open('%s/%s' % ('originals', img))
        im = im.resize(size, Image.ANTIALIAS)
        im.save('%s/%s' % ('thumbnails', img))

# build a composite image                    
if False:
    hor = []
    for h1 in range(maxW[1], 0, -1):
        hor.append('%s%s' % (h1, 'w'))
    for h2 in range(1, maxE[1] + 1):
        hor.append('%s%s' % (h2, 'e'))

    ver = []    
    for v1 in range(maxN[1], 0, -1):
        ver.append('%s%s' % (v1, 'n'))
    for v2 in range(1, maxS[1] + 1):
        ver.append('%s%s' % (v2, 's'))

    im = Image.open('%s/%s' % ('thumbnails', 'blank_w.png'))
    im = im.resize((tile * len(hor), tile * len(ver)))

    for i, h in enumerate(hor):
        for j, v in enumerate(ver):
            target = '%s%s.png' % (v, h)
            print target, 
            if os.path.exists('thumbnails/%s' % target):
                pass
            else:
                if 'n' in target.split('.')[0]:
                    target = 'blank_w.png'
                else:
                    target = 'blank_b.png'
            im2 = Image.open('thumbnails/%s' % target)
            im.paste(im2, (i * tile, j * tile))
            print 'pasting %s at (%s, %s)' % (target, i * tile, j * tile)
    im.save('composite.png')
    print 'composite.png saved'

#build html file
if True:
    f = open('clickdrag.html', 'w')
    f.write('<html>\n<head></head>\n<body>\n')
    size = 25
    f.write('<table border="0" cellpadding="0" cellspacing="0">')
    for v in range(maxN[1], 0, -1):
        f.write('<tr>\n')
        for h in range(maxW[1], 0, -1):
            target = '%sn%sw.png' % (v, h)
            if os.path.exists('thumbnails/%s' % target):
                pass
            else:
                target = 'blank_b.png'
            f.write('<td><a href="originals/%s">' % target)
            f.write('<img src="thumbnails/%s" width="%s">' % (target, size))
            f.write('</a></td>\n')
        for h in range(1, maxE[1] + 1):
            target = '%sn%se.png' % (v, h)
            if os.path.exists('thumbnails/%s' % target):
                pass
            else:
                target = 'blank_b.png'
            f.write('<td><a href="originals/%s">' % target)
            f.write('<img src="thumbnails/%s" width="%s">' % (target, size))
            f.write('</a></td>\n')
    for v in range(1, maxS[1] + 1):
        f.write('<tr>\n')
        for h in range(maxW[1], 0, -1):
            target = '%ss%sw.png' % (v, h)
            if os.path.exists('thumbnails/%s' % target):
                pass
            else:
                target = 'blank_w.png'
            f.write('<td><a href="originals/%s">' % target)
            f.write('<img src="thumbnails/%s" width="%s">' % (target, size))
            f.write('</a></td>\n')
        for h in range(1, maxE[1] + 1):
            target = '%ss%se.png' % (v, h)
            if os.path.exists('thumbnails/%s' % target):
                pass
            else:
                target = 'blank_w.png'
            f.write('<td><a href="originals/%s">' % target)
            f.write('<img src="thumbnails/%s" width="%s">' % (target, size))
            f.write('</a></td>\n')
        f.write('</tr>\n')
    f.write('</table>')
    f.write('</body>\n</html>\n')
    f.close()
    print 'clickdrag.html created'
