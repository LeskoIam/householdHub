# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.
# https://github.com/quentinsf/qhue

from typing import Callable, Optional

from qhue import Bridge, QhueException, create_new_username

# the IP address of your bridge
BRIDGE_IP = "192.168.1.51"

# the path for the username credentials file
CRED_FILE_PATH = "qhue_username.txt"


class Hue:

    def __init__(self, bridge_ip: str, credentials: Optional[str] = None):
        self.bridge_ip = bridge_ip
        self.credentials = credentials

        self.bridge = None
        self.lights = {}

    def register_hue(self, save_credentials_cb: Optional[Callable] = None):
        if self.credentials is None:
            while True:
                try:
                    self.credentials = create_new_username(BRIDGE_IP)
                    if save_credentials_cb is not None:
                        save_credentials_cb(self.credentials)
                        break
                except QhueException as err:
                    print("Error occurred while creating a new username: {}".format(err))

    def __create_bridge(self):
        if self.bridge is None:
            self.bridge = Bridge(self.bridge_ip, self.credentials)

    def find_all_lights(self):
        self.__create_bridge()
        lights = self.bridge.lights
        for key, val in lights().items():
            self.lights[key] = lights[key]

    def list_devices(self):
        self.find_all_lights()
        for hue_num, light in self.lights.items():
            print(f"{hue_num} - {light}")
            for key, val in light().items():
                print(f"\t{key} - {val}")


if __name__ == "__main__":
    with open(CRED_FILE_PATH, "r") as cred_file:
        username = cred_file.read()


    def p(tes):
        print(tes)


    h = Hue(BRIDGE_IP, credentials=username)

    h.list_devices()
