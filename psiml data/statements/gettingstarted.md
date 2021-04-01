# Getting started

Read a pixel from the top left corner of a given image and write its red, green
and blue components to the console output.

## Input

Path to the image is given through standard input. Please refer to the solution below for more details.

## Output

Result should be written to the console output in three lines, using the
following format:

```
Red: <red_component>
Green: <green_component>
Blue: <blue_component>
```

Please refer to the solution below for more details.

## Example
For a completely white image, the expected output is:
```text
Red: 255
Green: 255
Blue: 255
```

## Scoring
Correctly solving this task brings you 1 point. You can see the solution below.

## Solution

Feel free to copy/paste the given solution to see how the grading process works.

### Python
```python
import numpy as np
from PIL import Image
if __name__ == "__main__":
    image_path = input()
    image_file = Image.open(image_path)
    image = np.array(image_file)
    pixel = image[0, 0]
    print("Red: {0}".format(pixel[0]))
    print("Green: {0}".format(pixel[1]))
    print("Blue: {0}".format(pixel[2]))

```

### Checking the status of a submitted solution

You can find more details about your submitted solutions in the *Overview* tab to the left.

There are two groups of test cases (data sets):
* *Public data set* is used for developing your solution.
  After you submit your solution, you will be able to see how well your solution performs against this data set. *Public data set* is not used for calculating the final score. Public data set is available during the homework.
* *Private data set* is used for testing your solution.
  The final score will be measured against this data set. *Private data set* and the final score will be available after the homework finishes. *Private data set* contains different data than the *public data set*, but the type of data (e.g. text length, number of files, image size...) is roughly the same.

When you click on more details for a submitted solution, you can see the status, score and time and memory the solution uses per test case. Private test cases are marked with *?* during the homework.