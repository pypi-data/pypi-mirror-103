from keras_vggface.vggface import VGGFace
from keras.models import Model, load_model
from keras.layers import Dense,Flatten
from keras.callbacks import ModelCheckpoint , EarlyStopping
from keras.optimizers import RMSprop
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from timeit import default_timer as timer

class modelvggface():
    def __init__(self,models= ['vgg16','resnet50','senet50'],input_shape = (256,256,3),decodekey={},X=None,y=None,name="",outputpath=None):
        #all achitect avaliable ['vgg16','resnet50','senet50']
        self.outputpath = outputpath
        if self.outputpath is None:
            self.outputpath = '/content/drive/My Drive/Colab Notebooks/facelink/model output/'
        self.input_shape = input_shape
        self.keys = decodekey
        self.num_class = len(decodekey)
        self.X = X
        self.y = y
        self.models = models = [{'name':i+name,'model':self.getVggFacemodel(architect=i)}for i in tqdm(models)]
        
    #try change classifier
    def getVggFacemodel(self,architect=''):
        model = VGGFace(model=architect,weights ='vggface',include_top =False,input_shape = self.input_shape)
        if architect == 'vgg16':
            top = model.get_layer('pool5').output
        else:
            top = model.get_layer('avg_pool').output
        top = Flatten(name='flatten')(top)
        top = Dense(1024,activation='relu')(top)
        top = Dense(1024,activation='relu')(top)
        top = Dense(512,activation='relu')(top)
        output = Dense(self.num_class,activation='softmax')(top)
        Result = Model(inputs=model.input,outputs=output)
        return Result
    
    def evaluate(model,testset,label):
        start = timer()
        SA = model.evaluate(testset, label, verbose=0)
        end = timer()
        TA = end - start
        print('acc : ',SA[1]*100)
        print('time used for evaluation: ',TA)
        return SA,TA
  
    #plot_loss(h_Augment.history['loss'], h_Augment.history['val_loss'],title='Augment loss')
    def plot_loss(self,history,title='Model loss'):
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        plt.figure()
        plt.plot(loss)
        plt.plot(val_loss)
        plt.title(title)
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper right')
        plt.savefig(self.outputpath+title+'.png')
        plt.show()
    
    def TrainsTests(self,patience=7):
        output = {}
        '''if self.X == None or self.y == None:
            raise Exception('there are missing feature or label that require for training')'''
        for model in self.models:
            Model = model['model']
            checkpoint = ModelCheckpoint(self.outputpath+model['name']+'.h5',monitor='val_loss',mode='min',save_best_only=True,verbose=1)
            earlystop = EarlyStopping(patience=patience,monitor='val_loss',verbose=1)
            Model.compile(loss='categorical_crossentropy',optimizer=RMSprop(lr=0.01),metrics=['accuracy'])
            start = timer()
            #get training time
            h = Model.fit(self.X,self.y,epochs=100,callbacks=[earlystop,checkpoint],validation_split=0.2)
            end = timer()
            traintime = end-start
            for i in report:
                print(model['name'],' train history')
                plot_loss(h)
            acc, testtime = evaluate(Model,)
            output[model['name']] = {
                    'model':Model,
                    'name':model['name'],
                    'decodekey':self.keys,
                    'accuracy': acc,
                    'traintime':traintime,
                    'testtime': testtime
            }
        return output

    #ไปแปะที่ experiment ดึง traintime จาก report และ evaluation time จาก evaluation function 
    def TimeConCatsave(selfReport1,Report2,path='/content/drive/My Drive/Colab Notebooks/facelink/model output/'):
        data = pd.DataFrame(Report1).join(pd.DataFrame(Report2))
        data.loc[['time']].to_csv(path+'traintime.csv')
  
