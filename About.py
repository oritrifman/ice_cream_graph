from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap

class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About Me')
        self.setGeometry(100, 100, 340, 490) 

        self.my_name = QLabel('Ori Trifman', self)
        self.my_name.setGeometry(20, 20, 300, 30)

        self.my_picture = QLabel(self)
        self.my_picture.setGeometry(20, 60, 300, 300)

        image = QPixmap('ori_photo.jpg').scaled(300, 300)
        self.my_picture.setPixmap(image)

        self.my_email = QLabel('Email: oritrifman@gmail.com', self)
        self.my_email.setGeometry(20, 370, 300, 30)

        self.my_linkedin = QLabel('<a href="https://www.linkedin.com/in/ori-trifman-7333b2233">My LinkedIn Profile</a>', self)
        self.my_linkedin.setGeometry(20, 400, 300, 30)
        self.my_linkedin.setOpenExternalLinks(True) 

        self.my_github = QLabel('<a href="https://github.com/oritrifman/ice_cream_graph">My GitHub Repository</a>', self)
        self.my_github.setGeometry(20, 430, 300, 30)
        self.my_github.setOpenExternalLinks(True)      
