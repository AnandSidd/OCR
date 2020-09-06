import cv2
import numpy as np
import pytesseract

config = '-l eng+equ --oem 1 --psm 6'
# Load image, grayscale, Otsu's threshold
image = cv2.imread('sample.jpeg')
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Dilate with horizontal kernel
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 50))
kernel2 = np.ones((7, 7), np.uint8)
dilate = cv2.dilate(thresh, kernel, iterations=2)
cv2.imshow('dilate', dilate)


cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
print(len(cnts))
height = []
for c in cnts:
    area = cv2.contourArea(c)
    if area < 5000:
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(c)
        height.append(y)
print(height)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


for i in range(len(height)):
    if i == 0:
        crop = original[height[i]:original.shape[0], 0:original.shape[1]]
        text = pytesseract.image_to_string(crop, config=config)
        year = find_between(text, "[","]")
        ques_num = text[text.index('. ') - 1]
        print(ques_num + " " + year)
        cv2.imshow("Question" + ques_num + " " + year, crop)
        cv2.imwrite("Question" + ques_num + " " + year + ".jpg", crop)

        cv2.waitKey(0)
    elif i != 0:
        crop = original[height[i]:height[i - 1], 0:original.shape[1]]
        text = pytesseract.image_to_string(crop, config=config)
        ques_num = text[text.index('. ') - 1]
        year = find_between(text, "[","]")
        print(ques_num + " " + year)
        cv2.imshow("Question " + ques_num + " " + year, crop)
        cv2.imwrite("Question" + ques_num + " " + year + ".jpg", crop)
        cv2.waitKey(0)

