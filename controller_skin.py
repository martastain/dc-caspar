
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
    color: #c0c0c0;
    text-align: bottom left;
    padding: 5px;
    }}

QPushButton:hover {{
    background-color : #242424;
    }}

QPushButton:pressed {{
    border : 2px solid #f0f0f0;
    }}

QPushButton[ccheck="false"] {{
    border : 2px solid {color_off};
    }}

QPushButton[ccheck="true"] {{
    border : 2px solid {color_on};
    }}



.BigButton {{
    background-color : #181818;
    width  : 112px;
    height : 112px;
    }}

.SmallButton {{
    background-color : #121212;
    width  : 112px;
    height : 48px;
    }}


""".format(**colors)