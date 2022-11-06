import json
import os 
import sys 
import cv2



pre_dir = './'

label_dir = pre_dir +'labels/'
image_dir = pre_dir +'images/'


new_schema = dict()            
images = []

annotations = []
cnt = 0
for json_ in os.listdir(label_dir):

    label_dir_json = label_dir + json_
            
    print(label_dir_json)
    image_dir = label_dir_json.replace('.json','.png')
    image_dir = image_dir.replace('labels','images')
    #print(image_dir)
    
    with open(label_dir_json, "r") as json_file:
        img = cv2.imread(image_dir, cv2.IMREAD_COLOR)
        h , w, c = img.shape
        
        img_name = json_.replace('.json','.png')
        
        json_dict = json.load(json_file)
        image = dict()
        image['file_name'] = img_name
        image['height'] = h
        image['id'] = json_dict['id']
        image['width'] = w
        
        

        for data in json_dict['segments']:
            #print(data)
            if data["type_detail"] != '수식':
                continue
            #print(data)
            cnt +=1
            annotation = dict()
            min_x = 9999 
            min_y = 9999
            max_x = 0 
            max_y = 0
            anno = []
            for b in data['box']:
                min_x = min(min_x,b[0])
                min_y = min(min_y,b[1])
                max_x = max(max_x,b[0])
                max_y = max(max_y,b[1])
                anno.extend(b)
            gap_x , gap_y  = max_x-min_x , max_y-min_y

            #print(gap_x,gap_y)
            #box = [min(data['box'])]
            annotation['area'] = float(gap_x * gap_y)
            annotation['bbox'] = [min_x,min_y,gap_x,gap_y]
            annotation['category_id'] = 1
            cnt +=1
            annotation['id'] = cnt
            annotation['image_id'] = json_dict['id']
            annotation['iscrowd'] = 0 
            annotation['segmentation'] = [anno]
            annotations.append(annotation)
            images.append(image)

        
            
                #print(json_dict['segments'])

    

