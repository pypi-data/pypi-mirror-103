import os, shutil

def merge_augmentations(augment_dir, output_dir, list_of_aug_files):
  '''
    - augment_dir         (string)   : The path which has subfolders that are augmentation folders.
    - output_dir          (string)   : The path you want to put all augmentations.
    - list_of_aug_files   (list)     : List of names which contains augmentations.
  '''
  os.mkdir(output_dir + '/images')
  os.mkdir(output_dir + '/labels')

  for folder in list_of_aug_files:
    if folder != 'base':
      for file in sorted(os.listdir(augment_dir + '/' + folder + '/images')):
        shutil.copy(augment_dir + '/' + folder + '/images/' + file, output_dir + '/images/' + folder + '_' + file.split("_")[-1].split('.')[0] + '.png')
        shutil.copy(augment_dir + '/' + folder + '/labels/' + file, output_dir + '/labels/' + folder + '_' + file.split("_")[-1].split('.')[0] + '.png')
    else:
      for file in sorted(os.listdir(augment_dir + '/' + folder + '/images')):
        shutil.copy(augment_dir + '/' + folder + '/images/' + file, output_dir + '/images/' + file.split("_")[-1].split('.')[0] + '.png')
        shutil.copy(augment_dir + '/' + folder + '/labels/' + file, output_dir + '/labels/' + file.split("_")[-1].split('.')[0] + '.png')
    

    print(folder + ' folder has been merged...')
    print('Number of images in output: ' + str(len(os.listdir(output_dir + '/images'))))
 

  print('Merging is done successfully!')


#n_iteration
#n_augmentation
def random_search(input_path,output_path,n_iteration,n_augmentation):
  aug_list=list(os.listdir(input_path))
  for i in range(n_iteration):
    augmentations=[]
    exclude=['combinations','.ipynb_checkpoints']
    os.mkdir("{}".format(i))
    new_output_path= output_path{}.format(i)
    for m,n in enumerate(range(n_augmentation)):
      aug2=[i for i in aug_list if i not in augmentations and i not in exclude]
      random_aug=random.choice(aug2)
      augmentations.append(random_aug)
    print(augmentations)
    
    merge_augmentations(input_path, new_output_path, augmentations)

  inzva_path=os.listdir(output_path)
  print(inzva_path)

  for item in inzva_path:
    images = os.path.abspath(output_path+"/"+item+"/images")
    for j, f in enumerate(os.listdir(images)):
      src = os.path.join(images, f)
      dst = os.path.join(images, (str(j)+".png"))
      os.rename(src, dst)
    labels = os.path.abspath(output_path+"/"+item+"/labels")
    for k, f in enumerate(os.listdir(labels)):
      src = os.path.join(labels, f)
      dst = os.path.join(labels, (str(k)+".png"))
      os.rename(src, dst)

  for road in inzva_path:
    #training function
    TRAIN_PATH_IMG        = output_path+'/'+road+'/images'
    TRAIN_PATH_MASK       = output_path+'/'+road+'/labels'
    os.mkdir(output_path+'/'+road+'/logs')
    os.mkdir(output_path+'/'+road+'/checkpoints')
    os.mkdir(output_path+'/'+road+'/results')
    LOG_PATH   = output_path+'/'+road+'/logs'
    CKPTS_PATH = output_path+'/'+road+'/checkpoints'
    RESULTS_PATH = output_path+'/'+road+'/results'
    KFOLD_TEMP_TRAIN      = output_path+'/'+road+'/temp_train'
    KFOLD_TEMP_TEST       = output_path+'/'+road+'/temp_test'

    data_gen_args = dict()
    train_generator = trainGenerator(2, output_path+'/'+road+'/','images','labels',data_gen_args,save_to_dir = None,target_size=(512,512))
    model = SqueezeUNet(inputs=Input((512, 512, 1)))
    model_checkpoint = ModelCheckpoint(CKPTS_PATH + "/fold_squeezeunet.hdf5", monitor='loss',verbose=1, save_best_only=True)
    model_history = model.fit_generator(train_generator,steps_per_epoch=20,epochs=20,callbacks=[model_checkpoint])
  

    
random_search(input_path,output_path,2,20)


from __future__ import print_function

import os
import skimage.io as io
import skimage.transform as trans
import shutil
import cv2
import matplotlib.pyplot as plt
import pickle
import time
import glob

import numpy as np
import keras
from keras.models import Model
from keras.layers import Input, merge, Convolution2D, MaxPooling2D, UpSampling2D
from keras.optimizers import Adam
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint, LearningRateScheduler

from keras import backend as keras

from keras.layers import Dropout

from sklearn.externals import joblib
import argparse
from keras.callbacks import *
import sys
import theano
import theano.tensor as T
from keras import initializers
from keras.layers import BatchNormalization
import copy
import tensorflow as tf

