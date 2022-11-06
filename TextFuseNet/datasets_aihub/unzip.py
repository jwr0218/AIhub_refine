import os 
import zipfile
import shutil
image_dir = './train_images/'
label_dir = './train_labels/'


for dir in [image_dir,label_dir]:
    zip_list = os.listdir(dir)
    for zip in zip_list : 
        
        if zip[-4:] != '.zip':
            continue
        zip_dir = dir + zip

        if '손' in zip:

            with zipfile.ZipFile(zip_dir, 'r') as zip_ref:
                zip_ref.extractall(dir+'hand/')

        else:


            with zipfile.ZipFile(zip_dir, 'r') as zip_ref:
                zip_ref.extractall(dir+'normal/')
            

    
    hand_dir = dir + 'hand/'
    hand_lst = os.listdir(hand_dir)
    for hand_ in hand_lst:
        
        lst = os.listdir(hand_dir + hand_)
        for datas in lst:
            d = os.listdir(hand_dir+hand_+'/'+datas)
            print(hand_dir+hand_+'/'+datas)
            try:
                d.remove('images')
            except:
                pass
            for data in d:
                if image_dir == dir :
                    shutil.move(hand_dir+hand_+'/'+datas+'/' + data, './images/' + data)
                else:
                    shutil.move(hand_dir+hand_+'/'+datas+'/' + data, './labels/' + data)
    hand_dir = dir + 'normal/'
    hand_lst = os.listdir(hand_dir)
    for hand_ in hand_lst:
        
        lst = os.listdir(hand_dir + hand_)
        for datas in lst:
            d = os.listdir(hand_dir+hand_+'/'+datas)
            for data in d:
                if image_dir == dir :
                    shutil.move(hand_dir+hand_+'/'+datas+'/' + data, './images/' + data)
                else:
                    shutil.move(hand_dir+hand_+'/'+datas+'/' + data, './labels/' + data)