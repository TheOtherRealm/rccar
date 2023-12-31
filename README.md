This is the link to the motor driver info: https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide

Here is where you can download the necessary library for the motor driver to work: https://github.com/sparkfun/SparkFun_TB6612FNG_Arduino_Library/archive/master.zip

Here is a table of connections from Ardiuno 
```
Motor Driver	Arduino  
AIN1		D8  
BIN1		D5  
AIN2		D9  
BIN2		D4  
PWMA  	        D10  
PWMB	        D3  
STBY		D7  
GND		GND  
VCC		5V  
--Connect to battery—  
Motor Driver	Battery  
VM		Positive/Red  
GND		Negative/Black  
```

<h1 style="text-align:center">Car CAD Code!</h1>
<p  style="text-align:center">The code that was used to generate the CAD files used in the 3D printer</p>

<p>We will primarily be using the Build123D Python API ( <a href='https://build123d.readthedocs.io/en/latest/index.html' title='Build123D'>https://build123d.readthedocs.io/en/latest/index.html</a> ) to create our models.  Although it may seem a little daunting at first glance, it allows you to create complex things quickly, and tweak parameters easily, once you get the hang of things.  And best of all, it's free and open source!</p>

## Python
If you want to learn more about Python, some good places to go are:  
The main Python website: https://www.python.org/  
Some other resources:  
https://developers.google.com/edu/python/  
https://www.w3schools.com/python/python_intro.asp
https://www.geeksforgeeks.org/python-programming-language/#
... or just do a search for python and a bazillion more usefull sites will show up - the basics are well documented.

## Arduino
We will be using Arduino for our project (under the /car.ino folder)
You can learn more about that at: https://www.arduino.cc/

## Setting things up  
Install Visual Studio Code: https://code.visualstudio.com/#alt-downloads  
Install git: https://git-scm.com/download/win  

### Once you have installed VS Code and git...
-- Press Ctrl+Shift+\` or Cmd+Shift+\`. The \` button is the one to the left of the 1 key
This will open a terminal window  
-- Then copy and paste into the terminal  
`./micromamba.exe shell hook -s powershell | Out-String | Invoke-Expression`  
This will activate Micro Mamba, a self-contained python environment  
-- Then run:  
`micromamba create -f environment.yml`  
This will install most of the necessary libraries.  
-- Then run  
`micromamba activate car `  
This will activate the newly created development environment  
-- There are a few libraries that can't be installed using the `micromamba` command, for these, we need to use pip, the "Python Package Index"    
There is a file called `pip.sh`.  Open that and copy its contents and past it into the terminal.  One it is done, we should be all set!  

-- Now we need to make some changes to the VS Code `settings.json` file so that the application knows where to find python.  This will depend on the OS, I will help you figure out where it is individually     

-- Now open the file called `car.ipynb`  
Put the curser in the first code box and press Shift+Enter  
Repeat this to run the other code blocks and see the 3D models that are output.  
