import os
from datetime import timedelta
from typing import List

import cv2
import numpy as np

from services import create_path, get_file_name, get_path_from_file_name


PATH_FOR_DATA = os.path.join(os.curdir, "data")


def format_timedelta(td: timedelta) -> str:
    return (str(td) + "-00").replace(":", "-")


def get_saving_frames_durations(cap, saving_fps) -> List:
    # получаем продолжительность клипа, разделив количество кадров на количество кадров в секунду
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    return [i for i in np.arange(3, clip_duration, 2)]


class CompareImage:

    def __init__(self, image_path_1: str, image_path_2: str):
        self._image1 = image_path_1
        self._image2 = image_path_2
        self._image1_hash = self.calc_image_hash(self._image1)
        self._image2_hash = self.calc_image_hash(self._image2)

    def its_similar(self) -> bool:

        different_bites = 0
        for i in range(len(self._image1_hash)):
            if self._image1_hash[i] != self._image2_hash[i]:
                different_bites += 1

        return different_bites < 1

    @staticmethod
    def calc_image_hash(file_name: str) -> str:

        if not file_name:
            raise ValueError("The file_name should not be an empty string")

        image = cv2.imread(file_name)  # Прочитаем картинку
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
        avg = gray_image.mean()  # Среднее значение пикселя
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

        # Рассчитаем хэш
        _hash = ""
        for x in range(8):
            for y in range(8):
                val = threshold_image[x, y]
                if val == 255:
                    _hash = _hash + "1"
                else:
                    _hash = _hash + "0"

        return _hash


def create_pictures_from_video(video_file):

    img_path_name = f"{get_path_from_file_name(video_file)}\\img"
    create_path(img_path_name)

    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)

    prev_frame_name = ""

    saving_frames_durations = get_saving_frames_durations(cap, fps)
    count = 0

    while True:
        is_read, frame = cap.read()
        if not is_read:
            break

        frame_duration = count / fps
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break
        if frame_duration >= closest_duration:
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            frame_name = f"{img_path_name}\\frame_{frame_duration_formatted}.jpg"

            if cv2.imwrite(frame_name, frame):
                if prev_frame_name:
                    if CompareImage(frame_name, prev_frame_name).its_similar():
                        os.remove(frame_name)
                    else:
                        prev_frame_name = frame_name
                else:
                    prev_frame_name = frame_name

            else:
                print('not')
            # удалить точку продолжительности из списка, так как эта точка длительности уже сохранена
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # увеличить количество кадров
        count += 1