from . import models
import pickle
import numpy as np





model = pickle.load(open('main/model.pkl', 'rb'))
def predict_body_fat(model, X_test):
    density = model.predict(X_test)
    fat = ((4.95/density[0]) - 4.5)*100
    return fat 
    
X_test = [26,	37.4,	101.8,	86.4,	101.2,	60.1,	37.3,	22.8,	32.4,	29.4,	18.2,	24.9]
X_test = np.array(X_test)
data = models.Enquiry.objects.values_list('age', 'neck', 'chest', 'abdomen', 'hip', 'thigh', 'knee', 'ankle', 'biceps', 'forearm', 'wrist', 'bmi')
data = np.array(data)

print(data)