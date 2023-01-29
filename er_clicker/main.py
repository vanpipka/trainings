import pyautogui
import random
import time
import datetime
from make_bezier import make_bezier


def move_to(x: int, y: int, sleep: float):
    pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
    # Minimal number of seconds to sleep between mouse moves.
    pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
    # The number of seconds to pause after EVERY public function call.
    pyautogui.PAUSE = 0  # Default: 0.1
    pyautogui.FAILSAFE = False

    x1, y1 = pyautogui.position()  # Starting position

    ts = [t / 100.0 for t in range(101)]

    xys = [(x1, y1), (random.randint(1, 2559), random.randint(1, 1436)), (x, y)]

    bezier = make_bezier(xys)

    points = bezier(ts)

    duration = 0.2
    timeout = duration / len(points[0]) / 10

    for point in points:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(timeout)

    time.sleep(1.5 + random.randint(0, 1))
    pyautogui.click(x + random.randint(-5, 5), y + random.randint(-5, 5))
    time.sleep(sleep)


def autofightings() -> None:
    now = datetime.datetime.now()
    print('autofightings: ' + str(now.strftime("%d-%m-%Y %H:%M")))

    fighting_button_coords = (1207, 166)
    fighting_type_button_coords = (1078, 253)

    conditions = ("search_new", "waiting_for", "fighting")
    condition = conditions[0]

    while True:

        if condition == conditions[0]:

            move_to(fighting_button_coords[0] + random.randint(-15, 15),
                    fighting_button_coords[1] + random.randint(-15, 15), 0)
            move_to(fighting_type_button_coords[0] + random.randint(-15, 15), fighting_type_button_coords[1], 0)

            while True:
                fight_coords = pyautogui.locateCenterOnScreen("static\\new_order.png", confidence=0.9)
                if fight_coords:
                    move_to(fight_coords.x - 350, fight_coords.y, 0)
                    if pyautogui.locateCenterOnScreen("static\\cancel.png", confidence=0.9):
                        condition = conditions[1]
                        break
                else:
                    move_to(fighting_type_button_coords[0] + random.randint(-15, 15), fighting_type_button_coords[1], 0)

        elif condition == conditions[1]:

            while True:
                go_coords = pyautogui.locateCenterOnScreen("static\\go.png", confidence=0.9)
                refresh_coords = pyautogui.locateCenterOnScreen("static\\refresh.png", confidence=0.9)
                finish_coords = pyautogui.locateCenterOnScreen("static\\finish.png", confidence=0.9)

                if finish_coords:
                    move_to(finish_coords[0] + random.randint(-15, 15), finish_coords[1], 0)
                    condition = conditions[0]
                    break
                elif go_coords:
                    move_to(go_coords[0] + random.randint(-15, 15), go_coords[1], 0)
                    time.sleep(random.randint(0, 2))
                elif refresh_coords:
                    move_to(refresh_coords[0] + random.randint(-15, 15), refresh_coords[1], 0)
                else:
                    time.sleep(random.randint(0, 3))

    # c_width, c_height = pyautogui.position()
    # print(c_width, c_height)


def butterflies_farming() -> None:
    now = datetime.datetime.now()
    print('butterflies_farming: ' + str(now.strftime("%d-%m-%Y %H:%M")))
    return

    c_width, c_height = pyautogui.position()
    step_count = 1
    add_step_count = False
    search_button_coords = [138, 330]
    exit_coords = [1487, 410]

    coords = [[1329, 542], [1326, 586], [1244, 580], [1240, 534]]

    all = 0
    all_search = 0

    print(c_width, c_height)

    while True:

        for x in coords:

            for y in range(step_count):

                move_to(x[0], x[1], random.randint(3, 5))
                move_to(search_button_coords[0], search_button_coords[1], random.randint(32, 40))
                all_search += 1

                while True:

                    img_find = pyautogui.locateCenterOnScreen("static\\img_1.png", confidence=0.9)

                    if img_find:

                        all += 1
                        move_to(img_find.x, img_find.y, 1)
                        print(str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")) + '/ всего найдено: '
                              + str(all) + " из " + str(all_search))
                    else:
                        break

                img_find = pyautogui.locateCenterOnScreen("static\\img_2.png", confidence=0.9)

                if img_find:
                    move_to(exit_coords[0], exit_coords[1], random.randint(1, 3))

            add_step_count = not add_step_count

            if add_step_count is False:
                step_count = step_count + 1


def main():
    print("Choose the option:")
    print("1. butterflies farming")
    print("2. autofighting")
    option = input()

    if option == "1":
        butterflies_farming()
    elif option == "2":
        autofightings()
    else:
        main()


if __name__ == "__main__":
    main()
