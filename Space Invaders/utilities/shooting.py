from time import sleep

from PyQt5.QtCore import pyqtSignal, QObject, QThread, pyqtSlot
from PyQt5.QtWidgets import QLabel


class ShootBullet(QObject):
    updated_position = pyqtSignal(QLabel, int, int)
    collision_detected = pyqtSignal(QLabel, QLabel)

    def __init__(self):
        super().__init__()

        self.threadWorking = True
        self.bullets = []
        self.aliens = []

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.__work__)

    def start(self):
        self.thread.start()

    def add_bullet(self, bullet: QLabel):
        self.bullets.append(bullet)

    def add_alien(self, alien: QLabel):
        self.aliens.append(alien)

    def remove_alien(self, alien:QLabel):
        self.aliens.remove(alien)

    def remove_bullet(self, bullet: QLabel):
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def die(self):
        self.threadWorking = False
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        while self.threadWorking:

            for bullet in self.bullets:
                bulletGeo = bullet.geometry()
                bullet_x = bulletGeo.x()
                bullet_y = bulletGeo.y() - 5
                self.updated_position.emit(bullet, bullet_x, bullet_y)

            sleep(0.01)