from keras.models import *
from keras.layers import *
from keras.optimizers import *
from tensorflow.keras.models import load_model as load_initial_model
from keras.preprocessing.image import ImageDataGenerator
from keras.losses import binary_crossentropy

import gc
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Dropout
from keras.layers import concatenate, Conv2DTranspose, BatchNormalization
from keras import backend as K

#metrics
def dice_coef(y_true, y_pred):
  smooth = 0.0
  y_true_f = keras.flatten(y_true)
  y_pred_f = keras.flatten(y_pred)
  intersection = keras.sum(y_true_f * y_pred_f)
  return (2. * intersection + smooth) / (keras.sum(y_true_f) + keras.sum(y_pred_f) + smooth)

def jacard(y_true, y_pred):

  y_true_f = keras.flatten(y_true)
  y_pred_f = keras.flatten(y_pred)
  intersection = keras.sum ( y_true_f * y_pred_f)
  union = keras.sum ( y_true_f + y_pred_f - y_true_f * y_pred_f)

  return intersection/union

def dice_coef_loss(y_true, y_pred):
    return 1. - dice_coef(y_true, y_pred)

def cross_entropy(p, q):
	  return -sum([p[i]*log2(q[i]) for i in range(len(p))])

#model
def fire_module(x, fire_id, squeeze=16, expand=64):
    f_name = "fire{0}/{1}"
    channel_axis = 1 if K.image_data_format() == 'channels_first' else -1

    x = Conv2D(squeeze, (1, 1), activation='relu', padding='same', name=f_name.format(fire_id, "squeeze1x1"))(x)
    x = BatchNormalization(axis=channel_axis)(x)

    left = Conv2D(expand, (1, 1), activation='relu', padding='same', name=f_name.format(fire_id, "expand1x1"))(x)
    right = Conv2D(expand, (3, 3), activation='relu', padding='same', name=f_name.format(fire_id, "expand3x3"))(x)
    x = concatenate([left, right], axis=channel_axis, name=f_name.format(fire_id, "concat"))
    return x


def SqueezeUNet(inputs, num_classes=None, deconv_ksize=3, dropout=0.5, activation='sigmoid'):
    """SqueezeUNet is a implementation based in SqueezeNetv1.1 and unet for semantic segmentation
    :param inputs: input layer.
    :param num_classes: number of classes.
    :param deconv_ksize: (width and height) or integer of the 2D deconvolution window.
    :param dropout: dropout rate
    :param activation: type of activation at the top layer.
    :returns: SqueezeUNet model
    """
    channel_axis = 1 if K.image_data_format() == 'channels_first' else -1
    if num_classes is None:
        num_classes = K.int_shape(inputs)[channel_axis]

    x01 = Conv2D(64, (3, 3), strides=(2, 2), padding='same', activation='relu', name='conv1')(inputs)
    x02 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='pool1', padding='same')(x01)

    x03 = fire_module(x02, fire_id=2, squeeze=16, expand=64)
    x04 = fire_module(x03, fire_id=3, squeeze=16, expand=64)
    x05 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='pool3', padding="same")(x04)

    x06 = fire_module(x05, fire_id=4, squeeze=32, expand=128)
    x07 = fire_module(x06, fire_id=5, squeeze=32, expand=128)
    x08 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='pool5', padding="same")(x07)

    x09 = fire_module(x08, fire_id=6, squeeze=48, expand=192)
    x10 = fire_module(x09, fire_id=7, squeeze=48, expand=192)
    x11 = fire_module(x10, fire_id=8, squeeze=64, expand=256)
    x12 = fire_module(x11, fire_id=9, squeeze=64, expand=256)

    if dropout != 0.0:
        x12 = Dropout(dropout)(x12)

    up1 = concatenate([
        Conv2DTranspose(192, deconv_ksize, strides=(1, 1), padding='same')(x12),
        x10,
    ], axis=channel_axis)
    up1 = fire_module(up1, fire_id=10, squeeze=48, expand=192)

    up2 = concatenate([
        Conv2DTranspose(128, deconv_ksize, strides=(1, 1), padding='same')(up1),
        x08,
    ], axis=channel_axis)
    up2 = fire_module(up2, fire_id=11, squeeze=32, expand=128)

    up3 = concatenate([
        Conv2DTranspose(64, deconv_ksize, strides=(2, 2), padding='same')(up2),
        x05,
    ], axis=channel_axis)
    up3 = fire_module(up3, fire_id=12, squeeze=16, expand=64)

    up4 = concatenate([
        Conv2DTranspose(32, deconv_ksize, strides=(2, 2), padding='same')(up3),
        x02,
    ], axis=channel_axis)
    up4 = fire_module(up4, fire_id=13, squeeze=16, expand=32)
    up4 = UpSampling2D(size=(2, 2))(up4)

    x = concatenate([up4, x01], axis=channel_axis)
    x = Conv2D(64, (3, 3), strides=(1, 1), padding='same', activation='relu')(x)
    x = UpSampling2D(size=(2, 2))(x)
    x = Conv2D(num_classes, (1, 1), activation=activation)(x)
    model = Model(inputs, x)
    #model.summary()
    model.compile(optimizer=Adam(lr = 1e-4), loss=binary_crossentropy, metrics = ['accuracy',dice_coef,jacard,tf.keras.metrics.MeanIoU(num_classes=2),
                                                                                      tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])                                                                                
    return model

