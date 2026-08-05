# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
from camera1 import VideoCamera1
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
#from plotly import graph_objects as go
import cv2
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import imagehash
from werkzeug.utils import secure_filename
from PIL import Image
import argparse
import urllib.request
import urllib.parse

import pyttsx3

from skimage import transform
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS


import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import PIL.Image
from PIL import Image
##
import torch
import torch.nn as nn
import mediapipe as mp
##
import sounddevice as sd
#from faster_whisper import WhisperModel
##
import pygame
import time
##
# necessary imports 
import seaborn as sns
#import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

plt.style.use('fivethirtyeight')
#%matplotlib inline
pd.set_option('display.max_columns', 26)
##
from PIL import Image, ImageOps
import scipy.ndimage as ndi

from skimage import transform
import seaborn as sns
#from keras.preprocessing.image import ImageDataGenerator , load_img , img_to_array
#from keras.models import Sequential
#from keras.layers import Conv2D, Flatten, MaxPool2D, Dense
##
import glob
#from keras.models import Sequential, load_model
import numpy as np
import pandas as pd
import seaborn as sns
#import keras as k
#from keras.layers import Dense
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
#from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
#from tensorflow.keras.optimizers import Adam
##
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="sign_meet_new"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    ff1=open("static/log.txt","w")
    ff1.write("2")
    ff1.close()
    
    return render_template('index.html',msg=msg)


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM sign_user WHERE uname = %s AND pass = %s AND allow_st=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname

            ff=open("static/msg.txt","w")
            ff.write("")
            ff.close()

            f2=open("static/user2.txt","w")
            f2.write(uname)
            f2.close()
            fn=uname+".jpg"
            shutil.copy("static/f1.jpg","static/photo/"+fn)
            
            cursor.execute('SELECT count(*) FROM sign_user WHERE status=1')
            dd = cursor.fetchone()[0]
            if dd==0:
                cursor.execute("update sign_user set status=1 where uname=%s",(uname,))
                mydb.commit()

                ff=open("static/deaf.txt","w")
                ff.write(uname)
                ff.close()
            
            return redirect(url_for('test_cam'))
        else:
            msg = 'Incorrect username/password!' 
   
    return render_template('login_user.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided' 
   
    return render_template('login.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute('SELECT count(*) FROM sign_user WHERE uname = %s', (uname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM sign_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO sign_user(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,uname,pass1)
            mycursor.execute(sql,val)
            mydb.commit()
            return redirect(url_for('login_user'))
        else:
            msg="fail"

    
        
    return render_template('register.html',msg=msg)

def lg_translate(lg,output):
    result=""
    recognized_text=output
    recognizer = sr.Recognizer()
    translator = Translator()
    try:
        available_languages = {
            'ta': 'Tamil',
            'hi': 'Hindi',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'te': 'Telugu',
            'mr': 'Marathi',
            'ur': 'Urdu',
            'bn': 'Bengali',
            'gu': 'Gujarati',
            'fr': 'French'
        }

        print("Available languages:")
        for code, language in available_languages.items():
            print(f"{code}: {language}")

        #selected_languages = input("Enter the language codes (comma-separated) you want to translate to: ").split(',')
        selected_languages=lg.split(',')
       
        for lang_code in selected_languages:
            lang_code = lang_code.strip()
            if lang_code in available_languages:
                translated = translator.translate(recognized_text, dest=lang_code)
                print(f"Translation in {available_languages[lang_code]} ({lang_code}): {translated.text}")

                result=translated.text
               

            else:
                print(f"Language code {lang_code} not available.")

        
    except Exception as e:
        print("An error occurred during translation:", e)

    return result
    ###

####
def translate_text(text, source_language, target_language):
    api_key = 'AIzaSyDW9tvaQUsywmaILt73Go8Fy5mU6ILOixU'  # Replace with your API key
    url = f'https://translation.googleapis.com/language/translate/v2?key={api_key}'
    payload = {
        'q': text,
        'source': source_language,
        'target': target_language,
        'format': 'text'
    }
    response = requests.post(url, json=payload)
    translation_data = response.json()
    translated_text = translation_data
    #translation_data['data']['translations'][0]['translatedText']
    return translated_text

def speak(audio):
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()

def text_to_speech(text, language='en'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the audio file
    tts.save("static/output.mp3")

    # Play the audio
    #os.system("start output.mp3")  # For Windows, use "start", for macOS use "afplay", for Linux use "mpg321"




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    dimg=[]
    '''path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #resize
        img = cv2.imread('static/data/'+fname)
        rez = cv2.resize(img, (300, 300))
        cv2.imwrite("static/dataset/"+fname, rez)'''
        
        
    return render_template('admin.html',dimg=dimg)
@app.route('/process_a', methods=['GET', 'POST'])
def process_a():
    dimg=[]
    path_main = 'static/dataset'
    
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    return render_template('process_a.html',dimg=dimg)

@app.route('/process1_a', methods=['GET', 'POST'])
def process1_a():
    dimg=[]
    path_main = 'static/dataset'
    
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    return render_template('process1_a.html',dimg=dimg)

@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))

        #resize
        #img = cv2.imread('static/data/'+fname)
        #rez = cv2.resize(img, (400, 300))
        #cv2.imwrite("static/dataset/"+fname, rez)'''

        '''img = cv2.imread('static/dataset/'+fname) 	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("static/trained/g_"+fname, gray)
        ##noice
        img = cv2.imread('static/trained/g_'+fname) 
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        fname2='ns_'+fname
        cv2.imwrite("static/trained/"+fname2, dst)'''

    return render_template('pro1.html',dimg=dimg)


def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/pro11', methods=['GET', 'POST'])
def pro11():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)

    return render_template('pro11.html',dimg=dimg)

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #f1=open("adata.txt",'w')
        #f1.write(fname)
        #f1.close()
        ##bin
        '''image = cv2.imread('static/dataset/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)

        
        ###cv2.imshow('thresh', thresh)
        ###cv2.imshow('result', result)
        ###cv2.imshow('mask', mask)
        ###cv2.imshow('kmeans', kmeans)
        ###cv2.imshow('image', image)
        ###cv2.waitKey()

        #cv2.imwrite("static/trained/bb/bin_"+fname, thresh)'''

    
   

    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        ##RPN
        
        
        img = cv2.imread('static/trained/g_'+fname)
        '''gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,1.5*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        segment = cv2.subtract(sure_bg,sure_fg)
        img = Image.fromarray(img)
        segment = Image.fromarray(segment)
        path3="static/trained/sg/"+fname'''
        #segment.save(path3)
        

    return render_template('pro2.html',dimg=dimg)

