import cv2
import pytesseract
import re
import json

im = cv2.imread('sample.jpeg')
config = '-l eng+equ --oem 1 --psm 4'
gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


threshold_img = cv2.threshold(gray_image, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]

text = pytesseract.image_to_string(threshold_img, config=config)
text = text.split('\n')
year = []
question = ''
questions = []
for lines in text:
    # print(lines)
    words = lines.split()
    res = len(words)
    if res > 5:         # for a question the number of words in the sentence greater than 5 and starting with a digit assumed as question
        if words[0].isdigit() or words[0][0].isdigit():
            question = lines
            questions.append(lines)
    # print(words)
for lines in text:
    words = lines.split()
    if 'JEE' in words:     # to get the year of exam using regex
        year.append(re.findall(r'\d+', words[words.index('JEE') + 1]))

# print(question)
# print(year)
years = []
for y in year:
    years.append(y[0])


jsonlist=[]
datalist=[]

for i in range(len(questions)):
    data={}
    data['Question'] = questions[i]
    data['Exam']=years[i]
    datalist.append(data)
    i=i+1
jsondata = json.dumps(datalist, indent=4)

print(jsondata)
with open('finaloutput.txt', 'w') as outfile:
    json.dump(datalist,outfile,indent=4)