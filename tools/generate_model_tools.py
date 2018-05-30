import cv2
import os
import time
import face_recognition

path = os.path.join("img", "face_recognition")  # 模型数据图片目录
save_path = os.path.join("img", "test_result")
extend_width = 100
max_width = 700

total_image_name = []
total_face_encoding = []


def init_image_model():
    for fn in os.listdir(path):  # fn 表示的是读取模型文件夹下各个文件的文件名
        file_extend_name = os.path.splitext(os.path.join(os.getcwd(), path, fn))[1]
        if file_extend_name != ".png" and file_extend_name != ".jpg" and file_extend_name != ".jpeg":
            continue  # 跳过非图片文件
        print(path + "/" + fn)
        total_face_encoding.append(
            face_recognition.face_encodings(
                face_recognition.load_image_file(os.path.join(path, fn)))[0])  # 调用库函数的方法，装载图片模型
        fn = fn[:(len(fn) - 4)]  # 截取图片名（这里应该把images文件中的图片名命名为为人物名）
        total_image_name.append(fn)  # 图片名字列表


def draw_face_rectangle(frame, face_locations, face_encodings):
    name = "Unknown"
    for (top, right, bottom, left), face_encoding in zip(
            face_locations, face_encodings):
        # 看看面部是否与已知人脸相匹配。
        for i, v in enumerate(total_face_encoding):
            match = face_recognition.compare_faces(
                [v], face_encoding, tolerance=0.45)
            name = "Unknown"
            if match[0]:
                name = total_image_name[i]
                break
        # 画出一个框，框住脸
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # 画出一个带名字的标签，放在框下
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255),
                      cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0,
                    (255, 255, 255), 1)
    return frame


def detect_face(frame):
    # 调用库函数，查找图片当中的人脸和对应的坐标
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    return face_locations, face_encodings


def extend_face_size(frame, left, top, right, bottom, extend_limit_width=extend_width):
    # 对剪裁的区域进行扩张，可选传入指定扩张的pixel数目
    resize = calculate_size(frame, extend_limit_width)
    print((left, top), (right, bottom))
    left = left - resize[0]
    top = top - resize[1]
    right = right + resize[0]
    bottom = bottom + resize[1]
    return left, top, right, bottom


def fix_size(frame, left, top, right, bottom):
    # 当扩大的范围超过图片本身边界的时候，对范围大小进行调整
    image_width, image_height = get_shape(frame)
    if left < 0:
        left = 0
    if top < 0:
        top = 0
    if right > image_width:
        right = image_width
    if bottom > image_height:
        bottom = image_height
    return left, top, right, bottom


def get_shape(frame):
    # 获取图片的宽和高
    shape = frame.shape
    return shape[1], shape[0]


def calculate_size(frame, limit_width):
    image_width, image_height = get_shape(frame)
    if (image_width < limit_width):
        return (image_width, image_height)  # 如果图片的尺寸小于上限，直接返回图片尺寸
    ratio = image_width / image_height  # 计算图片的比例
    max_height = int(limit_width / ratio)  # 根据传入给定的宽，通过比例，计算出对应的高
    resize = (limit_width, max_height)  # 调整图片尺寸
    return resize


def gettime():
    return time.ctime().replace(":", "_")


def save_file(frame):
    save_time = gettime()
    save_file_name = os.path.join(os.getcwd() + save_path, save_time) + ".jpg"
    static_file_name = "/static/" + save_time + ".jpg"
    cv2.imwrite(save_file_name, frame)
    cv2.imwrite(os.path.join(os.getcwd(), "static", save_time) + ".jpg", frame)
    return save_file_name, static_file_name


def compress_frame(frame, limit_width=max_width):
    resize = calculate_size(frame, limit_width)
    return cv2.resize(frame, resize, interpolation=cv2.INTER_AREA)


init_image_model()