categories = [
        
        {
            "id" : 1,
            "name" : "text",
            "supercategory" : "text"
        },
        
        {
            "id" : 2,
            "name" : "0",
            "supercategory" : "text"
        },
        
        {
            "id" : 3,
            "name" : "1",
            "supercategory" : "text"
        },
        
        {
            "id" : 4,
            "name" : "2",
            "supercategory" : "text"
        },
        
        {
            "id" : 5,
            "name" : "3",
            "supercategory" : "text"
        },
        
        {
            "id" : 6,
            "name" : "4",
            "supercategory" : "text"
        },
        
        {
            "id" : 7,
            "name" : "5",
            "supercategory" : "text"
        },
        
        {
            "id" : 8,
            "name" : "6",
            "supercategory" : "text"
        },
        
        {
            "id" : 9,
            "name" : "7",
            "supercategory" : "text"
        },
        
        {
            "id" : 10,
            "name" : "8",
            "supercategory" : "text"
        },
        
        {
            "id" : 11,
            "name" : "9",
            "supercategory" : "text"
        },
        
        {
            "id" : 12,
            "name" : "A",
            "supercategory" : "text"
        },
        
        {
            "id" : 13,
            "name" : "B",
            "supercategory" : "text"
        },
        
        {
            "id" : 14,
            "name" : "C",
            "supercategory" : "text"
        },
        
        {
            "id" : 15,
            "name" : "D",
            "supercategory" : "text"
        },
        
        {
            "id" : 16,
            "name" : "E",
            "supercategory" : "text"
        },
        
        {
            "id" : 17,
            "name" : "F",
            "supercategory" : "text"
        },
        
        {
            "id" : 18,
            "name" : "G",
            "supercategory" : "text"
        },
        
        {
            "id" : 19,
            "name" : "H",
            "supercategory" : "text"
        },
        
        {
            "id" : 20,
            "name" : "I",
            "supercategory" : "text"
        },
        
        {
            "id" : 21,
            "name" : "J",
            "supercategory" : "text"
        },
        
        {
            "id" : 22,
            "name" : "K",
            "supercategory" : "text"
        },
        
        {
            "id" : 23,
            "name" : "L",
            "supercategory" : "text"
        },
        
        {
            "id" : 24,
            "name" : "M",
            "supercategory" : "text"
        },
        
        {
            "id" : 25,
            "name" : "N",
            "supercategory" : "text"
        },
        
        {
            "id" : 26,
            "name" : "O",
            "supercategory" : "text"
        },
        
        {
            "id" : 27,
            "name" : "P",
            "supercategory" : "text"
        },
        
        {
            "id" : 28,
            "name" : "Q",
            "supercategory" : "text"
        },
        
        {
            "id" : 29,
            "name" : "R",
            "supercategory" : "text"
        },
        
        {
            "id" : 30,
            "name" : "S",
            "supercategory" : "text"
        },
        
        {
            "id" : 31,
            "name" : "T",
            "supercategory" : "text"
        },
        
        {
            "id" : 32,
            "name" : "U",
            "supercategory" : "text"
        },
        
        {
            "id" : 33,
            "name" : "V",
            "supercategory" : "text"
        },
        
        {
            "id" : 34,
            "name" : "W",
            "supercategory" : "text"
        },
        
        {
            "id" : 35,
            "name" : "X",
            "supercategory" : "text"
        },
        
        {
            "id" : 36,
            "name" : "Y",
            "supercategory" : "text"
        },
        
        {
            "id" : 37,
            "name" : "Z",
            "supercategory" : "text"
        },
        
        {
            "id" : 38,
            "name" : "a",
            "supercategory" : "text"
        },
        
        {
            "id" : 39,
            "name" : "b",
            "supercategory" : "text"
        },
        
        {
            "id" : 40,
            "name" : "c",
            "supercategory" : "text"
        },
        
        {
            "id" : 41,
            "name" : "d",
            "supercategory" : "text"
        },
        
        {
            "id" : 42,
            "name" : "e",
            "supercategory" : "text"
        },
        
        {
            "id" : 43,
            "name" : "f",
            "supercategory" : "text"
        },
        
        {
            "id" : 44,
            "name" : "g",
            "supercategory" : "text"
        },
        
        {
            "id" : 45,
            "name" : "h",
            "supercategory" : "text"
        },
        
        {
            "id" : 46,
            "name" : "i",
            "supercategory" : "text"
        },
        
        {
            "id" : 47,
            "name" : "j",
            "supercategory" : "text"
        },
        
        {
            "id" : 48,
            "name" : "k",
            "supercategory" : "text"
        },
        
        {
            "id" : 49,
            "name" : "l",
            "supercategory" : "text"
        },
        
        {
            "id" : 50,
            "name" : "m",
            "supercategory" : "text"
        },
        
        {
            "id" : 51,
            "name" : "n",
            "supercategory" : "text"
        },
        
        {
            "id" : 52,
            "name" : "o",
            "supercategory" : "text"
        },
        
        {
            "id" : 53,
            "name" : "p",
            "supercategory" : "text"
        },
        
        {
            "id" : 54,
            "name" : "q",
            "supercategory" : "text"
        },
        
        {
            "id" : 55,
            "name" : "r",
            "supercategory" : "text"
        },
        
        {
            "id" : 56,
            "name" : "s",
            "supercategory" : "text"
        },
        
        {
            "id" : 57,
            "name" : "t",
            "supercategory" : "text"
        },
        
        {
            "id" : 58,
            "name" : "u",
            "supercategory" : "text"
        },
        
        {
            "id" : 59,
            "name" : "v",
            "supercategory" : "text"
        },
        
        {
            "id" : 60,
            "name" : "w",
            "supercategory" : "text"
        },
        
        {
            "id" : 61,
            "name" : "x",
            "supercategory" : "text"
        },
        
        {
            "id" : 62,
            "name" : "y",
            "supercategory" : "text"
        },
        
        {
            "id" : 63,
            "name" : "z",
            "supercategory" : "text"
        }
]

new_dic = {'images' : images , 'categories' : categories , 'annotations' : annotations}
f = open('train.json','w+')

f.write(str(new_dic).replace('\'','\"'))
f.close()