# timetable
This Python script is a timetables game in combination with Raspberry PI connected to some elecrtonic devices (via http://wiringpi.com/):
+ it generates automatically a multiplication
+ it asks the result:
  + wait for 5 seconds or store the result # the countdown is displayed on the seven segment screen
    + if there is no result, then the red LED is on for a short amount of time and the game stops
    + if the result is wrong, then the red LED is on for a short amount of time and the game stops
    + if the result is right, then:
      + the green LED is on for a short amount of time, the score is updated and the game continues.
    
    
    
  
