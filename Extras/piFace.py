import pifacedigitalio as p
from psutil import cpu_percent
from time import sleep
import unittest

pf = p.PiFaceDigital()
p.init()    # Initializes the PiFace LEDs
delay = 2.0 # Replace with any value for faster or slower polling
cpu = 0

# Finds modulus of CPU percent, turns on corresponding LED, waits 
def getLeds(cpu):
        #print(cpu)
        if not boundaryTest(cpu):
                num_leds = -1
                return num_leds
        
        num_leds = cpu/12.5 # 8 Piface LEDs, thus (100%)/8 = 12.5 %
        num_leds = int(num_leds)
        turnOnLEDs(num_leds)
        
        # Indexing fix; for the sake of turning of LEDs, we do not want a range(-1,7)
       	if num_leds <= 0:
                num_leds = 1
   
        turnOffLEDs(num_leds)
        
       	sleep(delay)  # wait (delay) seconds
       	return num_leds # For unit testing
 
# For turning on LEDs from 0 to CPU%12.5
def turnOnLEDs(num):
        for i in range(0,num):
                pf.leds[i].turn_on()
                #print("led %i has turned on.", i)

# Cleaner function; for turning off all LEDs not needed
def turnOffLEDs(num):
        for k in range(num-1, 8):
                pf.leds[k].turn_off()
                #print("led %i has turned off.", k)

# Test for impossible CPU representation
def boundaryTest(cpu):
        if cpu > 100.0 or cpu < 0.0:
                return False
        return True

# Makes sure input CPU value is outputting the correct number of activated LEDs
class TestPiFace(unittest.TestCase):
       	def test_cpuToLED(self):
       	        # Impossible CPU values
       	        self.assertEqual(getLeds(-10.0), -1)
       	        self.assertEqual(getLeds(110.0), -1)
       	        # 1 - 8 LEDs lit
               	self.assertEqual(getLeds(12.5), 1)
               	self.assertEqual(getLeds(25.0), 2)
               	self.assertEqual(getLeds(37.5), 3)
               	self.assertEqual(getLeds(50.0), 4)
               	self.assertEqual(getLeds(62.5), 5)
               	self.assertEqual(getLeds(75.0), 6)
               	self.assertEqual(getLeds(87.5), 7)
               	self.assertEqual(getLeds(100.0), 8)

if __name__ == "__main__":
        # Comment out to remove unit testing
       	# unittest.main()
       	# Polls for CPU percentage, displays on LEDs
       	while(True):
       	        # When the CPU usage changes, represent it on the LEDs
       	        if(cpu !=  psutil.cpu_percent(interval=delay)):
               	        cpu = psutil.cpu_percent(interval=delay) # Percentage of CPU usage * 100
               	        leds = getLeds(cpu)

