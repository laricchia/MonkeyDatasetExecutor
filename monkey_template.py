def get_template(package, gestures):
    return '''# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import time

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

# Installs the Android package. Notice that this method returns a boolean, so you can test
# to see if the installation worked.
# device.installPackage('/mnt/com.yummly.android/2_com.yummly.android_2017-03-23.apk')

package = '%package'

# Runs the component
device.shell("monkey -p %s -c android.intent.category.LAUNCHER 1" % package)

print("---%s---%s" % (time.time(), package))
time.sleep(4)

#INSERT INSTRUCTIONS HERE
%gestures

# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile('/mnt/shot1.png','png')
'''.replace("%package", package).replace("%gestures", gestures)
