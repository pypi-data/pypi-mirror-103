this is library nade for besuto and made by besuto
REFERENCE
--------------------------------------------------------------------------------------------------------------------
MTCNN   - used for face detection 
        - source : https://github.com/ipazc/mtcnn
VGGFACE - used for face feature extraction
        - papers : https://www.robots.ox.ac.uk/~vgg/publications/2018/Cao18/cao18.pdf
        - source : https://github.com/rcmalli/keras-vggface?fbclid=IwAR0wOMKDbjdQjNULYziO78RZM3dBkRJ4vCgjyZcVXffbgQYO9Ui4QDAhTIw
UPDATE LOG
--------------------------------------------------------------------------------------------------------------------
besuto 0.0.1 unfinished release to learn Pypi upload machanic

besuto 0.0.2 realease the image Augmentation function (for my school project) and face extracttion which use pretrain model in mtcnn library

besuto 0.0.3 realease the pipeline for training all VggFace model from the paper
https://www.robots.ox.ac.uk/~vgg/publications/2015/Parkhi15/parkhi15.pdf
https://www.robots.ox.ac.uk/~vgg/publications/2018/Cao18/cao18.pdf

besuto 0.0.4 fix bug that keras_application is not found

besuto 0.0.5    - fix corrupted ui in load_face_dataset function
                - fix functional type error in trains function
                
besuto 0.0.6    - fix loop massage problem in Augmentation (can be solve by add %%capture at the top of that cell in jupyter notebook)
                - write library doc and instruction (writed some of them)

besuto 0.0.7    - add faces feature extractor in augment module

besuto 0.0.8    - 0.0.7 but not bug



