from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from keras.utils import np_utils
import tensorflow as tf
import matplotlib.pyplot as plt

(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()
train_images = train_images.reshape(train_images.shape[0], 32, 32, 3)
test_images = test_images.reshape(test_images.shape[0], 32, 32, 3)
train_images = train_images.astype('float32')
test_images = test_images.astype('float32')
train_images /= 255
test_images /= 255
# Normalize pixel values to be between 0 and 1

n_classes = 10
print("Shape before one-hot encoding: ", train_labels.shape)
Y_train = np_utils.to_categorical(train_labels, n_classes)
Y_test = np_utils.to_categorical(test_labels, n_classes)
print("Shape after one-hot encoding: ", Y_train.shape)
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']
# Class labels

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i])
    plt.xlabel(class_names[train_labels[i][0]])
    # The CIFAR labels happen to be arrays,
    # which is why you need the extra index
plt.show()

# I have initialized the model by specifying that it is a sequential model.
# My convolution layers provide image processing to blur and sharpen the images,
# but also to perform other operations such as enhance edges and emboss.
# The pooling layer summarizes the features present in a region of the feature
# map passed on by the convolution layers i.e., reduces the dimensions of the feature maps.
# The flattening layer is used to convert all the resultant 2-Dimensional arrays from pooled
# feature maps into a single long continuous linear vector.
# The flattened matrix is fed as input to the fully connected layer to classify the image.
# I pass the data to the dense layer so for that I flatten the vector which comes out of the convolutions.
# Moreover, I added a Rectified Linear Unit activation to all my layers
# so as to make sure that the negative values aren't passed on to the next layer.
# It is important to note that CNNs enforce a local connectivity pattern between neurons of adjacent layers.

model = Sequential()
model.add(Conv2D(50, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu', input_shape=(32, 32, 3)))
model.add(Conv2D(75, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Conv2D(125, kernel_size=(3,3), strides=(1,1), padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(500, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(250, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(10, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

history = model.fit(train_images, train_labels, batch_size=128, epochs=10,
                    validation_data=(test_images, test_labels))

# Plot of Accuracy vs. Epochs
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 0.8])
plt.legend(loc='lower right')
plt.show()

# Plot of Loss vs. Epochs
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.ylim([0.5, 0.8])
plt.legend(loc='lower right')
plt.show()

#Evaluation of the model
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print(test_acc)