#generators
def adjustData(img,mask,flag_multi_class,num_class):
  if(flag_multi_class):
    img = img / 255
    mask = mask[:,:,:,0] if(len(mask.shape) == 4) else mask[:,:,0]
    new_mask = np.zeros(mask.shape + (num_class,))
    for i in range(num_class):
        #for one pixel in the image, find the class in mask and convert it into one-hot vector
        #index = np.where(mask == i)
        #index_mask = (index[0],index[1],index[2],np.zeros(len(index[0]),dtype = np.int64) + i) if (len(mask.shape) == 4) else (index[0],index[1],np.zeros(len(index[0]),dtype = np.int64) + i)
        #new_mask[index_mask] = 1
        new_mask[mask == i,i] = 1
    new_mask = np.reshape(new_mask,(new_mask.shape[0],new_mask.shape[1]*new_mask.shape[2],new_mask.shape[3])) if flag_multi_class else np.reshape(new_mask,(new_mask.shape[0]*new_mask.shape[1],new_mask.shape[2]))
    mask = new_mask
  elif (np.max(img) > 1):
    img = img / 255
    mask = mask /255
    mask[mask > 0.5] = 1
    mask[mask <= 0.5] = 0
  return (img,mask)

def trainGenerator(batch_size,train_path,image_folder,mask_folder,aug_dict,image_color_mode = "grayscale",
                    mask_color_mode = "grayscale",image_save_prefix  = "image",mask_save_prefix  = "mask",
                    flag_multi_class = False,num_class = 2,save_to_dir = None,target_size = (512,512),seed = 1):
  image_datagen = ImageDataGenerator(**aug_dict)
  mask_datagen = ImageDataGenerator(**aug_dict)
  image_generator = image_datagen.flow_from_directory(
      train_path,
      classes = [image_folder],
      class_mode = None,
      color_mode = image_color_mode,
      target_size = target_size,
      batch_size = batch_size,
      save_to_dir = save_to_dir,
      save_prefix  = image_save_prefix,
      seed = seed)
  mask_generator = mask_datagen.flow_from_directory(
      train_path,
      classes = [mask_folder],
      class_mode = None,
      color_mode = mask_color_mode,
      target_size = target_size,
      batch_size = batch_size,
      save_to_dir = save_to_dir,
      save_prefix  = mask_save_prefix,
      seed = seed)
  train_generator = zip(image_generator, mask_generator)
  for (img,mask) in train_generator:
    img,mask = adjustData(img,mask,flag_multi_class,num_class)
    yield (img,mask)




def saveResult(fold,k,save_path,npyfile,flag_multi_class = False,num_class = 2):
  for i,item in enumerate(npyfile):
      img = labelVisualize(num_class,COLOR_DICT,item) if flag_multi_class else item[:,:,0]
      io.imsave(os.path.join(save_path,"%d_predict.png"%(i+fold*k)),img)

#k_fold

