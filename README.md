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

### Once you have installed VS Code...
--Press Ctrl+Shift+\` or Cmd+Shift+\`. The \` button is the one to the left of the 1 key
This will open a terminal window  
--Then copy and paste into the terminal  
`./micromamba.exe shell hook -s powershell | Out-String | Invoke-Expression`  
This will activate Micro Mamba, a self-contained python environment  
--Then run:  
`micromamba create -f environment.yml`  
This will install most of the necessary libraries.  
--Then run  
`micromamba activate car `  
This will activate the newly created development enviroment  
--There are a few libraries that can't be installed using the `micromamba` command, for these, we need to use pip, the "Python Package Index"    
There is a file called `pip.sh`.  Open that and copy its contents and past it into the terminal.  One it is done, we should be all set!  
