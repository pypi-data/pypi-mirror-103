Function `get_gifNimage()` opens any image listed below:
* `jpg`
* `jpeg`
* `png`
* `svg`

Also it opens `gif` from a link (**in string format**). 
After that, it will be saved in the current folder, convert (if needed) to `png` (from `svg` format) and - finally - displayed. 
The function deletes the svg file after conversion - in that case, it will leave only the `png` version so there won't be any useless files in the folder.

**Importing and calling:**
```
import get_gifNimage
from get_gifNimage import get_gifNimage
# or, you can write:
# from get_gifNimage import *

# Then you can call the module (for ex.):
get_gifNimage('https://st2.depositphotos.com/1004199/6231/i/600/depositphotos_62310947-stock-photo-boxer-dog-on-white-background.jpg')
get_gifNimage('https://media.giphy.com/media/W80Y9y1XwiL84/giphy.gif')

# or:

import get_gifNimage

# Then you can call the module (for ex.):
get_gifNimage.get_gifNimage('https://st2.depositphotos.com/1004199/6231/i/600/depositphotos_62310947-stock-photo-boxer-dog-on-white-background.jpg')
get_gifNimage.get_gifNimage('https://media.giphy.com/media/W80Y9y1XwiL84/giphy.gif')
```
