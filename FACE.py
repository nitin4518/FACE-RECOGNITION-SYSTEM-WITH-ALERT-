def Face_recog_code():
    import cv2
    from mtcnn import MTCNN
    from yolov5 import YOLOv5
    import face_recognition as FACE  
    import numpy as np
    import warnings
    from twilio.rest import Client
    import json

    # Your Twilio account SID and Auth Token
    account_sid = 'TWILIO_SID'  # Replace with your Account SID
    auth_token = 'TWILIO_AUTH_TOKEN'    # Replace with your Auth Token

    client = Client(account_sid, auth_token)
    warnings.filterwarnings("ignore")

    # Initialize detectors
    mtcnn_detector = MTCNN()
    yolo_detector = YOLOv5('yolov5s.pt')  # Load the YOLOv5 model

    # Load known face encodings and names
    known_face_encodings = []  # List to hold face encodings
    known_face_names = []      # List to hold names corresponding to the encodings
    mess= ""

    # Example: Load a known face

    image_path = "E:\\Camera\\IMG.jpg"  # Use double backslashes

    # Load an image file and learn how to recognize it.
    image_of_person = FACE.load_image_file(image_path)  # Use double backslashes
    face_encoding = FACE.face_encodings(image_of_person)[0]

    # Add the encoding and name to the lists
    known_face_encodings.append(face_encoding)
    known_face_names.append("criminal_name")

    # Start video capture
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize the frame to the expected input size for YOLOv5
        frame_resized = cv2.resize(frame, (640, 640))
        results = yolo_detector.predict(frame_resized)

        # For each detected person, apply MTCNN for face detection
        for detection in results.xyxy[0]:  # Get detections
            x1, y1, x2, y2, conf, cls = detection  # Unpack detection
            if cls == 0:  # Assuming class 0 is 'person'
                person_frame = frame[int(y1):int(y2), int(x1):int(x2)]
                faces = mtcnn_detector.detect_faces(person_frame)

                # Draw bounding boxes for detected faces and recognize them
                for face in faces:
                    x_face, y_face, w_face, h_face = face['box']
                    face_image = person_frame[int(y_face):int(y_face + h_face), int(x_face):int(x_face + w_face)]
                    
                    # Convert the face image from BGR to RGB
                    rgb_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

                    # Find face encodings for the detected face
                    face_encodings = FACE.face_encodings(rgb_face)

                    if face_encodings:  # If a face encoding was found
                        face_encoding = face_encodings[0]
                        # Compare with known faces
                        matches = FACE.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"

                        # Use the known face with the smallest distance to the new face
                        face_distances = FACE.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)

                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]

                        # Draw bounding box and label
                        cv2.rectangle(frame, (int(x1 + x_face), int(y1 + y_face)), 
                                    (int(x1 + x_face + w_face), int(y1 + y_face + h_face)), 
                                    (0, 255, 0), 2)
                        # Sending the SMS
                        link_to_send = "https://tidy-actor.surge.sh"

                        message = client.messages.create(
                            body=f"Open this link Quickly : {link_to_send}",
                            from_='twilio_no',  # Replace with your Twilio number
                            to='receiver_no'      # Replace with the recipient's phone number
                        )
                        
                        print(f"Message sent with SID: {message.sid}")  # Print the unique Message SID
                        mess=message.sid
                        cv2.putText(frame, name, (int(x1 + x_face), int(y1 + y_face - 10)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        exit()

        # Display the resulting frame
        cv2.imshow('Real-time Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    result = "Message sent with SID: {mess}"
    # You can return any data you want, such as a string, list, or dictionary
    return result
