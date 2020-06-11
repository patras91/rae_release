How to do learning?

Directory Structure:
Data files should be in:
<your_folder>/raeResults/AIJ2020/learning/SR
<your_folder>/raeResults/AIJ2020/learning/SD
<your_folder>/raeResults/AIJ2020/learning/EE
<your_folder>/raeResults/AIJ2020/learning/CR
<your_folder>/raeResults/AIJ2020/learning/OF

Code files should be in:
<your_folder>/rae/learning/

Trained models are saved in:
<your_folder>/rae/learning/models/AIJ2020/

Files to run:

decideIntervals.py: To play with how the intervals are divided by looking at the efficiency distribution, important for learnH

convertDataFormat.py: After playing with the above, if you want to make changes in the intervals, please update the DivideIntoIntervals() function here and run this file again to convert the training data.

learnH.py: To make changes to the neural network and training params.

You can set --dataFrom and --modelFrom to be p while running the above three files.

Please send an email to patras@cs.umd.edu for any doubts.