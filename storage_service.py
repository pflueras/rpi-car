from threading import Thread
from functools import wraps
import time
import flask

from car.car import Car
from storage.storage_scan import StorageScan
from storage.storage_object import StorageObject

class StorageService:
    def __init__(self, publish_distances_func):
        self.publish_distances_func = publish_distances_func
        self.scan_interval = 0.25
        # self.car = Car(6, 13, 19, 26, 21, 20, 16, 12,
        #       14, 15, 18, 17, 2, 3)
        self.car = Car(13, 6, 26, 19, 20, 21, 12, 16,
                       14, 15, 18, 17, 2, 3)

        self.car_running = False

    def _scan_storage_worker(self):
        storage_scan = StorageScan(210, 50, self.scan_interval)

        while self.car_running:
            dists = self.car.read_distances()
            storage_scan.add_dists((dists[0], dists[1], dists[2]))

            self.publish_distances_func(dists[0], dists[1], dists[2])

            # print("Front = %.2f cm, side = %.2f cm, back %.2f cm, emergency stop: %r" % dists)
            if dists[3] or dists[4]:
                self.car.stop()
                break

            time.sleep(self.scan_interval)

        objects = storage_scan.collect_objects()
        print('Number of scans: ' + str(storage_scan.no_scan_dists()) + '; number of objects: ' + str(len(objects)))
        for obj in objects:
            print('Start index: ' + str(obj.start_index) + '; end index: ' + str(obj.end_index))

    def scan_storage(self):
        dists = self.car.read_distances()
        if dists[3] or dists[4]:
            print('Too close to objects. Car not moving forward!')
            return

        self.car_running = True
        self.car.move_forward()

        #eventlet.spawn(self.read_dists_worker)
        self._scan_storage_worker()

    def move_car_bwd(self):
        self.car.move_backward()

    def stop_car(self):
        self.car_running = False
        self.car.stop()