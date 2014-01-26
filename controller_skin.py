
try:
    from PyQt5.QtCore import *
    from PyQt5.QtGui  import *
    from PyQt5.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui  import *
 

INVERT_COLORS = True

ORANGE = "#FE9309"
BLUE   = "#0317FF"

colors = {
    "color_off" : [ORANGE, BLUE][INVERT_COLORS],
    "color_on"  : [BLUE, ORANGE][INVERT_COLORS]
    }



base_css = """

QMainWindow {{
    background-color : #080808;
    }}

QPushButton {{
    border-radius : 4px;
    border : 2px solid {color_off};
    color: #c0c0c0;
    text-align: bottom left;
    padding: 5px;
    }}

QPushButton:hover {{
    background-color : #242424;
    }}

QPushButton:pressed {{
    border : 2px solid {color_on};
    }}




.BigButton {{
    background-color : #181818;
    width  : 128px;
    height : 128px;
    }}

.SmallButton {{
    background-color : #121212;
    width  : 128px;
    height : 56px;
    }}


""".format(**colors)