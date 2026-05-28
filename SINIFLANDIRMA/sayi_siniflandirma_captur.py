import cv2
import numpy as np
from keras.models import load_model

# -----------------------------------------------------
# MODELİ YÜKLE
# -----------------------------------------------------
model = load_model("model_trained_new.h5")
print("Model yüklendi.")

# -----------------------------------------------------
# GÖRÜNTÜ ÖN İŞLEME
# -----------------------------------------------------
def preProcess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img / 255.0
    return img

# -----------------------------------------------------
# CAMERA
# -----------------------------------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 480)

while True:
    success, frame = cap.read()
    # frame=cv2.flip(frame,1) aklında olsun🫠
    if not success:
        print("Kamera okunamadı!")
        break

    # resize + preprocess
    img = cv2.resize(frame, (32, 32))
    img = preProcess(img)
    img = img.reshape(1, 32, 32, 1)

    # tahmin
    predictions = model.predict(img)
    classIndex = int(np.argmax(predictions))
    probVal = np.max(predictions)

    print("Tahmin:", classIndex, " | Olasılık:", probVal)

    # ekrana yazdır
    if probVal > 0.7:
        cv2.putText(
            frame,
            f"{classIndex}  {probVal:.2f}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # göster
    cv2.imshow("Rakam Siniflandirma", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
