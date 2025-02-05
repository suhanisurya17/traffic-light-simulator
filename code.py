
import machine #this statement imports the machine module
from ssd1306 import SSD1306_I2C #this statement imports the ssd1306 module
from time import sleep, ticks_ms, sleep_ms #this statement imports the time module

# Pin variables
redLed1Pin = 9 #setting the GPIO pin of the first red led
yellowLed1Pin = 10 #setting the GPIO pin of the first yellow led
greenLed1Pin = 11 #setting the GPIO pin of the first green led

redLed2Pin = 12 #setting the GPIO pin of the second red led
yellowLed2Pin = 13 #setting the GPIO pin of the second yellow led
greenLed2Pin = 14 #setting the GPIO pin of the second green led

buzzerPin = 15 #this statement sets the GPIO pin for the buzzer

oledsdaPin = 16 #this statement sets the GPIO pin for the sda on the oled
oledsclPin = 17 #this statement sets the GPIO pin for the scl on the oled

oledWidthPX = 128 #this variable stores the width of the oled in pixels
oledHeightPX = 64 #this variable stores the height of the oled in pixels

row1Time = 10
row2Time = 3
row3Time = 2

row4Time = row1Time
row5Time = row2Time
row6Time = row3Time

# Initializing objects
redLed1 = machine.Pin(redLed1Pin, machine.Pin.OUT) #this statement initializes the redLed1 object
yellowLed1 = machine.Pin(yellowLed1Pin, machine.Pin.OUT)#this statement initializes the yellowLed1 object
greenLed1 = machine.Pin(greenLed1Pin, machine.Pin.OUT)#this statement initializes the greenLed1 object

redLed2 = machine.Pin(redLed2Pin, machine.Pin.OUT)  #this statement initializes the redLed2 object
yellowLed2 = machine.Pin(yellowLed2Pin, machine.Pin.OUT)#this statement initializes the yellowLed2 object
greenLed2 = machine.Pin(greenLed2Pin, machine.Pin.OUT)#this statement initializes the greenLed1 object

buzzer = machine.PWM(machine.Pin(buzzerPin))#initializing a buzzer object

i2c = machine.I2C(0, sda=machine.Pin(oledsdaPin), scl=machine.Pin(oledsclPin), freq=400000) #setting the i2c protocol for the oled display
oled = SSD1306_I2C(oledWidthPX, oledHeightPX, i2c) #creating the oled object

# Set initial values of all leds to off
redLed1.value(0)
yellowLed1.value(0)
greenLed1.value(0)

redLed2.value(0)
yellowLed2.value(0)
greenLed2.value(0)

def tone(pin, frequency, duration): #this function accepts three parameters; the pin object, frequency of the buzzer sound and the duration of the buzzer sound
    pin.freq(frequency) #setting the frequency to the value set by the user
    pin.duty_u16(30000) #setting the duty cycle to the value set by the user
    sleep_ms(duration) #this statement sets the delay to the duration in seconds set by the user
    pin.duty_u16(0)

#This is the function to draw a thick progress bar line
#It accepts arguments for the object, x, y position, length, thickness and color
def draw_thick_hline(oled, x, y, length, thickness, color):
    #for loop that iterates for the thickness (i.e the number of pixels thick)
    for i in range(0, thickness):
        oled.hline(x, 64 - i, length, color)
        #this statement draws a horizontal line and as the loop iterates, the y position is increased by 1. The x, length and color remain the same

# Function I created to update progress bar
def update_progress_bar(counter, max_count, oled, y):#this function accepts 4 parameters; the counter, ax count of the progress bar, the led object and the y coordinate of the line
    if counter == 1:#this line bvasically ensures that when the counter  = 1, the width of the bar is zero to mimic the example
        draw_thick_hline(oled, 0, y, 0, 8, 1)
    else: #this statement will execute if the counter is not one
        length = int((oledWidthPX / (max_count - 1)) * (counter - 1)) #the length of the line is the width of the oled (128px) divided by the max number of intervals for decreasing
                                                                      #this is so that when the time duration of a section f the sequence is 10 seconds, the progress bar is divided
                                                                      #when the counter is 1, the line width is zero.
        draw_thick_hline(oled, 0, y, length, 8, 1) #this line calls the draw thick line function to redraw the updated line with the most recent length