def k_fold(epoch,train_batch_size,test_batch_size,k=5,show_samples=False,no_of_sample=300):
  """
  Parameters:
    - epoch: nof epochs for each fold
    - train_batch_size: batch size for training
    - test_batch_size: batch size for test
    - k: I HAVE K SAMPLES IN TEST AND 30+AUGMENTED-K SAMPLES IN TRAIN 
          for example if you didn't make augmentation, and choose k=5
          you have 5 images in test and 25 images in train.
          function iterates folds.
    - show_samples: show ground truth predictions pairs 
  """

  assert 30 % k ==0, "Number of images divided by fold number must be integer."
  NOF_PLOTS = 0
  for i in range(int(30/k)):
    test_images_temp = [j for j in range(k)]
    test_images_temp_2 = [a + i*k for a in test_images_temp]
    test_images = [str(a) for a in test_images_temp_2] #our test ids
    print("Test images: {}".format(test_images))

    shutil.rmtree(KFOLD_TEMP_TRAIN, ignore_errors=False, onerror=None)
    os.mkdir(KFOLD_TEMP_TRAIN)
    os.mkdir(KFOLD_TEMP_TRAIN + "/images")
    os.mkdir(KFOLD_TEMP_TRAIN + "/labels")

    shutil.rmtree(KFOLD_TEMP_TEST, ignore_errors=False, onerror=None)
    os.mkdir(KFOLD_TEMP_TEST)
    os.mkdir(KFOLD_TEMP_TEST + "/images")
    os.mkdir(KFOLD_TEMP_TEST + "/labels")

    for test_image in test_images: #allocates test images into the path
      src = TRAIN_PATH_IMG + "/" + test_image + ".png"
      shutil.copy(src, KFOLD_TEMP_TEST + "/images")

      src = TRAIN_PATH_MASK + "/" + test_image + ".png"
      shutil.copy(src, KFOLD_TEMP_TEST + "/labels")

    for img in sorted(os.listdir(TRAIN_PATH_IMG)): #allocates train images into the path
      img_splitted_1 = img.split("_")
      img_splitted_2 = img.split(".")
      if (img_splitted_1[-1].split(".")[0] not in test_images) and (img_splitted_2[0] not in test_images):
        src = TRAIN_PATH_IMG + "/" + img
        shutil.copy(src, KFOLD_TEMP_TRAIN + "/images")

        src = TRAIN_PATH_MASK + "/" + img
        shutil.copy(src, KFOLD_TEMP_TRAIN + "/labels")

    data_gen_args = dict()
    train_generator = trainGenerator(train_batch_size,KFOLD_TEMP_TRAIN,'images','labels',data_gen_args,save_to_dir = None)
    test_generator = testGenerator2(test_batch_size,KFOLD_TEMP_TEST,'images','labels',data_gen_args,save_to_dir = None)

    model = SqueezeUNet(inputs=Input((512, 512, 1)))
    #model.save('/content/drive/MyDrive/AI_Projects/seed_deneme/initial_model/my_model.h5')
    #model = load_initial_model('/content/drive/MyDrive/AI_Projects/seed_deneme/initial_model/my_model.h5', custom_objects={'dice_coef': dice_coef , 'jacard' : jacard}) ## SONRADAN
    model_checkpoint = ModelCheckpoint(CKPTS_PATH + "/fold_{}_unet_ISBI2012.hdf5".format(i), monitor='loss',verbose=1, save_best_only=True)
    model_history = model.fit_generator(train_generator,steps_per_epoch=no_of_sample//train_batch_size,epochs=epoch,
                                        callbacks=[model_checkpoint],validation_data=test_generator,validation_steps=no_of_sample//test_batch_size)
    #steps_per_epochda   sample sayısı kadara böl
    log_file = open(LOG_PATH + "/log_fold_{}.pkl".format(i), "wb")#history file
    pickle.dump(model_history.history, log_file)
    log_file.close()

    test_generator_2 = testGenerator(KFOLD_TEMP_TEST)
    results = model.predict_generator(test_generator_2,k,verbose=1)
    saveResult(i,k,RESULTS_PATH,results)

    #time.sleep(10)
    # we dont know if time.sleep is the solution
    # but keep it
    #del model
    #gc.collect()

    # worst-practice visualization code. since our plots are dynamic, figsize of (17,17)
    # can be small for towards the end folds. You can make figsize = (17 + NOF_PLOTS, 17 + NOF_PLOTS) for bigger plots
    if show_samples:
      fig, axs = plt.subplots(k + NOF_PLOTS,3,figsize=(17,17))
      for idx,item in enumerate(sorted(os.listdir(RESULTS_PATH))):
        item_without_predict = item.split("_")[0] + ".png"
        img_real = cv2.imread(TRAIN_PATH_IMG + "/" + item_without_predict)
        img_real = cv2.cvtColor(img_real, cv2.COLOR_BGR2RGB)
        #print(TRAIN_PATH_IMG + "/" + item_without_predict)
        #print(os.path.isfile(TRAIN_PATH_IMG + "/" + item_without_predict))
        img_ground_truth = cv2.imread(TRAIN_PATH_MASK + "/" + item_without_predict)
        img_ground_truth = cv2.cvtColor(img_ground_truth, cv2.COLOR_BGR2RGB) 
        img_predict = cv2.imread(RESULTS_PATH + "/" + item)
        img_predict = cv2.cvtColor(img_predict, cv2.COLOR_BGR2RGB)

        axs[idx,0].imshow(img_real)
        axs[idx,0].title.set_text('image_{}'.format(item_without_predict))
        axs[idx,1].imshow(img_ground_truth)
        axs[idx,1].title.set_text('ground truth')
        axs[idx,2].imshow(img_predict)
        axs[idx,2].title.set_text('predicted')
      plt.show()
      NOF_PLOTS += k

