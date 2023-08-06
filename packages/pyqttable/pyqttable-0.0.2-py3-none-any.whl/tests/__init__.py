# -*- coding: utf-8 -*-
"""doc string"""

import datetime as dt
import pandas as pd
import sys

from PyQt5 import QtWidgets
from pyqttable import PyQtTable

app = QtWidgets.QApplication(sys.argv)
config = [
    {
        'key': 'name',
        'name': 'Name',
        'editable': False,
        'filter_type': 'contain',
    },
    {
        'key': 'age',
        'name': 'Age',
        'type': int,
        'h_align': 'r',
        'filter_type': 'expression',
    },
    {
        'key': 'gender',
        'name': 'Gender',
        'selection': ['male', 'female'],
        'filter_type': 'multiple_choice',
    },
    {
        'key': 'smart',
        'name': 'Smart',
        'type': bool,
        'filter_type': 'multiple_choice',
    },
    {
        'key': 'birthday',
        'name': 'Birthday',
        'type': dt.date,
        'filter_type': 'expression',
    },
]
table = PyQtTable(None, config, True, True, True)
data = pd.DataFrame([
    {
        'name': 'Xu Tongyan',
        'age': 27,
        'gender': 'male',
        'smart': True,
        'birthday': dt.date(1994, 6, 27),
    },
    {
        'name': 'Su Chenyao',
        'age': 24,
        'gender': 'female',
        'smart': False,
        'birthday': dt.date(1996, 10, 12),
    },
])
table.set_data(data)
table.setMinimumWidth(400)
table.setMinimumHeight(300)
table.show()
signal = app.exec_()
print(table.get_data(full=False))
print(table.get_filter_data())
sys.exit(signal)
