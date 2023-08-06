import json
import os
def get_imagenet_label_mapping() -> dict:
    # print(os.path.abspath("."))
    # print(os.path.curdir)
    # 坑壁啊，居然默认是在整个项目的根目录下
    with open("src\DatasetsHelperQ\data\mapping.json", 'r') as f:
        mapping = json.loads(f.read())
    return mapping

