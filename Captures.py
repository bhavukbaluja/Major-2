# import iris_extraction_for1

def cap(username):

    import cv2
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Capture Image")
    print("Hit Space button to capture the image")
    print("Hit ESC button to close the camera window")
    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("Capture Image", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "SignupPics/"+username+".jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
            # iris_extraction_for1.func1(username)

    cam.release()

    cv2.destroyAllWindows()