from robot.api.deco import keyword


class CoffeeMachineExtended(object):
    @keyword("Idle")
    def idle(self):
        print(r'Check that machine is in Idle state.')

    @keyword("Selecting")
    def selecting(self):
        print(r'Check that machine shows the selection menu.')

    @keyword("Canceling")
    def canceling(self):
        print(r'Check that machine is canceling the selection.')

    @keyword("Serving")
    def serving(self):
        print(r'Check that machine is serving the selected coffee.')

    @keyword("Returning Change")
    def returning_change(self):
        print(r'Check that machine has returned the correct amount of change.')

    @keyword("Turn ON")
    def turn_on(self):
        print(r'Turn on the coffee machine...')

    @keyword("Input Money")
    def input_money(self):
        print(r'Input an amount of money...')

    @keyword("Cancel")
    def cancel(self):
        print(r'Cancel the current selection...')

    @keyword("Select Coffee")
    def select_coffee(self):
        print(r'Select a given coffee option...')

    @keyword("Return Change")
    def return_change(self):
        print(r'Return the given amount of change...')

    @keyword("Return to Idle state")
    def return_to_idle_state(self):
        print(r'Return to main menu...')

    @keyword("OFF")
    def off(self):
        print(r'Checking that coffee machine is in off state...')

    @keyword("Turn OFF")
    def turn_off(self):
        print(r'Turn OFF the machine...')