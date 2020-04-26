from robot.api.deco import keyword


class AirHandlerStates(object):
    @keyword('Idle')
    def idle(self):
        print(r'Checking "Idle" state...')

    @keyword('Cooling Down')
    def cooling_down(self):
        print(r'Checking "Cooling Down" state...')

    @keyword('Warming Up')
    def warming_up(self):
        print(r'Checking "Warming Up" state...')

    @keyword('Off')
    def off(self):
        print(r'Checking "Off" state...')
