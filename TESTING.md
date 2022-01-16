# Testing
I used [pep8online](http://pep8online.com/checkresult) to show the checks online

Validation for run.py

![](documentation/testing-8.png)

Validation for weather_wrapper.py

![](documentation/testing-9.png)



Entering a value that is not 1 to 3 should not be expected

![](documentation/testing-1.png)


Entering a value that is not from the completion list

![](documentation/testing-2.png)


Entering a value brings up the completor with relevant countries

![](documentation/testing-3.png)


Entering a town that does not exist will cause an error

![](documentation/testing-4.png)


Selecting option 1 while return relevant information

![](documentation/testing-5.png)


Selecting option 2 while return relevant information

![](documentation/testing-6.png)


Selecting option 3 while return relevant information

![](documentation/testing-7.png)


Changing the units of measurement

![](documentation/units-menu.png)


Entering an incorrect value for changing units of measurement

![](documentation/units-fail.png)


Unit of measurement in menu changing afterwards

![](documentation/menu-imperial.png)


Before creating the wrapper (see "API Wrapper" in README.md) I used postman so that I could see first-hand what data was returned, as shown below

![](documentation/postman-checking.png)


Using Postman to make a call to London, Canada

![](documentation/postman-canada-london-correct.png)

# Bugs
When entering a country into the country input it will treat words after a space a new word rather than the whole input as one phrase.
Other than that there are no known bugs