import cv2
import face_recognition
import os
import time

path = os.path.join("img", "face_recognition")  # 模型数据图片目录
save_path = os.path.join("img", "test_result")
total_image_name = []
total_face_encoding = []
max_width = 700
extend_width = 100


def init_image_model():
    for fn in os.listdir(path):  # fn 表示的是文件名q
        file_extend_name = os.path.splitext(os.path.join(os.getcwd(), path, fn))[1]
        if file_extend_name != ".png" and file_extend_name != ".jpg" and file_extend_name != ".jpeg":
            continue
        print(path + "/" + fn)
        total_face_encoding.append(
            face_recognition.face_encodings(
                face_recognition.load_image_file(os.path.join(path, fn)))[0])
        fn = fn[:(len(fn) - 4)]  # 截取图片名（这里应该把images文件中的图片名命名为为人物名）
        total_image_name.append(fn)  # 图片名字列表


def corp_image_to_face(frame):
    if (isinstance(frame, str)):
        frame = cv2.imread(frame)
    frame = compress_frame(frame)
    face_locations, _ = detect_face(frame)
    if (len(face_locations) > 1):
        print("上传了多长脸")
        return "不能有多张脸"
    for (top, right, bottom, left) in face_locations:
        left, top, right, bottom = extend_face_size(frame, left, top, right, bottom)
        left, top, right, bottom = fix_size(frame, left, top, right, bottom)
        print((left, top), (right, bottom))
        frame = frame[top:bottom, left:right]
        return frame


def extend_face_size(frame, left, top, right, bottom):
    resize = calculate_size(frame, extend_width)
    print((left, top), (right, bottom))
    left = left - resize[0]
    top = top - resize[1]
    right = right + resize[0]
    bottom = bottom + resize[1]
    return left, top, right, bottom


def fix_size(frame, left, top, right, bottom):
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
    shape = frame.shape
    return shape[1], shape[0]


def calculate_size(frame, max_width):
    image_width, image_height = get_shape(frame)
    if (image_width < max_width):
        return (image_width, image_height)
    ratio = image_width / image_height
    max_height = int(max_width / ratio)
    resize = (max_width, max_height)
    return resize


def compress_frame(frame):
    resize = calculate_size(frame, max_width)
    return cv2.resize(frame, resize, interpolation=cv2.INTER_AREA)


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


def compare_image(filename):
    frame = cv2.imread(filename)
    frame = compress_frame(frame)
    face_locations, face_encodings = detect_face(frame)
    frame = draw_face_rectangle(frame, face_locations, face_encodings)
    save_file_name, static_file_name = save_file(frame)
    print(save_file_name)
    print(static_file_name)
    return save_file_name, static_file_name, frame


def gettime():
    return time.ctime().replace(":", "_")


def save_file(frame):
    save_time = gettime()
    save_file_name = os.path.join(os.getcwd() + save_path, save_time) + ".jpg"
    static_file_name = "/static/" + save_time + ".jpg"
    cv2.imwrite(save_file_name, frame)
    cv2.imwrite(os.path.join(os.getcwd(), "static", save_time) + ".jpg", frame)
    return save_file_name, static_file_name


def detect_face(frame):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    return face_locations, face_encodings


init_image_model()

if __name__ == "__main__":
    compare_image("/Users/sunkai/Desktop/20180526_001506.jpg")
