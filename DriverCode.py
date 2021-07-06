import cv2
import smtplib
import sys
import os
import time
import json

from datetime import datetime
import pyrebase

import JumpWayMQTT.Device as JWMQTTdevice
from TASSCore import TassCore

TassCore = TassCore()
config = {
  "apiKey": "XUEBQNb50Ap3IrBFg7vjuwdgjobdg0uvuD5RouOt",
  "authDomain": "pibase-4de10.firebaseapp.com",
  "databaseURL": "https://pibase-4de10-default-rtdb.firebaseio.com",
  "storageBucket": "pibase-4de10.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
class TASS():

	def __init__(self):

		self.jumpwayClient = ""
		self.configs = {}
		self.train = 0
		self.rec_counting = 0
		self.not_rec_counting = 0

		with open('required/config.json') as configs:
			self.configs = json.loads(configs.read())

		self.startMQTT()

		print("LOADING VIDEO CAMERA")

		self.OpenCVCapture = cv2.VideoCapture(0)
		#self.OpenCVCapture = cv2.VideoCapture('http://'+self.configs["StreamSettings"]["streamIP"]+':'+self.configs["StreamSettings"]["streamPort"]+'/stream.mjpg')

		#self.OpenCVCapture.set(5, 30)
		#self.OpenCVCapture.set(3,640)
		#self.OpenCVCapture.set(4,480)

	def deviceCommandsCallback(self,topic,payload):

		print("Received command data: %s" % (payload))
		newSettings = json.loads(payload.decode("utf-8"))

	def startMQTT(self):

		try:
			
			self.jumpwayClient = JWMQTTdevice.DeviceConnection({
				"locationID": self.configs["IoTJumpWay"]["Location"],
				"zoneID": self.configs["IoTJumpWay"]["Zone"],
				"deviceId": self.configs["IoTJumpWay"]["Device"],
				"deviceName": self.configs["IoTJumpWay"]["DeviceName"],
				"username": self.configs["IoTJumpWayMQTT"]["MQTTUsername"],
				"password": self.configs["IoTJumpWayMQTT"]["MQTTPassword"]
			})

		except Exception as e:
			print(str(e))
			sys.exit()

		

TASS = TASS()
model = cv2.face.createEigenFaceRecognizer(threshold=TASS.configs["ClassifierSettings"]["predictionThreshold"])
model.load(TASS.configs["ClassifierSettings"]["Model"])
print("LOADED STREAM & MODEL")
while True:

	if(TASS.train==1):

		print("TRAINING MODE")
		TassCore.processTrainingData()
		TassCore.trainModel()
		TASS.train=0

	elif(TASS.configs["AppSettings"]["armed"]==1):

		try:

			ret, frame = TASS.OpenCVCapture.read()
			if not ret: continue

			currentImage,detected = TassCore.captureAndDetect(frame)
			if detected is None:
				continue

			image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			x, y, w, h = detected
			crop = TassCore.resize(TassCore.crop(image, x, y, w, h))
			label,confidence = model.predict(crop)

			if label:
				TASS.rec_counting = TASS.rec_counting + 1
				if label == 9: 
					label = "Sayeed"
				print("Person is recognized...Name is:  " + str(label) + " Confidence " +str(confidence))
				print(TASS.rec_counting)
				if TASS.rec_counting == 3:
					now = datetime.now()
					timestamp = datetime.timestamp(now)
					tym = now.strftime("%d-%b-%Y (%H:%M:%S)")
					image_name = "d_face.jpg"
					cv2.imwrite(image_name,image)
					path_cloud = "images/" + tym
					storage.child(path_cloud).put(image_name)
					url = storage.child(path_cloud).get_url(None)
					data = {
					"date": "Time: " + tym,
					"message": "Alert: Person named " + label + " has entered in Camera 1",
					"url": url
					}
					db.child("Activity").push(data)

			else:
				TASS.not_rec_counting = TASS.not_rec_counting + 1
				print("Person not recognised " + str(label) + " Confidence "+str(confidence));
				if TASS.not_rec_counting == 3: 
					now = datetime.now()
					timestamp = datetime.timestamp(now)
					tym = now.strftime("%d-%b-%Y (%H:%M:%S)")
					image_name = "d_face.jpg"
					cv2.imwrite(image_name,image)
					path_cloud = "images/" + tym
					storage.child(path_cloud).put(image_name)
					url = storage.child(path_cloud).get_url(None)
					data = {
					"date": "Time: " + tym,
					"message": "An unrecognized person has entered in Camera 1",
					"url": url
					}
					db.child("Activity").push(data)

					server = smtplib.SMTP('smtp.gmail.com',587)
					server.starttls()
					server.login("rudro.sakafi@gmail.com","rudrosakafi12")
					msg="An unknown person is detected"
					server.sendmail("SpiderCam System","rudro.sakafi@gmail.com",msg)
					server.quit()


			time.sleep(4)

		except cv2.error as e:
			print(e)

TASS.OpenCVCapture.release()
cv2.destroyAllWindows()
