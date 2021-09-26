# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
import numpy as np
import random
import pandas as pd
import json
from tweet import Tweet
from tracker import Tracker
from application_ui import Ui_Application
from datetime import datetime

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import os 
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
     
class Application(qtw.QWidget):  
    '''class variables'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ui = Ui_Application()
        self.ui.setupUi(self)
        self.ui.push_button_1.clicked.connect(lambda: self.display(0))
        self.ui.push_button_2.clicked.connect(lambda: self.display(1))
        self.ui.push_button_3.clicked.connect(lambda: self.display(2))
        self.timer = qtc.QTimer()
        self.timer_2 = qtc.QTimer()
        self.timer_2.start(5000)
        self.timer.start(1000)
        self.update_tweet_screen()
        self.timer.timeout.connect(self.update_main_screen)
        self.timer.timeout.connect(lambda: self.ui.label_time.setText(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        self.timer_2.timeout.connect(lambda: self.update_market_screen())
        self.timer_2.timeout.connect(lambda: self.update_tweet_screen())

        self.setWindowTitle("Scraped BETA")
        self.ui.stackedWidget.setCurrentIndex(1)

    #this is called upon when no data is available
    def default_value_main_screen(self):
        self.ui.bar_tracker_1.canvas.axes.clear()
        self.ui.bar_tracker_1.canvas.axes.grid(color='green', linestyle='--', linewidth=0.5)
        self.ui.bar_tracker_1.canvas.axes.set_ylabel('likes', color='green')
        self.ui.bar_tracker_1.canvas.axes.set_title('main tracker overview', color='green')
        self.ui.bar_tracker_1.canvas.draw()
        self.ui.tracker_names.setText('NO DATA')
        self.ui.tracker_likes.setText('NO DATA')
        self.ui.tracker_likes_5.setText('NO DATA')

    def update_main_screen(self):
        try: 
            data = pd.read_excel(r'python\Data\export_list_sorted.xlsx')
            names = []
            for name in (data[0])[:10]:
                names.append(name)
            values = []
            for value in (data[1])[:10]:
                values.append(value)

            self.ui.bar_tracker_1.canvas.axes.clear()
            self.ui.bar_tracker_1.canvas.axes.grid(color='green', linestyle='--', linewidth=0.5)
            self.ui.bar_tracker_1.canvas.axes.bar(names,values, color='green')
            self.ui.bar_tracker_1.canvas.axes.set_ylabel('likes', color='green')
            self.ui.bar_tracker_1.canvas.axes.set_title('main tracker overview', color='green')
            self.ui.bar_tracker_1.canvas.draw()
            self.ui.tracker_names.setText((data[0])[:20].to_string(index=False))
            self.ui.tracker_likes.setText((data[1])[:20].to_string(index=False))
            self.ui.tracker_mentions.setText((data[2])[:20].to_string(index=False))
            self.ui.tracker_likes_5.setText((data[3])[:20].to_string(index=False, header=None))
        except: 
            self.default_value_main_screen()

    def update_market_screen(self):
        print('timer')
        data = pd.read_csv(r'python\Data\export_list_likes.csv', header=None)
        data = data.sort_values(data.columns[-1], ascending=False)
        data = (np.matrix(data)[:,1:])
        data_names = data[:,:1]
        data_likes = data[:,1:]

        tracker_windows = [
            self.ui.likes_tracker_1,
            self.ui.likes_tracker_2,
            self.ui.likes_tracker_3,
            self.ui.likes_tracker_4,
            self.ui.likes_tracker_5,
            self.ui.likes_tracker_6,
            self.ui.likes_tracker_7,
            self.ui.likes_tracker_8,
            self.ui.likes_tracker_9,
            self.ui.likes_tracker_10,
            self.ui.likes_tracker_11,
            self.ui.likes_tracker_12
        ]

        
        for id, tracker in enumerate(tracker_windows):
            tracker.canvas.axes.clear()
            tracker.canvas.axes.grid(color='green', linestyle='--', linewidth=0.1)
            tracker.canvas.axes.set_title(data_names[id,0], color='green')
            tracker.canvas.axes.yaxis.set_tick_params(labelsize=6, rotation=45)
            tracker.canvas.axes.xaxis.set_tick_params(labelsize=6, rotation=45)
            tracker.canvas.axes.set_xlim(0,12)
            tracker.canvas.axes.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12])
            tracker.canvas.axes.set_xticklabels(['-60m', '-55m', '-50m', '-45m', '-40m', '-35m', '-30m', '-25m', '-20m', '-15m', '-10m', '-5m', '0'])
            x_data = np.linspace(0,12,13)
            y_data = []
            for i in range(13):
                try:
                    y_data.append(data_likes[id, -13+i])
                except IndexError:
                    y_data.append(0)

            tracker.canvas.axes.plot(x_data, y_data, color='green')
            tracker.canvas.axes.set_ylim((0, max(y_data)*3/2))
            tracker.canvas.draw()
        return

    def update_tweet_screen(self):
        with open(r'python\Data\export_tracker_tweets.json') as json_file:
            data = pd.DataFrame(json.load(json_file))

        print(data['user'])
        self.ui.tweets_user.setText(pd.DataFrame(data['user']).to_string())
        self.ui.tweets_content.setText(pd.DataFrame(data['content']).to_string())
        self.ui.tweets_likes.setText(pd.DataFrame(data['likes']).to_string())
        self.ui.tweets_date.setText(pd.DataFrame(data['date']).to_string())


    def calculate_plots(self):
        None


    def display(self, i):
        self.ui.stackedWidget.setCurrentIndex(i)



app = qtw.QApplication([])
general_window = Application()
general_window.show()

app.exec_()