# Infinite while loop to make the sequence
while True:
    # row 1
    greenLed1.value(1) #this statement turns on greenLed1
    redLed2.value(1) #this statement turns on redLed2
    
    for counter in range(row1Time, 0, -1): #this is a for loop that will iterate 10 times, once for every second
        oled.fill(0) #this clears the screen so it can be populated with the most recent info
        msg = "  LIGHT 1: GO" #setting the msg variable = to "LIGHT 1: GO"
        oled.text(msg, 0, 0, 1) #creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 1: Green" #setting the msg variable = to "Light 1: Green"
        oled.text(msg, 0, 20, 1) #creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 2: Red" #setting the msg variable = to "Light 2: Red"
        oled.text(msg, 0, 30, 1) #creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        oled.text('Time: ' + str(counter), 0, 40, 1) #this statement prints the current time based on the foor loop counter variable
        update_progress_bar(counter, row1Time, oled, 60) #this statement calls the update progress bar function to update the width of the progress bar
        oled.show() #this statement displays all the text onto the oled
        if counter <= 3: #if the counter is less than or equal to 3
            tone(buzzer, 1000, 200) #it sounds the buzzer at 1000hz for 200ms
        sleep(1)#delay for one second

    # row 2
    greenLed1.value(0) #this statement turns off the greenLed1
    yellowLed1.value(1) #this statement turns on the yellowLed1

