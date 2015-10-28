import matting, inpainting
import gc
import cv2

def testFunc():
    imname = "frame_samples/IMG_3056.jpg"
    mskname = "_M.".join(imname.split('.'))

    matting.calcMatte(imname, mskname, 1)

def run_inpainting():
    in_dir = "input_frames/"
    out_dir = "frames/"
    maskdir = "masks/"
    name_base = "IMG_"
    name_extension = ".jpg"

    #name_min = 3010
    #name_max = 3358
    name_min = 3126
    name_max = 3158

    names = [(name_base + str(i) + name_extension, name_base + str(i) + "_M" +\
        name_extension) for i in range(name_min, name_max + 1)]

    for name,mskname in names:
        im = cv2.imread(in_dir + name)
        print(str("Read " + in_dir + name))
        msk = cv2.imread(maskdir + mskname, 0)
        print(str("Read " + maskdir + name))
        print(str("Inpainting.........."))
        fixed = inpainting.fromMask(im, msk, 5)
        print(str("Done."))
        cv2.imwrite(out_dir + name, fixed)
        print(str("Wrote to " + out_dir + name))

def run_matting():
    in_dir = "matte_input/"
    out_dir = "mattes/"
    out_mask_dir = "mattes/masks/"
    maskdir = "matte_input/masks/"
    name_base = "IMG_"
    name_extension = ".JPG"

    name_min = 3415
    name_max = 3437

    names = [(name_base + str(i) + name_extension, name_base + str(i) + "_M" +\
        name_extension) for i in range(name_min, name_max + 1)]

    for name,mskname in names:
        print(str("Image " + in_dir + name + " with mask " + maskdir + mskname))
        print(str("Matting.........."))
        fixed = matting.calcMatte(in_dir + name, maskdir + mskname)
        print(str("Done."))
        if fixed is None:
            print(str("Missing something, skipping...."))
            continue
        fixed,outmask,dispmask = fixed
        cv2.imwrite(out_dir + name, fixed)
        print(str("Wrote to " + out_dir + name))
        cv2.imwrite(out_mask_dir + mskname, outmask)
        print(str("Wrote to " + out_mask_dir + mskname))
        cv2.imwrite(out_mask_dir + name, dispmask)
        print(str("Wrote to " + out_mask_dir + name))

def make_video():
    #fourcc = cv2.cv.CV_FOURCC('x','2','6','4') 
    #fourcc = cv2.cv.CV_FOURCC('X','2','6','4') 
    fourcc = cv2.cv.CV_FOURCC('H','2','6','4') 
    #fourcc = cv2.cv.CV_FOURCC('M','P','4','2') 
    #fourcc = cv2.cv.CV_FOURCC('M','P','E','G') 
    #fourcc = cv2.cv.CV_FOURCC('D','I','V','X') 
    #fourcc = cv2.cv.CV_FOURCC('3', 'I', 'V', 'X')
    #fourcc = -1
    fps = 10

    in_dir = "frames/"
    name_base = "IMG_"
    name_extension = ".JPG"
    name_min = 3010
    #name_max = 3358
    name_max = 3250
    names = [in_dir + name_base + str(i) + name_extension \
        for i in range(name_min, name_max + 1)]
    
    im = cv2.imread(names[0])
    print(str(im.shape))
    #height, width = im.shape[:2]
    width, height = (1600, 1080)

    v_out = cv2.VideoWriter("fly_away.mp4", fourcc, 10, (width, height))
    
    for name in names:
        if not v_out.isOpened():
            print("Video not opened.")
            break
        im = cv2.imread(name)
        if im is None:
            print("-->Could not read frame " + name)
            continue
        v_out.write(im)
        del im
        gc.collect()
        print(str("Wrote frame " + name))
    cv2.destroyAllWindows()
    v_out.release()

def make_unedit_video():
    #fourcc = cv2.cv.CV_FOURCC('x','2','6','4') 
    #fourcc = cv2.cv.CV_FOURCC('X','2','6','4') 
    fourcc = cv2.cv.CV_FOURCC('H','2','6','4') 
    #fourcc = cv2.cv.CV_FOURCC('M','P','4','2') 
    #fourcc = cv2.cv.CV_FOURCC('M','P','E','G') 
    #fourcc = cv2.cv.CV_FOURCC('D','I','V','X') 
    #fourcc = cv2.cv.CV_FOURCC('3', 'I', 'V', 'X')
    #fourcc = -1
    fps = 10

    in_dir = "input_frames/"
    name_base = "IMG_"
    name_extension = ".JPG"
    name_min = 3010
    #name_max = 3358
    name_max = 3250
    names = [in_dir + name_base + str(i) + name_extension \
        for i in range(name_min, name_max + 1)]
    
    im = cv2.imread(names[0])
    print(str(im.shape))
    #height, width = im.shape[:2]
    width, height = (1600, 1080)

    v_out = cv2.VideoWriter("fly_away_unedited.mp4", fourcc, 10, (width, height))
    
    for name in names:
        if not v_out.isOpened():
            print("Video not opened.")
            break
        im = cv2.imread(name)
        if im is None:
            print("-->Could not read frame " + name)
            continue
        v_out.write(im)
        del im
        gc.collect()
        print(str("Wrote frame " + name))
    cv2.destroyAllWindows()
    v_out.release()

#run_matting()
make_video()
make_unedit_video()
