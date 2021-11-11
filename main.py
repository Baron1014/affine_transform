import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def main():
    img = cv2.imread("data/women.jpg")
    print(img.shape)

    print("Click on the screen and press any key for end process")
    points = get_points(img)
    print(points)

    # get transform
    origin_points = np.float32(points)
    trans_points = np.float32([[65, 90], [95, 90], [80, 120]])
    M = cv2.getAffineTransform(origin_points, trans_points)
    print(f"M = {M[:2].round(1)}")
    #res = cv2.warpAffine(img, M, (160, 190))
    #api = Image.fromarray(np.uint8(res))
    #api.save("data/api.png")

    # generate new img
    new_img = np.zeros((160, 190, 3))
    for i in range(new_img.shape[0]):
        for j in range(new_img.shape[1]):
            new_pixel = np.float32([i,j,1]).reshape(-1,1)
            original_pixel=np.dot(M, new_pixel)
            
            #將數值四捨五入及將負數改為0
            #original_pixel = np.around(original_pixel, decimals=-1)
            original_pixel = np.where(original_pixel>0, original_pixel, 0)

            # 對應回原始圖片pixel
            new_img[i,j] = img[int(original_pixel[0]), int(original_pixel[1])]

    new = Image.fromarray(np.uint8(new_img))
    new.save("data/affine_women.png")


def mouse_handler(event, x, y, flags, data):
    if event == cv2.EVENT_LBUTTONDOWN:
        # 標記點位置
        cv2.circle(data['img'], (x,y), 3, (0,0,255), 5, 16)

        #改變顯示內容
        cv2.imshow("Image", data['img'])

        # 顯示(x,y)並儲存到list中
        print(f"get point: [x,y] = [{x}, {y}]")
        data["points"].append([x,y])

def get_points(img):
    data = dict()
    data['img'] = img.copy()
    data['points'] = list()

    # 建立一個window
    cv2.namedWindow("Image", 0)

    # 改變Window為適當大小
    h, w, dim = img.shape
    print(f"Img height, width:({h}, {w})")
    cv2.resizeWindow('Image', w, h)

    # 顯示圖片至window
    cv2.imshow("Image", img)

    # 利用滑鼠回傳值，資料皆保存於data dict中
    cv2.setMouseCallback("Image", mouse_handler, data)

    # 按下任意鍵釋放opencv資源
    cv2.waitKey()
    cv2.destroyAllWindows()

    return data['points']

if __name__ == "__main__":
    main()
