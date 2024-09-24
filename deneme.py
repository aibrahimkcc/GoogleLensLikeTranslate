#Requierments
import easyocr
import cv2
import os
from google.cloud import translate_v2 as translate
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\KCC\Downloads\googleapi.json"

# çeviri özelliği
## hedef dil 'en','tr','ja','it'
translate_client = translate.Client()
def translate_text(text, target_language='en'):
        if isinstance(text, bytes):
            text = text.decode("utf-8")
        result = translate_client.translate(text, target_language=target_language)  
        return result['translatedText']



# tanınması isteniln dil 'tr' japanese:'ja' 'en','es'# 
reader = easyocr.Reader(['tr'],gpu=True)

## read images for directory
##can change to jpg too but it ll be longer
image_dir = './frames'
edited_image_dir = './editedframes'
image_files = sorted([f for f in  os.listdir(image_dir) if f.endswith('.png')])

# Iterate over the images and read them
count = 0
savedText=[]

for file in image_files:
    ##Ocr 24 kare'de bir çalışır ve çevri 1 kez gerçekleşir.
    ##count 1 yaplırak her resim için çeviri gerçekleştirilebilir.
    if count%24 == 0:
        savedText.clear()
        image_path = os.path.join(image_dir, file)
        img = cv2.imread(image_path)
    

        text_ = reader.readtext(img)
        
        ##threshold namı diğer eşik
        threshold = 0.30
        for t in text_:

            bbox, text, score=t
            if score > threshold:
                topleftcorner = [int(x) for x in bbox[0]]
                bottomrightcorner = [int(x) for x in bbox[2]]
                bottomleftcorner= [int(x) for x in bbox[3]]
                bottomleftcorner[1]-= 5

                
                text = translate_text(text)
                savedText.append((topleftcorner, bottomrightcorner, bottomleftcorner, text))
                cv2.rectangle(img, topleftcorner, bottomrightcorner, (0,0,0),-1)
                cv2.putText(img, text, bottomleftcorner, cv2.FONT_HERSHEY_SIMPLEX, 0.53 ,(0,255,0), 2)



        
    else:
        image_path = os.path.join(image_dir, file)
        img = cv2.imread(image_path)
        for t in savedText:
            topleftcorner, bottomrightcorner,bottomleftcorner,text = t
            cv2.rectangle(img, topleftcorner, bottomrightcorner, (0,0,0), -1)
            cv2.putText(img, text, bottomleftcorner, cv2.FONT_HERSHEY_SIMPLEX, 0.53 ,(0,255,0), 2)

    count+=1
    save_path = os.path.join(edited_image_dir,'edited'+file)
    cv2.imwrite(save_path,img)