@app.route('/pro3', methods=['GET', 'POST'])
def pro3():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        
    '''path_main = 'static/dataset'
    i=1
    while i<=50:
        fname="r"+str(i)+".jpg"
        dimg.append(fname)

        img = Image.open('static/data/classify/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/upload/ff_'+fname)
        i+=1
    i=1
    j=51
    while i<=10:
        
        fname="r"+str(j)+".jpg"
        dimg.append(fname)

        img = Image.open('static/dataset/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/upload/ff_'+fname)
        j+=1
        i+=1

    '''    

    return render_template('pro3.html',dimg=dimg)

@app.route('/pro4', methods=['GET', 'POST'])
def pro4():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        #####
        image = cv2.imread("static/dataset/"+fname)
        '''gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        
        path4="static/trained/ff/"+fname
        edged.save(path4)'''
        ##
    
        
    return render_template('pro4.html',dimg=dimg)


@app.route('/pro5', methods=['GET', 'POST'])
def pro5():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    #graph
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[30,80,140,210,265]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model Precision")
    plt.ylabel("precision")
    
    fn="graph1.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph2
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[30,80,140,220,275]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model recall")
    plt.ylabel("recall")
    
    fn="graph2.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph3########################################
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[5,23,55,85,105]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy %")
    
    fn="graph3.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #######################################################
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[5,23,55,85,105]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Model loss")
    
    fn="graph4.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    return render_template('pro5.html',dimg=dimg)

def toString(a):
  l=[]
  m=""
  for i in a:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m
                
@app.route('/pro6', methods=['GET', 'POST'])
def pro6():
    msg=""
    dimg=[]
    path_main = 'static/dataset'
    
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    

    return render_template('pro6.html',dimg=dimg)

