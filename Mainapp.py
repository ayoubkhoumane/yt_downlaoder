
#import libraries
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType

import urllib.request
import pafy
import humanize
import os
from os import path
from pytube import Playlist


# create a simple app : download a file

# 1 add essential codes : links app with ui + launch app
ui,_ = loadUiType('main.ui')

class MainApp(QMainWindow ,ui):
    def __init__(self , parent=None):
        super(MainApp , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.Handle_UI()

# to do modification in ui
    def Handle_UI(self):
        self.progressBar.setValue(0)
    # @staticmethod
    # def func2(total, recvd, ratio, rate, eta):
    #     print(round(ratio*100))

    def Handle_Buttons(self):


        self.Button_search_1.clicked.connect(self.Search_Youtube_video)
        self.Button_search_2.clicked.connect(self.Handle_Search_playlist)

        self.Button_download_1.clicked.connect(self.Download_file)
        self.Button_download_5.clicked.connect(self.Download_Youtube_video)
        self.Button_download_6.clicked.connect(self.Download_Youtube_playlist)


        self.Button_browse_5.clicked.connect(self.Handle_Browse_2)
        self.Button_browse_6.clicked.connect(self.Handle_Browse_2)
        self.Button_browse_1.clicked.connect(self.Handle_Browse)






#####TAB 1
    def Handle_Browse(self):
        save_place=QFileDialog.getSaveFileName(self,caption="Save as",directory="/.",filter="All Files *.*")
        self.case_location_2.setText(save_place[0])



    def Handle_Progress(self,numberpacks,sizepacks,totalsize):
        value=numberpacks*sizepacks
        if totalsize>0 : 
            percent = value *100//totalsize
            self.progressBar.setValue(percent)



    def Download_file(self): # url - location - progress
        url=self.case_location_1.text()
        save_loc=self.case_location_2.text()

        try :
          urllib.request.urlretrieve(url,save_loc,self.Handle_Progress)
          QApplication.processEvents()
          QMessageBox.information(self, "Download finished", "File downloaded")
        except:
            QMessageBox.warning(self, "Download Failed", "Problem when downloading file")

        self.progressBar.setValue(0)


#####TAB 2
    def Search_Youtube_video(self): # url - location - progress - quality
        url=self.case_location_9.text()
        video=pafy.new(url)
        st=video.videostreams
        for s in st :
            size=humanize.naturalsize(s.get_filesize())
            data= '{} {} {}' .format(s.extension,s.quality,size)
            self.comboBox.addItem(data)


    def Download_Youtube_video(self):
        url=self.case_location_9.text()
        video=pafy.new(url)
        save_loc=self.case_location_10.text()
        quality=self.comboBox.currentIndex()
        try :
            st = video.videostreams
            down=st[quality].download(filepath=save_loc, quiet=True, callback=self.Handle_Progress_2)
            QApplication.processEvents()

            QMessageBox.information(self, "Download finished", "Youtube video downloaded")

        except:
            QMessageBox.warning(self, "Download Failed", "Problem when downloading Youtube video")

        self.progressBar_5.setValue(0)


    def Handle_Browse_2(self):
        save_place=QFileDialog.getExistingDirectory(self,caption="Select Directory",directory="/.")
        self.case_location_9.setText(save_place)
        self.case_location_12.setText(save_place)
        
    def Handle_Progress_2(self,total, recvd, ratio, rate, eta):
     if total>0 :
        percent = round(ratio*100)
        self.progressBar_5.setValue(percent)



##### TAB 3

    # def Handle_Browse_2(self):
    #     save_place=QFileDialog.getExistingDirectory(self,caption="Select Directory",directory="/.")
    #     self.case_location_10.setText(save_place)


    def Handle_Search_playlist(self): #search quality
        url_playlist = self.case_location_11.text()
        plist = Playlist(url_playlist)
        self.comboBox_2.addItem(f"High Quality : {plist.title}")


    def Download_Youtube_playlist(self):
      url_playlist = self.case_location_11.text()
      plist = Playlist(url_playlist)
      total=len(plist)
      print(total)
      name=plist.title
      save_loc=self.case_location_12.text()

      path_playlist=os.path.join(save_loc,name)

      save_loc=self.case_location_12.text()
      if os.path.exists(path_playlist)==False : os.mkdir(path_playlist) 


      for url in plist.video_urls:
        num_video=0
        try :
            video=pafy.new(url)
            video_qual=video.getbestvideo(preftype="mp4")
            video_qual.download(filepath=path_playlist)
            QApplication.processEvents()
            if num_video>0 :
                percent=num_video*100//total
                self.progressBar_6.setValue(percent)
                QApplication.processEvents()

                print(percent)


        except:
            pass
        num_video+=1
        print(num_video)
      QMessageBox.warning(self, "Download finished", "Youtube Playlist downloaded")



        ############# HANDLE OTHERS ########
    def Handle_Menu_exit(self): # url - location - progress
        pass







################################ Main App ###################################
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
