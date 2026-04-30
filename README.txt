howdy
sorry we didn't get more done on the GUI
i mean it definately works but there were some other features that we didn't get to

make sure you test the GUI before the launch, there are some dependancies that you might have to install
just run GUI/GPSGUI.py

to edit the tranmsitter board properties (frequency, output power, callsign, GPS baudrate) go to user_defines at
Projects\NUCLEO-WL55JC\Applications\SubGHz_Phy\SubGHz_Phy_PingPong_DualCore\STM32CubeIDE\CM4\Application\User\Includes\user_defines.h
STM baud is 9600, uBlox buad is 38400

WHATEVER YOU DO DON'T SET ONE FREQUENCY TO 13560Hz AND THE OTHER TO 7.889GHz. just don't