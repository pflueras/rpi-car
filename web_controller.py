import json

from flask import render_template
from flask_socketio import emit
from storage_service import StorageService

class WebController:
    def __init__(self):
        self.storage_service = StorageService(self.publish_distances, self.publish_position,
                                              self.publish_storage_objects)

    def index(self):
        return render_template('index.html')

    def scan_storage(self, message):
        self.storage_service.scan_storage()

    def backward_car(self, message):
        self.storage_service.move_car_bwd()

    def stop_car(self, message):
        self.storage_service.stop_car()

    def publish_distances(self, front_dist, side_dist, back_dist):
        emit('car_distances', {'front': front_dist, 'side': side_dist, 'back': back_dist})

    def publish_position(self, car_location):
        emit('car_position', {'car_position': car_location})

    def publish_storage_objects(self, storage_objects):
        json_objects = []
        for storage_object in storage_objects:
            json_objects.append({'start_position': storage_object.start_position, 'end_position': storage_object.end_position})
        emit('storage_objects', {'storage_objects': json.dumps(json_objects)})