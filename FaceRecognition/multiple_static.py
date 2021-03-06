
print("[INFO] Importing Libraries...")
# from imutils.video import VideoStream
# from imutils.video import FPS
import face_recognition
# import argparse
import imutils
import pickle
import time
import cv2

import os


# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection

def extract_names(list_names):
    found = []
    for Name in list_names:
        if Name != 'Unknown':
            found.append(Name)

    if len(found) == 0:
        return 'No known Faces found'
    else:
        return ', '.join(found)


def generate_paths(store_path):

    # get all files of the directory where the pictures are saved
    # opti
    #  if there are other image file types change the code to the other types or even
    #  that it checks for multiple file types
    onlyfiles = [file for file in os.listdir(store_path) if os.path.isfile(os.path.join(store_path, file))]
    # get only the files that are jpgs
    paths = list(filter(lambda x: x[-3:] == 'jpg', onlyfiles))
    # rejoin the names with the main paths to have the full path
    paths = list(map(lambda x: store_path + x, [path for path in paths]))
    return paths


def analyse_pics(pictures, view=False):
    # typetesting
    if isinstance(pictures, list):
        pass
    else:
        print('pictures needs to be a list of strings(path to pictures)')

    if isinstance(view, bool):
        pass
    else:
        print('view needs to be a boolean variable')

    # loop over the paths and get faces and identify found faces
    i = 1
    for path in pictures:
        print("[INFO] loading encodings + face detector...")
        data = pickle.loads(open('/home/pi/HomeBotRemote/FaceRecognition/encodings.pickle', "rb").read())
        detector = cv2.CascadeClassifier('/home/pi/HomeBotRemote/FaceRecognition/haarcascade_frontalface_default.xml')

        print('[INFO] path:', path)
        print("[INFO] processing image...")
        frame = cv2.imread(path)
        frame = imutils.resize(frame, width=500)

        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding, tolerance=0.4)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 0, 255), 1)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (255, 0, 0), 2)

        print('[INFO] Faces found Picture' + str(i) + ':', str(len(names)))
        print('[INFO] Known Faces in Picture' + str(i) + ':', extract_names(names))
        if view:
            print("[INFO] View image...")
            while True:
                cv2.imshow("Frames", frame)
                key = cv2.waitKey(1) & 0xFF

                if key == ord("q"):
                    break
            print("[INFO] Press Q to continue")
            print("[INFO] Image closed, see next")
        i += 1
    if view:
        print('[INFO] Last Image closed')


# tyt = ['/home/pi/HomeBotRemote/FaceRecognition/StoredPics/testpic3.jpg',
#        '/home/pi/HomeBotRemote/FaceRecognition/StoredPics/testpic.jpg']
pathss = generate_paths(store_path='/home/pi/HomeBotRemote/FaceRecognition/StoredPics/')
analyse_pics(pathss, view=False)
