import generateModel


# 中间层委托文件
# 用以调用对应的不同功能并返回结果

def corp_image(filepath):
    return generateModel.corp_image_to_face(filepath)


def compare_image(filepath):
    _, static_filename, _ = generateModel.compare_image(filepath)
    return static_filename


def reload_model():
    generateModel.init_image_model()
