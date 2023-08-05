"toynn" is a Python based DeepLearning Framework which maximized its accessibility for DL beginners.

You can start by creating a model in any desired structure with only 3 required arguments.
Easily train, predict and visualize your model. 

"toynn" supports 'export' and 'import' function in 'json' format.
pip install is available >> "pip install toynn"

Simple example for usage is like below.
=======================================================================
import toynn

#build a model
model = toynn.model.ANN(input_shape=(1, 784), structure = (100, 100, 100, 10), output="softmax")
model.describe()  #prints how the model looks

#train
model.train(y= TRAIN_BATCH, t= ANSWER_BATCH, learning_rate=0.001, iteration=1000)

#predict
model.predict(x = INPUT)

#export model as a 'json' file to a local directory
model.export(directory = "C:\Users....\", file_name="myModel.json")

#import model from a local directory
imported_model = toynn.factory.make(file = "C:\Users.....\myModel.json")

=======================================================================

Updates on more types of model such as 'CNN', 'LSTM' is underway.
Thanks, and please contact the author via e-mail for any comment.
