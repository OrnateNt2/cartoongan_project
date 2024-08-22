import cv2
import numpy as np
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .model import load_model

interpreter = load_model()
executor = ThreadPoolExecutor()

def create_weight_map(size, overlap):
    map_1d = np.linspace(0, 1, overlap)
    map_2d = np.outer(map_1d, map_1d)
    weight_map = np.ones(size)

    weight_map[:overlap, :overlap] *= map_2d
    weight_map[-overlap:, :overlap] *= map_2d[::-1, :]
    weight_map[:overlap, -overlap:] *= map_2d[:, ::-1]
    weight_map[-overlap:, -overlap:] *= map_2d[::-1, ::-1]

    weight_map[:overlap, overlap:-overlap] *= map_1d[:, np.newaxis]
    weight_map[-overlap:, overlap:-overlap] *= map_1d[::-1, np.newaxis]
    weight_map[overlap:-overlap, :overlap] *= map_1d[np.newaxis, :]
    weight_map[overlap:-overlap, -overlap:] *= map_1d[np.newaxis, ::-1]

    return weight_map

def process_image_block(image_block, interpreter):
    input_data = cv2.resize(image_block, (512, 512))
    input_data = np.expand_dims(input_data, axis=0).astype(np.float32) / 127.5 - 1

    input_index = interpreter.get_input_details()[0]['index']
    interpreter.set_tensor(input_index, input_data)
    interpreter.invoke()

    output_index = interpreter.get_output_details()[0]['index']
    output_data = interpreter.get_tensor(output_index)
    output_image = (output_data.squeeze() + 1) * 127.5
    output_image = np.clip(output_image, 0, 255).astype(np.uint8)

    return output_image

def process_image(image_data):
    np_arr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    h, w, _ = image.shape

    output_image = np.zeros_like(image, dtype=np.float32)
    weight_sum = np.zeros_like(image, dtype=np.float32)
    step = 512 - 50  # Предполагаемое перекрытие в 50 пикселей
    weight_map = create_weight_map((512, 512), 50)
    weight_map = np.expand_dims(weight_map, axis=-1)
    weight_map = np.repeat(weight_map, 3, axis=-1)

    for i in range(0, h, step):
        for j in range(0, w, step):
            block = image[i:i+512, j:j+512]
            if block.shape[0] != 512 or block.shape[1] != 512:
                block = cv2.copyMakeBorder(block, 0, 512-block.shape[0], 0, 512-block.shape[1], cv2.BORDER_REFLECT)

            processed_block = process_image_block(block, interpreter)

            output_image[i:i+512, j:j+512] += processed_block[:min(512, h-i), :min(512, w-j)] * weight_map[:min(512, h-i), :min(512, w-j)]
            weight_sum[i:i+512, j:j+512] += weight_map[:min(512, h-i), :min(512, w-j)]

    weight_sum[weight_sum == 0] = 1  # Избегаем деления на ноль
    output_image = (output_image / weight_sum).astype(np.uint8)

    _, buffer = cv2.imencode('.jpg', output_image)
    return buffer.tobytes()

async def async_process_image(image_data):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, process_image, image_data)
