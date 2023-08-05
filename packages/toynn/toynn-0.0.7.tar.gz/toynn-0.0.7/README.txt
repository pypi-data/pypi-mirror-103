"toynn" is a handy Neral Network model builder.

You'll be able to create a model in the desired structure with a single line of code.
Easily train, predict and visualize your model. 

"toynn" supports 'export' and 'import' of models in 'json' format.

Simple example for usage is like below.
=======================================================================
import toynn

#build a model
model = toynn.model.ANN(input_shape=(1, 784), shape = (100, 100, 100, 10), output="softmax", activation=("relu", "relu", "relu"))
model.describe()

#train
model.train(y= TRAIN_BATCH, t= ANSWER_BATCH, learning_rate=0.001, iteration=1000)

#predict
model.predict(x = INPUT)

#export model as a 'json' file to a local directory
model.export(directory = "C:\Users.......//", file_name="myModel.json")

#import model from a local directory
factory = toynn.factory.factory()
model2 = factory.make(directory = "C:\User.....\myModel.json")

=======================================================================

Updates on more types of model such as 'CNN', 'LSTM' is planned.
Thanks, and please contact the author via e-mail for any comment.