import json
import os 
import sys 
import cv2
import shutil
import numpy as np 
import matplotlib.pyplot as plt 

cnt = 0 
normal = 0 
figures = []
for dir in ['./validation/']:

    label_dir = dir + 'labels/'
    image_dir = dir + 'images/'

    new_schema = dict()            
    images = []
    categories = []
    annotations = []


    for label_json in os.listdir(label_dir):
        label_dir_folder_json = label_dir+label_json
            
        #print(label_dir_folder_json)
        image_dir = label_dir_folder_json.replace('.json','.png')
        image_dir = image_dir.replace('label','image')
        #print(image_dir)
        
        

        with open(label_dir_folder_json, "r") as json_file:
            img = cv2.imread(image_dir, cv2.IMREAD_COLOR)
            h , w, c = img.shape
            
            img_name = label_json.replace('.json','.png')
            
            json_dict = json.load(json_file)
            image = dict()
            image['file_name'] = img_name
            image['height'] = h
            image['id'] = json_dict['id']
            image['width'] = w
            total_area = h*w
            figure_area = 0 
            for data in json_dict['segments']:
                
                try:    
                    data['equation']
                    
                except:
                    #print('도형')
                    continue
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
                figure_area += float(gap_x * gap_y)
    
        figures.append(figure_area/total_area)
        normal+=1
        cnt +=1
        #if cnt >= 10000:
        #    bins = np.linspace(0,1,10)
        #    plt.hist(figures,bins)
        #    plt.show()
        if figure_area/total_area > 0.9:
            #print(figure_area/total_area , '<<<<< figure_area occupying over than threshold.')
            #print(image_dir)
            
            shutil.move(image_dir ,dir + 'cropped_image/'+ img_name)
            shutil.move(label_dir_folder_json,dir+'cropped_label/'+label_json)
            #sys.exit()
            cnt +=1 
            if cnt % 1000 == 0 :
                print('1000장의 데이터를 move 했습니다.')
            
            #break
            #continue
    #break