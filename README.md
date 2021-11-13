# Affine Transform
影像處理與機器人視覺

## 程式碼說明
### 讀取影像
```
img = cv2.imread(img_path)
```
### 取得定位點
```
points = get_points(img)
origin_points = np.float32(points)
```
### 設定轉換後的模板定位點
```
trans_points = np.float32([[65, 90, 1], [95, 90, 1], [80, 120, 1]])
```
### 計算Affine Transform
```
a = np.dot(f,g.T)
b = inv(np.dot(g, g.T))
M = np.dot(a,b) 
```
### 按照給定template生成新影像
```
new_img = np.zeros((190, 160, 3))
for i in range(new_img.shape[0]):
    for j in range(new_img.shape[1]):
        new_pixel = np.float32([j, i, 1]).reshape(-1,1)
        original_pixel=np.dot(M, new_pixel)

        # 將將負數改為0
        original_pixel = np.where(original_pixel>0, original_pixel, 0)

        # 對應回原始圖片pixel
        new_img[i, j] = img[int(original_pixel[1]), int(original_pixel[0])]
```
### 儲存影像
```
cv2.imwrite(save_path, new_img)
```

## Result
- 原始影像/處理後影像


<p float="left">
     <img src="data/women.jpg" width="500" /> <img src="data/affine_women.png"/>
     <img src="data/man.jpg" width="500" /> <img src="data/affine_man.png"/>
     <img src="data/both.bmp" width="500" /> <img src="data/affine_both_man.png"/> <img src="data/affine_both_women.png"/>
</p>
