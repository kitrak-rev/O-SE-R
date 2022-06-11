import cv2
import numpy as np
import yolo_img
import maskbb

def find_endpoints(img):
    height,width =img.shape
    kernel = np.ones((3,3), np.uint8)
    img_erosion = cv2.erode(img, kernel, iterations=1)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=3)
    corners = cv2.goodFeaturesToTrack(img, 7, 0.7, width/8)
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x,y), 7, (255,255,0), -1)
    cv2.imshow('img',img)
#    cv2.imshow('img',img_dilation)
#    cv2.imshow('img',img)
    cv2.waitKey()
    return corners



if __name__ == "__main__":
    (img,boxes,indexes) = yolo_img.yolo_ret()
    mask = maskbb.mask_it(img,boxes,indexes)
    endpoints = find_endpoints(mask)
    print(endpoints)
