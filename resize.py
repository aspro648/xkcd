# Use Python Image Library (PIL) to crop and annotate an image.

import Image, ImageDraw, ImageFont
import os, sys

''' At 300 dpi, this picture would be 16' x 40'
click-zoom at http://xkcd-map.rent-a-geek.de/
The Planiverse: Computer Contact with a Two-Dimensional World
by A.K. Dewdney
'''


if False:
    files = os.listdir(os.path.join(os.getcwd(),'originals'))
    print files
    size = 512, 512

    for img in files:
        print '%s/%s' % ('originals', img)
        im = Image.open('%s/%s' % ('originals', img))
        im = im.resize(size, Image.ANTIALIAS)
        im.save('%s/%s' % ('thumbs', img))
                    
if True:
    hor = []
    for h1 in range(33, 0, -1):
        hor.append('%s%s' % (h1, 'w'))
    for h2 in range(1, 49):
        hor.append('%s%s' % (h2, 'e'))

    ver = []    
    for v1 in range(13, 0, -1):
        ver.append('%s%s' % (v1, 'n'))
    for v2 in range(1, 20):
        ver.append('%s%s' % (v2, 's'))

    tile = 512
    im = Image.open('%s/%s' % ('thumbs', 'blank_w.png'))
    im = im.resize((tile * len(hor), tile * len(ver)))


    for i, h in enumerate(hor):
        for j, v in enumerate(ver):
            target = '%s%s.png' % (v, h)
            print target, 
            if os.path.exists('thumbs/%s' % target):
                pass
            else:
                if 'n' in target.split('.')[0]:
                    target = 'blank_w.png'
                else:
                    target = 'blank_b.png'
            im2 = Image.open('thumbs/%s' % target)
            im.paste(im2, (i * tile, j * tile))
            print 'pasting %s at (%s, %s)' % (target, i * tile, j * tile)
    im.save('combined.png')
    
print 'done'

    
        
