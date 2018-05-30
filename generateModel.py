import cv2
import tools.generate_model_tools as tools


def init_image_model():
    tools.init_image_model()


# 上传的模型文件可能有很大的一段区域是背景，用识别人脸之后对人脸区域进行剪裁
# 并保存到模型库文件夹中
def corp_image_to_face(frame):
    if (isinstance(frame, str)):  # 容错，可能传入的是图片的路径，当传人的字符串的时候，尝试进行一次加载
        frame = cv2.imread(frame)
    frame = tools.compress_frame(frame)  # 上传的图片的尺寸可能会非常大，对传入的尺寸进行限制，以降低压力
    face_locations, _ = tools.detect_face(frame)  # 检测人脸
    if (len(face_locations) > 1):
        print("上传了多长脸")
        return "不能有多张脸"
    for (top, right, bottom, left) in face_locations:
        left, top, right, bottom = tools.extend_face_size(frame, left, top, right,
                                                          bottom)  # 检测人脸的区域可能比较小，对整个区域进行扩大，让头部都被包裹在剪裁范围内
        left, top, right, bottom = tools.fix_size(frame, left, top, right, bottom)  # 由于扩充的区域可能会冲过图片面积，在此对整个区域的范围大小进行修正
        print((left, top), (right, bottom))
        frame = frame[top:bottom, left:right]  # 剪裁图片
        return frame


def compare_image(filename):
    frame = cv2.imread(filename)
    frame = tools.compress_frame(frame)  # 尺寸压缩
    face_locations, face_encodings = tools.detect_face(frame)  # 查找待检测的图片中的所有人脸
    frame = tools.draw_face_rectangle(frame, face_locations, face_encodings)  # 对找到的所有人脸进行人名比对,并画框显示在图片上
    save_file_name, static_file_name = tools.save_file(frame)
    print(save_file_name)
    print(static_file_name)
    return save_file_name, static_file_name, frame  # 返回结果图片，结果图片的地址


if __name__ == "__main__":
    compare_image("/Users/sunkai/Desktop/20180526_001506.jpg")
