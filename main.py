from tools import RicoGesturesUtils as RGU
import monkey_template


def print_monkey_gesture(rico_gesture):
    ret_s = "print('---%s---%s' % (time.time(), '" + "%s'))\n" % rico_gesture.activity
    sleep_after = "time.sleep(2)\n\n"
    if rico_gesture.type == RGU.RicoGesture.TYPE_PRESS:
        return ret_s+"device.touch(%d, %d, MonkeyDevice.DOWN_AND_UP)\n" % (rico_gesture.start_x, rico_gesture.start_y) + sleep_after
    elif rico_gesture.type == RGU.RicoGesture.TYPE_DRAG:
        return ret_s+"device.drag((%d, %d), (%d, %d), 0.25, 10)\n" % (rico_gesture.start_x, rico_gesture.start_y, rico_gesture.end_x, rico_gesture.end_y) + sleep_after

def build_monkey_file_for_package(package):
    ricoGestUtil = RGU.RicoGestureUtils(720, 1280, "/mnt/%s" % package)
    ricoGestUtil.parseGesturesFile()

    # print( ricoGestUtil.getNextGesture().type )

    gesture_list = "\n".join(list(map(lambda x: print_monkey_gesture(x), ricoGestUtil.getNextGesture())))

    with open("/mnt/%s/monkey.py" % package, "w") as file:
        file.writelines(monkey_template.get_template(package, gesture_list))


package_ = "com.yummly.android"

build_monkey_file_for_package(package_)

#ricoGestUtil = RGU.RicoGestureUtils(720, 1280, "/mnt/com.yummly.android")

#print(gesture_list)
