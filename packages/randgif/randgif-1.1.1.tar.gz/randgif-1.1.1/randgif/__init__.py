import imageio
from randomimg import create
import random,os
def newgif(w,h,count,fname):
    filenames=[]
    a=0
    def rs(l):
        m=[]
        for i in range(l):
            m.append(chr(random.randrange(67,200)))
        return ''.join(m)
    for i in range(count):
        m=rs(5)
        create(w,h,m+'.jpg')
        filenames.append(m+'.jpg')
        
    with imageio.get_writer(fname, mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
    for f in filenames:
        os.remove(f)
