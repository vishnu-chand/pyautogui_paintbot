import cv2
import time
import argparse
from glob import glob
import pyautogui as ui


def paintImg(impath, sw, sh):
    img = cv2.imread(impath,0) # read as gray img
    w = int(256 * img.shape[0] / img.shape[1])
    img = cv2.resize(img, (256, w))
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) # binarize image
    cnts,_ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS) # find contours
    cnts =  [[(x + sw, y + sh) for [[x, y]] in cnt[::5]] for cnt in cnts]
    for cnt in cnts:
        if len(cnt) > 5:
            print('draw from %s to %s' % (cnt[0], cnt[1]))
            x, y = cnt[0]
            ui.moveTo(x, y, .3) # move cursor
            for x, y in cnt:
                ui.dragTo(x, y)
                # time.sleep(np.random.randint(100)/500)
    return sw + w + 50, sh


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--imgPath", type=str, default="*.png", help="regex path to a image location eg: *.png")
    parser.add_argument("--shiftWidth", type=int, default=100, help="To draw at center of screen, shift the co-ordinates.")
    parser.add_argument("--shiftHeight", type=int, default=200, help="To draw at center of screen, shift the co-ordinates.")
    args = parser.parse_args()

    shiftBy = args.shiftWidth, args.shiftHeight
    print("make sure paint application is the front and active win")
    time.sleep(5) # will till switching to paint application
    for impath in glob(args.imgPath):
        print('---------------', impath,'---------------')
        shiftBy = paintImg(impath, *shiftBy)
