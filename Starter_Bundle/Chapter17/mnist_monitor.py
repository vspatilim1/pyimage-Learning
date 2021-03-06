# set the matplotlib backend so figures can be saved in the background
import matplotlib
matplotlib.use('Agg')

# import the necessary packages
from siddhantbansal.callbacks import TrainingMonitor
from sklearn.preprocessing import LabelBinarizer
from siddhantbansal.nn.conv import MiniVGGNet
from keras.optimizers import SGD
from keras.datasets import mnist
import argparse
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-o', '--output', required=True, help='path to the output directory')
args = vars(ap.parse_args())
output = args['output']

# show information on the process ID
print('[INFO] process ID: {}'.format(os.getpid()))

# load the training and testing data
print('[INFO] loading MNIST data...')
((trainX, trainY), (testX, testY)) = mnist.load_data()
trainX = trainX.astype('float') / 255.0
testX = testX.astype('float') / 255.0
trainX = trainX.reshape(60000, 28, 28, 1)
testX = testX.reshape(10000, 28, 28, 1)

# convert the lables from integers to vectors
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.fit_transform(testY)

# initialize the label names
labelNames = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# initlaize the SGD optimizer, but witout any learning rate decay
print('[INFO] compiling model...')
opt = SGD(lr=0.01, momentum=0.9, nesterov=True)
model = MiniVGGNet.build(width=28, height=28, depth=1, classes=10)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# construct the set of callbacks
figPath = os.path.sep.join([output, '{}.png'.format(os.getpid())])
jsonPath = os.path.sep.join([output, '{}.json'.format(os.getpid())])
callbacks = [TrainingMonitor(figPath, jsonPath=jsonPath)]

# train the network
print('[INFO] training network...')
model.fit(trainX, trainY, validation_data=(testX, testY), batch_size=64, epochs=100, callbacks=callbacks, verbose=1)
