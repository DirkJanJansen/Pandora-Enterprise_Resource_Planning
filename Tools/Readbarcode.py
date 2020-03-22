import cv2
from pyzbar.pyzbar import decode
 
 
image = cv2.imread('200000070.png')
 
detectedBarcodes = decode(image)
 
for barcode in detectedBarcodes:
     
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
  
    print(barcode.data)
    print(barcode.type)
 
 
cv2.imshow("Image", image)
  
cv2.waitKey(0)
cv2.destroyAllWindows()
