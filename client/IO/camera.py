import cv2

class Camera:

	# Class constructor.
	# out: Name of output file. Is automatically given a ".avi" extension.
	# fps: Framerate of video. Currently not acting as would be expected.
	# Increasing or decreasing its value seems to result in a sped up or slowed
	# down video. A value of 8.0 gives me a video that's approximately
	# real-time, but I suspect this differs depending on the camera being used.
	# size: Video dimensions. Also defines the size of the frame shown during
	# recording.
	def __init__(self, out="output", fps=8.0, size=(640,480)):
		self.out_file=out+".avi"
		self.framerate=fps
		self.framesize=size
		self.fourcc = cv2.cv.CV_FOURCC('M','J','P','G')

	# Records a video, displays it in a frame and saves it to a file in the same
	# directory. Recording can be stopped by pressing the 'q' key. The name of
	# the file created is defined in self.out_file.
	# Issue: Framerate doesn't act as you would expect.
	def record(self):
		# Used to write to an output file with the given specifications
		out = cv2.VideoWriter(self.out_file, self.fourcc, self.framerate, self.framesize)
		# Attaches to and receives input from a connected camera
		cap = cv2.VideoCapture(0)

		try:
			# Receive and save input from cap, one frame at a time
			while(cap.isOpened()):
				# ret: return value from read(). True if read() was successful
				# frame: image captured from cap
				ret, frame = cap.read() # Capture a frame from the camera

				if ret:
					out.write(frame) # Write frame to output file
					cv2.imshow('frame',frame) # Show frame on-screen

					# Check for 'q' keypress. If detected, exit the while loop.
					# Value returned by cv2.waitKey(1) must be truncated to 8
					# bits for comparison.
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
				else:
					break
		# Intended to be for cases where no camera is found. Very barebones.
		except cv2.error:
			print ("Error: No camera found")

		cap.release()
		out.release()
		cv2.destroyAllWindows()

if __name__ == "__main__":
	camera=Camera()
	camera.record()
