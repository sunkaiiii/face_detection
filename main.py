import generateModel
import cv2
frame=generateModel.compare_image("/Users/sunkai/Desktop/20180526_001506.jpg")
cv2.imshow("result",frame)
cv2.waitKey(0)
cv2.destroyAllWindows()