## How to the script from terminal

To make sure that we have all the libraries that we need we create a new conda environment and activate it. 
```
conda create --name myenv
```

We then activate this environment.
```
conda activate myenv
```
After we have done this we navigate to the folder where the script is lying in. To run the script we than simply run the following command in the terminal:

```
python3 Final_Version.py 
```


 
## Intended usage
As soon as the script is executed, a window opens. The input field is already selected, but the speed test does not start until something is entered into the input field.
We can now click on the "Settings" button and create a user name and select the mode in which the highscore list should be ordered (WPM stands for words per minute and CPM for characters per minute). Now we click on the Submit button.
To start the test, we now enter the text that is displayed above the input field. To finish the test, you must have typed the whole sentence correctly. If you make a mistake, the typed text will be highlighted in red. If you have typed the whole sentence correctly, you are done. Further input is not possible. Below the input field you can see your performance. On the left side of the screen you can see your personal highscore (the highscore with this username) and the total highscore. Via the highscore button you can see the scores of all previous players, sorted by the mode you selected in the settings. 
Via the "History" button you can see the scores of all your attempts with this username.
If you want to play again, you have to click on the "Reset" button. Your username will remain the same until you change it. 