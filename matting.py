import numpy, cv2
from matplotlib import pyplot as plt

def imToLogical(img):
    if img is None:
        return None
    newimg = numpy.zeros(img.shape[:2], numpy.uint8)
    newimg.fill(cv2.GC_PR_FGD)
    newimg[img == 0] = 0
    newimg[img == 255] = 1
    #return [1 if i == 255 else i for row in img for i in row]
    return newimg

def calcMatte(imname, mskname, iters = 5):
    """ Grabcut matting function which utilizes an input mask image """
    img = cv2.imread(imname)
    if img is None:
        print("Image not found.")
        return None
    rect = (0,0) + tuple(img.shape[:2])
    mask = imToLogical(cv2.imread(mskname, 0))
    if mask is None:
        print("Mask not found.")
        return None

    fgdModel = numpy.zeros((1,65), numpy.float64)
    bgdModel = numpy.zeros((1,65), numpy.float64)

    # why do you seem to need to use both init_with_mask and init_with_rect to get a result?
    res = cv2.grabCut(img, mask, rect, fgdModel, bgdModel, iters, cv2.GC_INIT_WITH_MASK)
    print(str(res))

    mask2 = numpy.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img2 = img*mask2[:,:,numpy.newaxis]

    #plt.imshow(img2),plt.colorbar(),plt.show()
    print("Returning img")
    return (img2, mask2, mask2 * 255)
