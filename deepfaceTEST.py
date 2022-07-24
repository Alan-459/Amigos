import DeepFace as df
import matplotlib.pyplot as plt
model = {}
model['emotion'] = df.build_model('Emotion')
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
# obj = df.analyze(img_path = 'emot.jfif',actions=['emotion'],models=model{'emotion'})
# print(obj)
#realtime 287-- commented gender and age prediction
#removed loading of other models as well
# obj2 = df.stream(db_path='Database',source=0,time_threshold=2,enable_face_analysis=True,model_name='DeepFace',frame_threshold=2)
print(plt.style.available())
obj3 = df.stream(source=0,time_threshold=1,model_name=models[2],frame_threshold=1,enable_face_analysis=True,distance_metric='euclidean',detector_backend = 'opencv') 
print(f'list is {obj3}')

obj2 = {'Sad': 0.5917060708008964, 'Happy': 0.061880612261741276, 'Neutral': 0.3464133169373622}
plt.style.use(plt.style.available[17])
labels = list(obj2.keys())
values = list(obj2.values())
plt.pie(values,labels=labels)
plt.show()