#     previousMillis = ticks_ms() #this statement g
#     prevSeconds = previousMillis / 1000
#     print(prevSeconds)

    #Turning on the buzzer
    buzzer.freq(1000) #this statement turns n the buzzer at a frequency of 1000hz
    buzzer.duty_u16(30000) #this statement sets the duty cycle to 30000

    for counter in range(row2Time, 0, -1): #this is a for loop that will iterate 3 times, once for every second
        oled.fill(0) #this clears the screen so it can be populated with the most recent info
        msg = "PREPARE TO STOP!"#setting the msg variable = to "PREPARE TO STOP!"
        oled.text(msg, 0, 0, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 1: Yellow"#setting the msg variable = to "Light 1: Yellow"
        oled.text(msg, 0, 20, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 2: Red"#setting the msg variable = to "Light 2: Red"
        oled.text(msg, 0, 30, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        oled.text('Time: ' + str(counter), 0, 40, 1)#this statement prints the current time based on the foor loop counter variable
        update_progress_bar(counter, row2Time, oled, 60)#this statement calls the update progress bar function to update the width of the progress bar
        oled.show()#this statement displays all the text onto the oled
        sleep(1)#delay for one second

    buzzer.duty_u16(0)#this statement sets the duty cycle of the buzzer to zero, meaning that you make it stop buzzing

    # row 3
    yellowLed1.value(0)#this statement turns off yellowLed1
    redLed1.value(1)#this statement turns on redLed1
 
    for counter in range(row3Time, 0, -1): #this is a for loop that will iterate 2 times, once for every second
        oled.fill(0)#this clears the screen so it can be populated with the most recent info
        msg = "      STOP!"#setting the msg variable = to "STOP!"
        oled.text(msg, 0, 0, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 1: Red"#setting the msg variable = to "Light 1: Red"
        oled.text(msg, 0, 20, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 2: Red"#setting the msg variable = to "Light 2: Red"
        oled.text(msg, 0, 30, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        oled.text('Time: ' + str(counter), 0, 40, 1)#this statement prints the current time based on the foor loop counter variable
        update_progress_bar(counter, row3Time, oled, 60)#this statement calls the update progress bar function to update the width of the progress bar
        oled.show()#this statement displays all the text onto the oled
        sleep(1)  # Add this line to introduce a delay of 1 second

    # row 4
    redLed2.value(0) #this statement turns off redLed2
    greenLed2.value(1) #this statement turns on greenLed2

    for counter in range(row4Time, 0, -1):#this is a for loop that will iterate 10 times, once for every second
        oled.fill(0)#this clears the screen so it can be populated with the most recent info
        msg = "   LIGHT 2: GO"#setting the msg variable = to "LIGHT 2: GO"
        oled.text(msg, 0, 0, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 1: Red"#setting the msg variable = to "Light 1: Red"
        oled.text(msg, 0, 20, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 2: Green"#setting the msg variable = to "Light 2: Green"
        oled.text(msg, 0, 30, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        oled.text('Time: ' + str(counter), 0, 40, 1)#this statement prints the current time based on the foor loop counter variable
        update_progress_bar(counter, row4Time, oled, 60)#this statement calls the update progress bar function to update the width of the progress bar
        oled.show()#this statement displays all the text onto the oled
        if counter <= 3: #if the counter is less than or equal to 3
            tone(buzzer, 1000, 200)#it sounds the buzzer at 1000hz for 200ms
        sleep(1)  #delay of 1 second

    # row 5
    greenLed2.value(0)#this statement turns off greenLed2
    yellowLed2.value(1) #this statement turns of yellowLed2

    # Start the buzzer for 3 seconds
    buzzer.freq(1000) #this statement sets the buzzer frequency to 1000 hz
    buzzer.duty_u16(30000) #this statement sets the duty cycle

    for counter in range(row5Time, 0, -1):#this is a for loop that will iterate 3 times, once for every second
        oled.fill(0)#this clears the screen so it can be populated with the most recent info
        msg = "PREPARE TO STOP!"#setting the msg variable = to "PREPARE TO STOP!"
        oled.text(msg, 0, 0, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 1: Red"#setting the msg variable = to "Light 1: Red"
        oled.text(msg, 0, 20, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 2: Yellow"#setting the msg variable = to "Light 2: Yellow"
        oled.text(msg, 0, 30, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        oled.text('Time: ' + str(counter), 0, 40, 1)#this statement prints the current time based on the foor loop counter variable
        update_progress_bar(counter, row5Time, oled, 60)#this statement calls the update progress bar function to update the width of the progress bar
        oled.show()#this statement displays all the text onto the oled
        currentMillis = ticks_ms()
        seconds = currentMillis / 1000
        print(seconds)
        sleep(1)

    # Stop the buzzer
    buzzer.duty_u16(0)#this statement turns the buzzer off by setting duty cycle to 0

    # row 6
    yellowLed2.value(0)#this statement turns off yellowLed2
    redLed2.value(1)#this statement turns on redLed2

    for counter in range(row6Time, 0, -1):#this is a for loop that will iterate 2 times, once for every second
        oled.fill(0)#this clears the screen so it can be populated with the most recent info
        msg = "      STOP!"#setting the msg variable = to "STOP!"
        oled.text(msg, 0, 0, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 1: Red"#setting the msg variable = to "Light 1: Red"
        oled.text(msg, 0, 20, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        msg = "Light 2: Red"#setting the msg variable = to  "Light 2: Red"
        oled.text(msg, 0, 30, 1)#creating text on the oled for the status of the light; e.g: go, prepare to stop and stop
        oled.text('Time: ' + str(counter), 0, 40, 1)#this statement prints the current time based on the foor loop counter variable
        update_progress_bar(counter, row6Time, oled, 60)#this statement calls the update progress bar function to update the width of the progress bar

        oled.show()#this statement displays all the text onto the oled
        sleep(1)  #delay of 1 second

    # completing cycle
    redLed2.value(0)#this statement turns off redLed2
    redLed1.value(0)#this statement turns off redLed1

