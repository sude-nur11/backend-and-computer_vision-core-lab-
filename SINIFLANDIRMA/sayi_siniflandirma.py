import numpy as np
import cv2
import os
import os
print("Current working directory:", os.getcwd())
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from keras.utils import to_categorical

# Keras 3 uyumlu ImageDataGenerator
from keras.src.legacy.preprocessing.image import ImageDataGenerator

# -----------------------------------------------------
# VERİYİ OKUMA
# -----------------------------------------------------
path1 = os.getcwd()
path = r"C:\Users\sude nur toprak\Desktop\opencv12\opencv_12\SINIFLANDIRMA\myData\myData"
print("****",path)
myList = os.listdir(path)
noOfClasses = len(myList)

print("Label(sınıf) sayısı:", noOfClasses)

images = []
classNo = []

for i in range(noOfClasses):
    myImageList = os.listdir(os.path.join(path, str(i)))
    for j in myImageList:
        img = cv2.imread(os.path.join(path, str(i), j))
        img = cv2.resize(img, (32, 32))
        images.append(img)
        classNo.append(i)

images = np.array(images)
classNo = np.array(classNo)

print("Tüm resimler:", images.shape)
print("Tüm sınıflar:", classNo.shape)

# -----------------------------------------------------
# TRAIN / TEST / VALIDATION AYIRMA
# -----------------------------------------------------

x_train, x_test, y_train, y_test = train_test_split(images, classNo, test_size=0.2, random_state=42)
x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

print("Train:", x_train.shape)
print("Validation:", x_validation.shape)
print("Test:", x_test.shape)

# -----------------------------------------------------
# PRE-PROCESS
# -----------------------------------------------------

def preProcess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img / 255
    return img

x_train = np.array(list(map(preProcess, x_train)))
x_test = np.array(list(map(preProcess, x_test)))
x_validation = np.array(list(map(preProcess, x_validation)))

x_train = x_train.reshape(-1, 32, 32, 1)
x_test = x_test.reshape(-1, 32, 32, 1)
x_validation = x_validation.reshape(-1, 32, 32, 1)

# -----------------------------------------------------
# DATA AUGMENTATION
# -----------------------------------------------------

dataGen = ImageDataGenerator(
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    rotation_range=10
)

dataGen.fit(x_train)

# -----------------------------------------------------
# ONE-HOT
# -----------------------------------------------------

y_train = to_categorical(y_train, noOfClasses)
y_test = to_categorical(y_test, noOfClasses)
y_validation = to_categorical(y_validation, noOfClasses)

# -----------------------------------------------------
# MODEL
# -----------------------------------------------------

model = Sequential()

model.add(Conv2D(8, (5, 5), activation="relu", padding="same", input_shape=(32, 32, 1)))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(16, (3, 3), activation="relu", padding="same"))
model.add(MaxPooling2D((2, 2)))

model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(256, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(noOfClasses, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="Adam", metrics=["accuracy"])

model.summary()

# -----------------------------------------------------
# EĞİTİM
# -----------------------------------------------------

batch_size = 250

hist = model.fit(
    dataGen.flow(x_train, y_train, batch_size=batch_size),
    validation_data=(x_validation, y_validation),
    epochs=15,
    steps_per_epoch=x_train.shape[0] // batch_size,
    shuffle=True
)

# -----------------------------------------------------
# MODEL KAYDETME (DOĞRU YÖNTEM)
# -----------------------------------------------------

model.save("model_trained_new.h5")
print("Model kaydedildi: model_trained_new.h5")

# -----------------------------------------------------
# EĞİTİM GRAFİKLERİ
# -----------------------------------------------------

plt.figure()
plt.plot(hist.history["loss"], label="Eğitim Loss")
plt.plot(hist.history["val_loss"], label="Val Loss")
plt.legend()
plt.show()

plt.figure()
plt.plot(hist.history["accuracy"], label="Eğitim Accuracy")
plt.plot(hist.history["val_accuracy"], label="Val Accuracy")
plt.legend()
plt.show()

# -----------------------------------------------------
# TEST DEĞERLENDİRME
# -----------------------------------------------------

score = model.evaluate(x_test, y_test, verbose=1)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# -----------------------------------------------------
# CONFUSION MATRIX
# -----------------------------------------------------

y_pred = model.predict(x_validation)
y_pred_class = np.argmax(y_pred, axis=1)
Y_true = np.argmax(y_validation, axis=1)

cm = confusion_matrix(Y_true, y_pred_class)
plt.figure(figsize=(8, 8))
sns.heatmap(cm, annot=True, cmap="Greens", fmt="d")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()
