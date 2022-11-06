# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import glob
import multiprocessing as mp
import os
import time
import cv2
import tqdm
import numpy as np
import json 
from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger
import sys
from predictor import VisualizationDemo
import torch 
import pandas as pd 
import os
import pickle
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# constants
WINDOW_NAME = "COCO detections"


def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set model
    cfg.MODEL.WEIGHTS = args.weights
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 Demo")
    parser.add_argument(
        "--config-file",
        default="/workspace/TextDetection/TextFuseNet/detect_text_custom/configs/custom.yaml",
        metavar="FILE",
        help="path to config file",
    )

    parser.add_argument(
        "--weights",
        default="/workspace/TextDetection/TextFuseNet/detect_text_custom/custom.pth",
        metavar="pth",
        help="the model used to inference",
    )

    parser.add_argument(
        "--input",
        default= '/workspace/TextDetection/TextFuseNet/datasets_aihub/training/images/',
        #"./aihub_korean/train_images/*",
        nargs="+"
    )

    parser.add_argument(
        "--output",
        default="./detect_text_custom/output/",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.65,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser


def compute_polygon_area(points):
    s = 0
    point_num = len(points)
    if(point_num < 3): return 0.0
    for i in range(point_num): 
        s += points[i][1] * (points[i-1][0] - points[(i+1)%point_num][0])
    return abs(s/2.0)
    
def make_image_crop(img_dir,prediction,polygons):
    classes = prediction['instances'].pred_classes
    img = cv2.imread(img_dir)
    
    crop_images = []
    bboxes = []
    for i in range(len(classes)):
        if classes[i]==0:
            if len(polygons[i]) != 0:
                points = []
                for j in range(0,len(polygons[i][0]),2):
                    points.append([polygons[i][0][j],polygons[i][0][j+1]])
                points = np.array(points)
                #print(points)
                area = compute_polygon_area(points)
                rect = cv2.minAreaRect(points)
                #print(rect)
                box = cv2.boxPoints(rect)
                #print(box)
                if area > 175:
                    bbox = [[int(box[0][0]) ,int(box[0][1])],[int(box[1][0]),int(box[1][1])],
                              [int(box[2][0]),int(box[2][1])],[int(box[3][0]),int(box[3][1])]]
                    bboxes.append(bbox) 
    color = (255, 255, 255)
    #print('============================')
    #print(polygons)
    #print(bboxes)
    for cnt, contour in enumerate(bboxes):
        stencil = np.zeros(img.shape).astype(np.dtype("uint8"))
        contour_ = np.array(contour,dtype = np.int32)
        cv2.fillConvexPoly(stencil, contour_, color)
        img_and = cv2.bitwise_and(stencil, img)
        x_min  =9999 
        x_max = 0
        y_min = 9999
        y_max = 0 
        for con in contour_:
            x_min = min(x_min,con[0])
            y_min = min(y_min,con[1])
            x_max = max(x_max,con[0])
            y_max = max(y_max,con[1])
        #print('======================')
        #print(img_and.shape)
        #print(contour_)
        #print(x_min,x_max,y_min,y_max)
        img_and = img_and[y_min:y_max,x_min:x_max]
        #sys.exit()
        try:

            cv2.imwrite('/workspace/TextDetection/TextFuseNet/detect_text_custom/test_full/'+img_name.split('.')[0]+"_{}_bbox.png".format(cnt),img_and)
        except:
            print('오류 발생, pass 합니다.')
            continue
    return 


def check_intersection(img,img_dir,prediction,polygons,figure_box):
    classes = prediction['instances'].pred_classes
    #img = cv2.imread(img_dir)
    

    bboxes = []
    for i in range(len(classes)):
        if classes[i]==0:
            if len(polygons[i]) != 0:
                points = []
                for j in range(0,len(polygons[i][0]),2):
                    points.append([polygons[i][0][j],polygons[i][0][j+1]])
                points = np.array(points)
                area = compute_polygon_area(points)
                rect = cv2.minAreaRect(points)
                box = cv2.boxPoints(rect)
                
                if area > 175:
                    bbox = [[int(box[0][0]) ,int(box[0][1])],[int(box[1][0]),int(box[1][1])],
                              [int(box[2][0]),int(box[2][1])],[int(box[3][0]),int(box[3][1])]]
                    bboxes.append(bbox)
                    #print('bbox : ',bbox)
                    #print('figure_box : ',figure_box)
                    #print(polygons)
                    #bbox = return_bbox(prediction,polygons)

    if len(bboxes) <= 0 :
        return 


    intersection = cal_intersection(img.shape,bboxes,figure_box,img_dir.split('/')[-1])

    if intersection >0 :
        
        print(img_dir)
        print('교집합이 발생 했습니다. ')
        
    w,h,c = img.shape
    #print(w,h,c)
    #sys.exit()
    return img_dir+ '\t ' +str(intersection)+"\t" +str(intersection/(w*h)) + '\n' , {'intersection' : intersection }

def cal_intersection(size,bbox1,bbox2,img_name):
    color = (255, 255, 255)

    stencil1 = np.zeros(size).astype(np.dtype("uint8"))
    
    for contour in bbox1:
       
        contour_ = np.array(contour,dtype = np.int32)
        cv2.fillConvexPoly(stencil1, contour_, color)
    
    stencil2= np.zeros(size).astype(np.dtype("uint8"))
    bbox2 = np.array(bbox2,dtype = np.int32)
    cv2.fillConvexPoly(stencil2, bbox2,color)
    np.logical_and(stencil1, stencil2)
    #sys.exit()
    intersection = np.sum(np.logical_and(stencil1, stencil2)) / 3 
    #print(intersection)
    #cv2.imwrite("/workspace/TextDetection/TextFuseNet/detect_text_custom/boxes/"+img_name.split('.')[0]+"_bbox.png", stencil1)

    #cv2.imwrite("/workspace/TextDetection/TextFuseNet/detect_text_custom/boxes/"+img_name.split('.')[0]+"_target.png", stencil2)


    return intersection / (stencil1.shape[0]*stencil1.shape[1])
        
if __name__ == "__main__":

    args = get_parser().parse_args()
    #file = open('/workspace/TextDetection/TextFuseNet/detect_text_custom/intersections.txt','w+')
    cfg = setup_cfg(args)
    detection_demo = VisualizationDemo(cfg)

    test_images_path = args.input
    output_path = args.output

    start_time_all = time.time()
    img_count = 0
    dataset = pd.DataFrame(columns = ['image_name','intersection'])
    test_lst = []
    with open('full_test_samples.pkl','rb') as fr:
        data = pickle.load(fr)
    
        for i in data:
            name = i.split('\\')[3]
            test_lst.append(name)
    print(len(test_lst))
    sys.exit()
    #for idx , i in enumerate(os.listdir(test_images_path)):
    for idx , i in enumerate(test_lst):
    
        #print('test')
        
        #print(test_labels_path)


        '/workspace/TextDetection/TextFuseNet/datasets_aihub/training/images/',

        try:
            print(i)
            if idx % 10 == 0 :
                print('현재 진행사항 {}/100: '.format(idx))
            #print(i)
            img_name = os.path.basename(i)
            img = cv2.imread(test_images_path+i)
            img_save_path = output_path + img_name.split('.')[0] + '.jpg'
            
            prediction, vis_output, polygons = detection_demo.run_on_image(img)
            make_image_crop(test_images_path+i,prediction,polygons)
        except:
            img_name = os.path.basename(i)
            tmp_path = test_images_path.replace('training','validation')
            img = cv2.imread(tmp_path+i)
            img_save_path = output_path + img_name.split('.')[0] + '.jpg'
            
            prediction, vis_output, polygons = detection_demo.run_on_image(img)
                    #print(data['box'])
                    
        #figurebox = data['box']
                    #print(type(figurebox))
        
            make_image_crop(tmp_path+i,prediction,polygons)
    #file.close()
