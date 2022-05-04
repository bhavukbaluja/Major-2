import cv2
import numpy as np
import glob
import pickle
import random

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def transform_image(img, threshold):

    retval, threshold = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
    close = closing

    open_close = cv2.bitwise_or(opening, closing, mask = None)

    return open_close, opening, close

imgs = []
label = 0
final_output = []
lables = []
eye_detected_imgs = []
iris_eye_detected_imgs = []

for filepath in glob.iglob('UBIRIS_200_150/Sessao_1/*'):
    
    num_in_folder = 0

    for filefilepath in glob.iglob(filepath+'/*'):
        if filefilepath[-1] == 'g':

            img = cv2.imread(filefilepath)
            imgs_colored = cv2.imread(filefilepath)
            img = cv2.resize(img,(200,150))

            img = cv2.cvtColor(img,	cv2.COLOR_BGR2GRAY)
            imgs.append([img,num_in_folder,label,imgs_colored])
            num_in_folder = num_in_folder+1
    label = label+1


eyes_num = 0
for i, j, L, c in imgs:

    i = cv2.resize(i, (400, 400))
    eyes = eye_cascade.detectMultiScale(i, 1.01, 0)
    if len(eyes) > 1:
        print(eyes_num)
        eye_detected_imgs.append(imgs[eyes_num])
        eyes_num = eyes_num+1
        maximum_area = -3

        for (ex, ey, ew, eh) in eyes:
            area = ew*eh
            if area > maximum_area:
                maximum_area = area
                maximum_width = ew
                point_x = ex
                point_y = ey
                maximum_height = eh

print("total_eyes_found = ", eyes_num)
print("total images number ", len(imgs))

iris_num = 0
for i, j, L, c in eye_detected_imgs:

    circles = cv2.HoughCircles(i, cv2.HOUGH_GRADIENT, 10, 100)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        maximum_average = 10000000000000
        key = True

        for(x, y, r) in circles:

            if x+r <= max(i.shape) and y+r <= max(i.shape) and x-r > 0 and y-r > 0 and r > 20:
                key = False
                new_roi = i[y-r:y+r, x-r:x+r]
                average = np.average(new_roi)

                if average < maximum_average:
                    maximum_r = r
                    point_x = x
                    point_y = y
                    maximum_average = average

        if key:
            #print("key opened")
            for (x, y, r) in circles:
                    maximum_radius = -4
                    if r > maximum_radius:
                        maximum_r = r
                        point_x = x
                        point_y = y
                        maximum_average = average

        cv2.imwrite('paper/iris/'+str(L)+'.'+str(j)+'.jpg', c)
        iris_eye_detected_imgs.append(eye_detected_imgs[iris_num])
        iris_num = iris_num+1

print("total_iris_found = ", iris_num)
print("total images number ", len(imgs))

imgs = iris_eye_detected_imgs
kernel = np.ones((5, 5), np.uint8)
random.shuffle(imgs)
test = []
for i, j, L, c in imgs:
    gold, silver, diamond = transform_image(i, 0)
    golden_reference = sum(sum(gold))

    for k in range(10, 1000, 10):
        working_img, opening, closing = transform_image(i, k)
        suming = sum(sum(working_img))
        difference = suming-golden_reference
        if difference > 800:
            print("the image threshold = ", k)
            print("the image name " + str(j))
            print(" ")

            cv2.imwrite('paper/threshold/'+str(L)+'.'+str(j)+'.jpg', working_img)
            cv2.imwrite('paper/opening/'+str(L)+'.'+str(j)+'.jpg', opening)
            cv2.imwrite('paper/closing/'+str(L)+'.'+str(j)+'.jpg', closing)

            contours = cv2.findContours(working_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for z in contours:
                x, y, w, h = cv2.boundingRect(z)
                if x+w < 150 and y+h < 200 and x-w//4 > 0:
                    
                    cv2.rectangle(working_img,(x,y),(x+w,y+h),(0,255,0),-2)
                    cv2.imwrite('paper/contour/'+str(L)+'.'+str(j)+'.jpg',working_img)

                contours = cv2.findContours(working_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            maximum_area = 0
            maximum_area = 0
            maximum_width = 0
            point_x = 0
            point_y = 0
            maximum_height = 0
            for z in contours:
                #print(len(i))
                x, y, w, h = cv2.boundingRect(z)
                new_area = h*w
                if x+w < 150 and y+h < 200 and new_area > maximum_area and x-w//4>0:
                    maximum_area = new_area
                    maximum_width = w
                    point_x = x
                    point_y = y
                    maximum_height = h

            center_x = point_x+maximum_width//2
            center_y = point_y+maximum_height//2
            radius = 40

            if (center_y-radius > 0 and center_x-radius > 0 and center_y+radius < 200 and center_x+radius < 150):
                new_roi = c[center_y-radius:center_y+radius, center_x-radius:center_x+radius]
                new_roi = cv2.resize(new_roi, (200, 150))
                cv2.imwrite('final_iris2/'+str(L)+'.'+str(j)+'.jpg', new_roi)

            else:
                center_y = c.shape[0]//2
                center_x = c.shape[1]//2
                new_roi = c[center_y-radius:center_y+radius, center_x-radius:center_x+radius]
                new_roi = cv2.resize(new_roi, (200, 150))
                cv2.imwrite('final_iris2/'+str(L)+'.'+str(j)+'.jpg',new_roi)

            cv2.imwrite('edging_5/'+str(L)+'_'+str(j)+'.jpg', i)
            test.append(i)
            final_output.append(new_roi)
            lables.append(L)
            break

print("the lenght of final output = ",len(final_output))
print("the of lables = ",len(lables))

final_output=np.array(final_output)
print(final_output.shape)

test=np.array(test)
print(test.shape)

pickle_out = open("test_ubiris.pickle","wb")
pickle.dump(test, pickle_out)
pickle_out.close()

pickle_out = open("ubiris_features.pickle","wb")
pickle.dump(final_output, pickle_out)
pickle_out.close()

pickle_out = open("ubiris_lables.pickle","wb")
pickle.dump(lables, pickle_out)
pickle_out.close()         

