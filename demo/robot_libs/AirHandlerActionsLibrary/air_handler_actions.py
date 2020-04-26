from robot.api.deco import keyword


class AirHandlerActions(object):
    @keyword('Turn AC ON')
    def turn_ac_on(self):
        print(r'Setting "Turn AC ON" state...')

    @keyword('Turn Heat ON')
    def turn_heat_on(self):
        print(r'Setting "Turn Heat ON" state...')

    @keyword('Reach Desired Temp')
    def reach_desired_temp(self):
        print(r'Setting "Reach Desired Temperature" state...')

    @keyword('Switch OFF')
    def switch_off(self):
        print(r'Setting "Switch OFF" state...')

    @keyword('Switch ON')
    def switch_on(self):
        print(r'Setting "Switch ON" state...')