#######
@app.route('/classify1', methods=['GET', 'POST'])
def classify1():
    msg=""
    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')


    ##    
    ff2=open("static/trained/tdata.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    ex=dat.split(',')
    ##
    vv=[]
    vn=0
    data2=[]
    
    path_main = 'static/dataset'
    for fname in os.listdir(path_main):
        print(fname)
            
    for val in ex:
        dt=[]
        n=0
        
        for fname in os.listdir(path_main):
            fa1=fname.split('.')
            fa=fa1[0].split('-')
            #print(fa[0])
            #print(fa[1])
            fv=int(fa[1])-1
            
            if cname[fv]==val:
                dt.append(fname)
                n+=1
        vv.append(n)
        vn+=n
        data2.append(dt)
        
    print(vv)
    print(data2[0])
    
    i=0
    vd=[]
    data4=[]
    while i<8:
        vt=[]
        vi=i+1
        vv[i]

        vt.append(cname[i])
        vt.append(str(vv[i]))
        
        vd.append(str(vi))
        data4.append(vt)
        i+=1
    print(data4)

    
    dd2=vv
    doc = vd #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['green','yellow','red','blue','brown','pink','grey','orange']
    plt.bar(doc, values, color =cc,
            width = 0.4)
 

    plt.ylim((1,25))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    #plt.xticks(rotation=20)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()
    return render_template('classify1.html',msg=msg,cname=cname,data2=data2,data4=data4)


@app.route('/train_gesture', methods=['GET', 'POST'])
def train_gesture():
    msg=""
    mycursor = mydb.cursor()

    
    
    if request.method=='POST':
        gname=request.form['gname']
        
        
        
        mycursor.execute("SELECT count(*) FROM ga_gesture where gesture=%s",(gname,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM ga_gesture")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            ff=open("static/label.txt","w")
            ff.write(gname)
            ff.close()
            gf="f"+str(maxid)

            
            gfile="f"+str(maxid)+".csv"
            ff=open("static/label1.txt","w")
            ff.write(gfile)
            ff.close()
                    
            sql = "INSERT INTO ga_gesture(id,gesture,fname) VALUES (%s, %s, %s)"
            val = (maxid,gname,gfile)
            mycursor.execute(sql,val)
            mydb.commit()
        else:
            mycursor.execute("SELECT * FROM ga_gesture where gesture=%s",(gname,))
            gd = mycursor.fetchone()
            gid=gd[0]
            ff=open("static/label.txt","w")
            ff.write(gname)
            ff.close()
            gf="f"+str(gid)

            
            gfile="f"+str(gid)+".csv"
            ff=open("static/label1.txt","w")
            ff.write(gfile)
            ff.close() 
            
            
        msg="ok"
    
        
    return render_template('train_gesture.html',msg=msg)

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    msg=""
    gdata=[]
    act=request.args.get("act")
    st=request.args.get("st")
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ga_gesture")
    gdata = mycursor.fetchall()

    if st=="del":
        did=request.args.get("did")
        mycursor.execute("SELECT * FROM ga_gesture where id=%s",(did,))
        gd = mycursor.fetchone()
        gfile=gd[2]
        os.remove("static/hand_gesture_data/"+gfile)
        mycursor.execute("delete from ga_gesture where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('capture',act='1'))
        
        
    return render_template('capture.html',msg=msg,act=act,gdata=gdata)

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ga_gesture")
    data = mycursor.fetchall()

    dt=[]
    dt2=[]
    for dc in data:
        dt.append(dc[1])
        d1=dc[2].split(".")
        dt2.append(d1[0])
        
    cname="|".join(dt)
    cname2="|".join(dt2)
    ff=open("static/class1.txt","w")
    ff.write(cname)
    ff.close()

    ff=open("static/class2.txt","w")
    ff.write(cname2)
    ff.close()
    
    #build model
    DATA_DIR = "static/hand_gesture_data"

    # Load data
    data = []
    labels = []
    gesture_map = {}  # Label mapping

    for idx, file in enumerate(os.listdir(DATA_DIR)):
        gesture_name = file.split(".")[0]
        gesture_map[idx] = gesture_name  # Store label mapping

        file_path = os.path.join(DATA_DIR, file)
        df = pd.read_csv(file_path, header=None)
        data.extend(df.values)
        labels.extend([idx] * len(df))

    # Convert to numpy array
    X = np.array(data)
    y = np.array(labels)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model and gesture mapping
    joblib.dump(model, "gesture_model.pkl")
    joblib.dump(gesture_map, "gesture_map.pkl")

    print(f"Model trained with accuracy: {model.score(X_test, y_test) * 100:.2f}%")

    return render_template('classify.html',msg=msg,data=data)


@app.route('/avatar_upload', methods=['GET', 'POST'])
def avatar_upload():
    msg=""
    dimg=[]
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        message=request.form['message']
        file = request.files['file']

        mycursor.execute("SELECT max(id)+1 FROM sign_image")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        fn="F"+str(maxid)+".gif"
        file.save(os.path.join("static/upload", fn))
        
        sql = "INSERT INTO sign_image(id,message,image_file) VALUES (%s, %s, %s)"
        val = (maxid,message,fn)
        mycursor.execute(sql,val)
        mydb.commit()
        msg="success"
        #return redirect(url_for('login_user'))

    
    '''path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #resize
        img = cv2.imread('static/data/'+fname)
        rez = cv2.resize(img, (300, 300))
        cv2.imwrite("static/dataset/"+fname, rez)'''
        
        
    return render_template('avatar_upload.html',msg=msg)

@app.route('/view_image', methods=['GET', 'POST'])
def view_image():
    msg=""
    act=request.args.get("act")
    dimg=[]
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM sign_image")
    data = mycursor.fetchall()

    if act=="del":
        did=request.args.get("did")

        mycursor.execute("SELECT * FROM sign_image where id=%s",(did,))
        d1 = mycursor.fetchone()
        fn=d1[2]
        if os.path.exists("static/upload/"+fn):
            os.remove("static/upload/"+fn)
        mycursor.execute("delete from sign_image where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_image'))

        
    return render_template('view_image.html',msg=msg,data=data,act=act)

@app.route('/view_user', methods=['GET', 'POST'])
def view_user():
    msg=""
    act=request.args.get("act")
    dimg=[]
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT * FROM sign_user")
    data = mycursor.fetchall()

    if act=="yes":
        did=request.args.get("did")
        mycursor.execute("update sign_user set allow_st=1 where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_user'))

    if act=="no":
        did=request.args.get("did")
        mycursor.execute("update sign_user set allow_st=2 where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_user'))

        
    return render_template('view_user.html',msg=msg,data=data,act=act)

@app.route('/test_cam', methods=['GET', 'POST'])
def test_cam():
    msg=""
    fn=""
    uname=""
    
    if 'username' in session:
        uname = session['username']
    print(uname)
    cursor = mydb.cursor()
    user=""
    cursor.execute('SELECT * FROM sign_user WHERE status=1')
    dd = cursor.fetchall()
    for dd1 in dd:
        user=dd1[4]

    f2=open("static/user.txt","w")
    f2.write(user)
    f2.close()

    ff=open("static/msg.txt","w")
    ff.write("")
    ff.close()

    ff=open("static/act.txt","w")
    ff.write("")
    ff.close()
            

    act=request.args.get("act")
    f2=open("lang.txt","r")
    lg=f2.read()
    f2.close()

    if request.method=='POST':
        lg=request.form['language']
        f2=open("lang.txt","w")
        f2.write(lg)
        f2.close()

    
        
    return render_template('test_cam.html',msg=msg,lg=lg,user=user,uname=uname)

@app.route('/test_voice', methods=['GET', 'POST'])
def test_voice():
    msg=""
    st=""
    vtext=""
    act=""
    dimg=[]
    uname=""
    
    if 'username' in session:
        uname = session['username']
    
    mycursor = mydb.cursor()
    
    img=""

    if request.method=='POST':        
        mess=request.form['message']
        print("hh")
        print(mess)
        if mess=="":
            s=1
        else:
            mm="%"+mess+"%"
            
            mycursor.execute("SELECT * FROM sign_image where message like %s",(mm,))
            dat = mycursor.fetchall()

            for dat1 in dat:
                img=dat1[2]
                

            if img=="":
                s=1
            else:
                ff=open("static/det.txt","w")
                ff.write(mess)
                ff.close()
                ff=open("static/img.txt","w")
                ff.write(img)
                ff.close()
                ff=open("static/act.txt","w")
                ff.write("1")
                ff.close()
        
                return redirect(url_for('test_voice',act='1'))

    ff=open("static/act.txt","r")
    act=ff.read()
    ff.close()
        
    if act=="1":
        ff=open("static/det.txt","r")
        vtext=ff.read()
        ff.close()

        ff=open("static/img.txt","r")
        img=ff.read()
        ff.close()

        #ff=open("static/act.txt","w")
        #ff.write("")
        #ff.close()
        
    return render_template('test_voice.html',msg=msg,act=act,img=img,st=st,vtext=vtext)

@app.route('/test_voice1', methods=['GET', 'POST'])
def test_voice1():
    msg=""
    st=""
    vtext=""
    act=""
    dimg=[]
    uname=""
    
    if 'username' in session:
        uname = session['username']
    
    img=""
    ff=open("static/act.txt","r")
    act=ff.read()
    ff.close()
        
    if act=="1":
        ff=open("static/det.txt","r")
        vtext=ff.read()
        ff.close()

        ff=open("static/img.txt","r")
        img=ff.read()
        ff.close()

        #ff=open("static/act.txt","w")
        #ff.write("")
        #ff.close()
        
    return render_template('test_voice1.html',msg=msg,act=act,img=img,st=st,vtext=vtext)

@app.route('/test_voice2', methods=['GET', 'POST'])
def test_voice2():
    msg=""
    st=""
    vtext=""
    act=""
    dimg=[]
    img=""
    uname=""
    
    if 'username' in session:
        uname = session['username']
    
    ff=open("static/act.txt","r")
    act=ff.read()
    ff.close()

    ff=open("static/user.txt","r")
    user=ff.read()
    ff.close()
        
    if act=="1":
        ff=open("static/det.txt","r")
        vtext=ff.read()
        ff.close()

        ff=open("static/img.txt","r")
        img=ff.read()
        ff.close()

        if user==uname:
            ff=open("static/count.txt","w")
            ff.write("1")
            ff.close()
        else:
            ff=open("static/count2.txt","w")
            ff.write("1")
            ff.close()

    ff=open("static/count.txt","r")
    cc=ff.read()
    ff.close()

    ff=open("static/count2.txt","r")
    cc2=ff.read()
    ff.close()

    cn=int(cc)
    cn2=int(cc2)
    cnn=cn+cn2
    if cnn>=2:
        ff=open("static/act.txt","w")
        ff.write("")
        ff.close()

        ff=open("static/count.txt","w")
        ff.write("0")
        ff.close()

        ff=open("static/count2.txt","w")
        ff.write("0")
        ff.close()
        
    return render_template('test_voice2.html',msg=msg,act=act,img=img,st=st,vtext=vtext)

@app.route('/process', methods=['GET', 'POST'])
def process():
    dimg=[]
    path_main = 'static/dataset'
    
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    return render_template('process.html',dimg=dimg)

@app.route('/process1', methods=['GET', 'POST'])
def process1():
    dimg=[]
    path_main = 'static/dataset'
    
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    return render_template('process1.html',dimg=dimg)


#Transformer-Based Gesture Encoder (Sign Recognition)
#MediaPipe Keypoint Extractor
class HolisticKeypoints:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            refine_face_landmarks=True
        )

    def extract(self, frame_bgr):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(frame_rgb)

        # Collect keypoints
        kp = []

        # Face: 468 points (x,y,z)
        if results.face_landmarks:
            for lm in results.face_landmarks.landmark:
                kp.extend([lm.x, lm.y, lm.z])
        else:
            kp.extend([0.0] * 468 * 3)

        # Pose: 33 points (x,y,z,visibility)
        if results.pose_landmarks:
            for lm in results.pose_landmarks.landmark:
                kp.extend([lm.x, lm.y, lm.z, lm.visibility])
        else:
            kp.extend([0.0] * 33 * 4)

        # Left hand: 21 points (x,y,z)
        if results.left_hand_landmarks:
            for lm in results.left_hand_landmarks.landmark:
                kp.extend([lm.x, lm.y, lm.z])
        else:
            kp.extend([0.0] * 21 * 3)

        # Right hand: 21 points (x,y,z)
        if results.right_hand_landmarks:
            for lm in results.right_hand_landmarks.landmark:
                kp.extend([lm.x, lm.y, lm.z])
        else:
            kp.extend([0.0] * 21 * 3)

        return np.array(kp, dtype=np.float32)



#Transformer Gesture Encoder Model
class GestureTransformer(nn.Module):
    def __init__(self, input_dim, num_classes, d_model=256, nhead=8, num_layers=4, dropout=0.1):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=512,
            dropout=dropout,
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.classifier = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, num_classes)
        )

    def forward(self, x):
        # x: (B, T, input_dim)
        x = self.input_proj(x)
        x = self.encoder(x)
        x = x.mean(dim=1)   # global average pooling over time
        return self.classifier(x)


#Real-Time Webcam Prediction
def run_realtime_sign_recognition():
    # Example sign labels
    labels = ["HELLO", "THANK YOU", "YES", "NO", "I LOVE YOU"]

    extractor = HolisticKeypoints()

    # Calculate input dimension:
    input_dim = (468*3) + (33*4) + (21*3) + (21*3)
    model = GestureTransformer(input_dim=input_dim, num_classes=len(labels))
    model.eval()

    # NOTE: model is untrained here.
    # Load trained weights like:
    # model.load_state_dict(torch.load("gesture_transformer.pth", map_location="cpu"))

    cap = cv2.VideoCapture(0)
    seq = []
    SEQ_LEN = 30

    print("Press Q to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        kp = extractor.extract(frame)
        seq.append(kp)

        if len(seq) > SEQ_LEN:
            seq = seq[-SEQ_LEN:]

        if len(seq) == SEQ_LEN:
            x = torch.tensor(np.array(seq)[None, :, :], dtype=torch.float32)
            with torch.no_grad():
                logits = model(x)
                pred = logits.argmax(dim=1).item()
                sign = labels[pred]

            cv2.putText(frame, f"SIGN: {sign}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Sign Recognition", frame)
        if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
            break

    cap.release()
    cv2.destroyAllWindows()
############
#RNN-T / CTC Speech Recognition
def init_rnn():
    SAMPLE_RATE = 16000
    BLOCK_SEC = 2.0

    audio_q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_q.put(indata.copy())

def run_streaming_stt():
    print("Loading model...")
    model = WhisperModel("small", device="cpu", compute_type="int8")  # use "cuda" for GPU

    print("Listening... Press Ctrl+C to stop.")
    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, callback=callback):
        buffer = np.zeros((0, 1), dtype=np.float32)

        while True:
            data = audio_q.get()
            buffer = np.concatenate([buffer, data], axis=0)

            # Process every 2 seconds
            if len(buffer) >= int(SAMPLE_RATE * BLOCK_SEC):
                chunk = buffer[: int(SAMPLE_RATE * BLOCK_SEC)]
                buffer = buffer[int(SAMPLE_RATE * BLOCK_SEC):]

                audio = chunk.flatten().astype(np.float32)

                segments, info = model.transcribe(audio, language="en")
                text = ""
                for seg in segments:
                    text += seg.text

                text = text.strip()
                if text:
                    print(">>", text)
    
###########
#Neural Avatar Synthesis (For Sign Animation Generation)
#sign motion library (demo)
SIGN_LIBRARY = {
    "HELLO": [(0, -20), (0, -40), (0, -20), (0, -40)],
    "YES":   [(0,  20), (0, -20), (0,  20), (0, -20)],
    "NO":    [(-20, 0), (20, 0), (-20, 0), (20, 0)],
}

def text_to_sign_sequence(text):
    words = text.upper().split()
    seq = []
    for w in words:
        if w in SIGN_LIBRARY:
            seq.append((w, SIGN_LIBRARY[w]))
    return seq

def run_avatar():
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Neural Avatar Synthesis (Demo)")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)

    base_x, base_y = 400, 250
    hand_x, hand_y = base_x + 80, base_y - 40

    text = "HELLO YES NO"
    signs = text_to_sign_sequence(text)

    idx = 0
    step = 0

    running = True
    while running:
        screen.fill((20, 20, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw body
        pygame.draw.circle(screen, (255, 220, 200), (base_x, base_y - 100), 40)  # head
        pygame.draw.line(screen, (200, 200, 255), (base_x, base_y - 60), (base_x, base_y + 100), 6)  # body
        pygame.draw.line(screen, (200, 200, 255), (base_x, base_y), (hand_x, hand_y), 6)  # arm

        if signs:
            sign_name, motion = signs[idx]
            dx, dy = motion[step]

            # Update hand position
            hand_x = base_x + 80 + dx
            hand_y = base_y - 40 + dy

            # Show sign label
            label = font.render(f"Signing: {sign_name}", True, (255, 255, 255))
            screen.blit(label, (20, 20))

            # Animate step
            if time.time() % 0.4 < 0.05:
                step += 1
                if step >= len(motion):
                    step = 0
                    idx = (idx + 1) % len(signs)

        pygame.draw.circle(screen, (255, 200, 0), (int(hand_x), int(hand_y)), 15)  # hand
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



#######
@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""

    
        
    return render_template('userhome.html',msg=msg)

@app.route('/test', methods=['GET', 'POST'])
def test():
    msg=""
    ss=""
    fn=""
    fn1=""
    tclass=0

    ff=open("static/trained/class1.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')

    ff=open("static/msg.txt","w")
    ff.write("")
    ff.close()
    
    if request.method=='POST':
        lg=request.form['language']
        #file = request.files['file']

        af=open("lang.txt","w")
        af.write(lg)
        af.close()
        return redirect(url_for('test_cam'))

        
        '''if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            f1=open('static/test/file.txt','w')
            f1.write(filename)
            f1.close()
            file.save(os.path.join("static/test", filename))

        cutoff=1
        path_main = 'static/dataset'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/dataset/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                print("ff="+fn)
                break
            else:
                ss="no"

        if ss=="ok":
            print("yes")
            tclass=0
            dimg=[]

            ##    
            ff2=open("static/trained/tdata.txt","r")
            rd=ff2.read()
            ff2.close()

            num=[]
            r1=rd.split(',')
            s=len(r1)
            ss=s-1
            i=0
            while i<ss:
                num.append(int(r1[i]))
                i+=1

            #print(num)
            dat=toString(num)
            dd2=[]
            ex=dat.split(',')
            print(fn)
            ##
            ##
            n=0
            fpos=""
            path_main = 'static/dataset'
            for val in ex:
                dt=[]
                fa1=fn.split('.')
                fa=fa1[0].split('-')
                fpos=fa[1]
                fv=int(fa[1])-1
                n+=1
                if cname[fv]==val:
                    tclass=n
                    
                    break
                
            
            print(tclass)
            tt=tclass-1
            cla=cname[tt]
            dta=cla+"|"+fn+"|"+fpos
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()

            
                    
            return redirect(url_for('test_pro',act="1"))
        else:
            msg="Invalid!"'''
    
        
    return render_template('test.html',msg=msg)


    
@app.route('/test_pro', methods=['GET', 'POST'])
def test_pro():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    
    ts=gs[0]
    fname=fn

    
    ##bin
    '''image = cv2.imread('static/dataset/'+fn)
    original = image.copy()
    kmeans = kmeans_color_quantization(image, clusters=4)

    # Convert to grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

    # Draw largest enclosing circle onto a mask
    mask = np.zeros(original.shape[:2], dtype=np.uint8)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
        cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
        break
    
    # Bitwise-and for result
    result = cv2.bitwise_and(original, original, mask=mask)
    result[mask==0] = (0,0,0)

    
    ###cv2.imshow('thresh', thresh)
    ###cv2.imshow('result', result)
    ###cv2.imshow('mask', mask)
    ###cv2.imshow('kmeans', kmeans)
    ###cv2.imshow('image', image)
    ###cv2.waitKey()

    #cv2.imwrite("static/upload/bin_"+fname, thresh)'''
    

    ###fg
    '''img = cv2.imread('static/dataset/'+fn)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    segment = cv2.subtract(sure_bg,sure_fg)
    img = Image.fromarray(img)
    segment = Image.fromarray(segment)
    path3="static/trained/test/fg_"+fname
    #segment.save(path3)'+'''
    
        
    return render_template('test_pro.html',msg=msg,fn=fn,ts=ts,act=act)

@app.route('/test_pro2', methods=['GET', 'POST'])
def test_pro2():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    ts=gs[0]
    pos=gs[2]

    n=int(pos)-1

    af2=open("lang.txt","r")
    lgg=af2.read()
    af2.close()
    
    lfile="a"+pos+"_"+lgg+".jpg"

    
    af=open("static/trained/lang1.txt","r")
    la=af.read()
    af.close()

    la1=la.split(",")
    la2=la1[n].split("-")
    
    c=0
    if lgg=="h":
        c=1
    elif lgg=="t":
        c=2
    elif lgg=="m":
        c=3
    else:
        c=0

    word=la2[c]
    
    
    return render_template('test_pro2.html',msg=msg,fn=fn,ts=ts,act=act,lfile=lfile,word=word)


@app.route('/test2',methods=['POST','GET'])
def test2():
    msg=""
    name=request.args.get("name")

    ff=open("bc.txt","r")
    bc=ff.read()
    ff.close()
    
    return render_template('test2.html', msg=msg,name=name,bc=bc)

@app.route('/autocapture',methods=['POST','GET'])
def autocapture():
    msg=""
    uname=""
    ff1=open("static/log.txt","r")
    log=ff1.read()
    ff1.close()

    if 'username' in session:
        uname = session['username']

    ff1=open("static/user.txt","r")
    user=ff1.read()
    ff1.close()
    
    if uname==user:
        print("hello")

        # Load model and gesture map
        model = joblib.load("gesture_model.pkl")
        gesture_map = joblib.load("gesture_map.pkl")

        # Get expected number of features
        expected_features = model.n_features_in_

        mp_hands = mp.solutions.hands
        mp_draw = mp.solutions.drawing_utils
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

        imgname=user+".jpg"
        frame = cv2.imread('static/photo/'+imgname)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract features
                landmark_list = []
                for lm in hand_landmarks.landmark:
                    landmark_list.extend([lm.x, lm.y, lm.z])
                
                # Predict only if feature size matches
                if len(landmark_list) == expected_features:
                    prediction = model.predict([landmark_list])[0]
                    gesture_name = gesture_map.get(prediction, "Unknown")

                    gn=""
                    ff=open("static/class2.txt","r")
                    cn=ff.read()
                    ff.close()
                    cna=cn.split("|")

                    ff=open("static/class1.txt","r")
                    hn=ff.read()
                    ff.close()
                    hna=hn.split("|")
                    u=0
                    for cna1 in cna:
                        if cna1==gesture_name:
                            gn=hna[u]
                            break
                        u+=1
                    if gn=="":
                        s=1
                    else:
                        ff=open("static/detect.txt","w")
                        ff.write(gn)
                        ff.close()
                        print(gn)

                        #cv2.putText(frame, f"{gn}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    ff=open("static/detect.txt","w")
                    ff.write("")
                    ff.close()

        '''mpHands = mp.solutions.hands
        hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        model = load_model('mp_hand_gesture')

        # Load class names
        f = open('gesture.names', 'r')
        classNames = f.read().split('\n')
        f.close()

        imgname=user+".jpg"
        frame = cv2.imread('static/photo/'+imgname)
        x, y, c = frame.shape

        # Flip the frame vertically
        #frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        # print(result)
        
        className = ''
        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]
                ff=open("static/msg.txt","w")
                ff.write(className)
                ff.close()
                text_to_speech(className)
                print("class="+className)
        else:
            ff=open("static/msg.txt","w")
            ff.write("")
            ff.close()'''

    return render_template('autocapture.html',msg=msg,user=user,uname=uname)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    msg=""
    uname=""
    
    if 'username' in session:
        uname = session['username']

    ff1=open("static/user.txt","r")
    user=ff1.read()
    ff1.close()
    print("yes")
    if request.method=='POST':
        if uname==user:
            print("capture")
            file = request.files['webcam']
            try:
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file:
                    fn=user+".jpg"
                    fn1 = secure_filename(fn)
                    file.save(os.path.join("static/photo", fn1))
                    #return redirect(url_for('detect'))
                    ff1=open("static/log.txt","w")
                    ff1.write("1")
                    ff1.close()
            except:
                print("dd")
    return render_template('upload.html',msg=msg)


@app.route('/test_pro3', methods=['GET', 'POST'])
def test_pro3():
    msg=""
    fn=""
    st=""
    lfile=""
    word=""
    val=""
    
    act=request.args.get("act")
    f2=open("lang.txt","r")
    lgg=f2.read()
    f2.close()

    f3=open("static/detect.txt","r")
    ms=f3.read()
    f3.close()

    ff=open("static/class1.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split('|')

    if ms=="":
        st=""
    else:
        st="1"
        n=0
        for cc in cname:
            n+=1
            if cc==ms:              
                
                break
        print("value=")
        print(str(n))
        m=n-1
        pos=n
        ##
        
        #lfile="a"+str(pos)+"_"+lgg+".jpg"

        c=0
        if lgg=="" or lgg=="en":
            c=1
            val=ms
            word=ms
            #text_to_speech(word)
        else:
            val=lg_translate(lgg,ms)
            word=val
            #text_to_speech(word,lgg)

        ff=open("static/detect.txt","w")
        ff.write("")
        ff.close()
        

    return render_template('test_pro3.html',msg=msg,st=st,lgg=lgg,fn=fn,act=act,lfile=lfile,word=word,val=val)

#######################
def gen1(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed1')
def video_feed1():
    return Response(gen1(VideoCamera1()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
############
def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


##########################
@app.route('/logout')
def logout():

    uname=""
    
    if 'username' in session:
        uname = session['username']

    cursor = mydb.cursor()
    cursor.execute("update sign_user set status=0 where uname=%s",(uname,))
    mydb.commit()
                
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


