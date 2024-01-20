import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *
import sys 
""" import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras import layers, models """


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(785, 775)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setObjectName(u"centralLayout")

        self.groupBox_1 = QGroupBox(self.centralwidget)
        self.groupBox_1.setObjectName(u"groupBox_1")
        self.gridLayout_4 = QHBoxLayout(self.groupBox_1)
        self.pushButton_1 = QPushButton(self.groupBox_1)
        self.pushButton_1.setObjectName(u"pushButton_1")
        self.pushButton_1.setMaximumSize(QSize(250, 16777215))
        self.pushButton_1.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_1.clicked.connect(self.loadImage)  
        self.label_1 = QLabel(self.groupBox_1) 
        self.label_1.setObjectName(u"label_1") 

        self.gridLayout_4.addWidget(self.label_1)  
        self.gridLayout_4.addWidget(self.pushButton_1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_5 = QVBoxLayout(self.groupBox_2)
        self.graphicsView = QGraphicsView(self.groupBox_2)
        self.gridLayout_5.addWidget(self.graphicsView)

        self.groupBox_6 = QGroupBox(self.centralwidget)
        #### 추가코드 ↓
        self.groupBox_6.setMaximumHeight(250)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_9 = QVBoxLayout(self.groupBox_6)
        self.textEdit = QTextEdit(self.groupBox_6)
        self.gridLayout_9.addWidget(self.textEdit)

        self.centralLayout.addWidget(self.groupBox_1)
        self.centralLayout.addWidget(self.groupBox_2)
        self.centralLayout.addWidget(self.groupBox_6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 785, 26))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def loadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(None, "Open Image File", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)

        if file_name:
            try:
                # 이미지를 모델로 전달하고 진단 결과를 얻는 함수 호출
                diagnosis_result = self.diagnosePneumonia(file_name)

                # 결과를 TextEdit에 출력
                self.textEdit.setPlainText(diagnosis_result)

                # 이미지를 QGraphicsView에 출력
                pixmap = QPixmap(file_name)
                pixmap = pixmap.scaledToHeight(530)
                self.graphicsView.setScene(QGraphicsScene())
                self.graphicsView.scene().addPixmap(pixmap)
                self.graphicsView.setSceneRect(pixmap.rect())
            except Exception as e:
                # 이미지 읽기 중 오류가 발생한 경우 오류 메시지를 출력
                self.textEdit.setPlainText("이미지를 읽을 수 없습니다. 오류: " + str(e))
            
    def diagnosePneumonia(self, image_path):
        # 모델 로드
        model = load_model(r"C:\diagnose_pneumonia\diagnose_resnet_model.h5")

        # 이미지 로드 및 전처리
        image_width, image_height = 224, 224  # 이미지 크기 조정
        image = cv2.imread(image_path)
        image = cv2.resize(image, (image_width, image_height))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)  # 배치 차원 추가

        # 모델을 사용하여 이미지 진단
        prediction = model.predict(image)

        # 결과 해석
        confidence = prediction[0][0]  # 진단의 정확도 값 (0 ~ 1)
        diagnosis_result = "폐렴 진단 결과: "
        if confidence > 0.5:
            diagnosis_result += f"정상입니다(폐렴X). (정확도: {confidence:.2%})"
        else:
            diagnosis_result += f"폐렴이 진단되었습니다. (정확도: {100-confidence:.2f}%)"

        return diagnosis_result


    def displayImage(self, image_path):
        pixmap = QPixmap(image_path)

        scene = QGraphicsScene()
        scene.addPixmap(pixmap)

        self.graphicsView.setScene(scene)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_1.setTitle("")
        self.pushButton_1.setText(QCoreApplication.translate("MainWindow", u"Attach File 1", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"Attach File", None))  # Add this line
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"DATA", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"RESULT", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Gulim'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin_bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\uacb0\uacfc\ucd9c\ub825</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin_top:0px; margin_bottom:0px; margin_left:0px; margin_right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\ud3d0\ub834\uc9c4\ub2e8", None))


if __name__ == "__main__":
    app = QApplication([])  
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    centralLayout = QVBoxLayout()
    centralWidget = QWidget()
    centralWidget.setLayout(centralLayout)
    centralLayout.addWidget(MainWindow.centralWidget())
    MainWindow.setCentralWidget(centralWidget)

    MainWindow.showMaximized()
    sys.exit(app.exec_())
