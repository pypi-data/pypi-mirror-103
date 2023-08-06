from typing import List, Union
import io

import numpy as np
from PIL.Image import Image

from anndb_api.anndb_api_pb import core_pb2


def vector_proto(vector:Union[List[float], np.ndarray]) -> core_pb2.Vector:
    if isinstance(vector, np.ndarray):
        return core_pb2.Vector(values=vector.tolist())

    return core_pb2.Vector(values=vector)


def image_proto(image:Union[Image,str]) -> core_pb2.Image:
    if isinstance(image, Image):
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='PNG')
        return core_pb2.Image(data=byte_arr.getvalue())

    return core_pb2.Image(url=image)
