import numpy, cv2

#def maskReformat(mask):

def fromMask(img, mask, radius=50, intype=cv2.INPAINT_NS):
    return cv2.inpaint(img, mask, radius, intype)
