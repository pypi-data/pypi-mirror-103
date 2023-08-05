"toynn" is a handy Neral Network model builder.

You'll be able to create a model in the desired structure with a single line of code.
Easily train, predict and visualize your model. 

"toynn" supports 'export' and 'import' of models in 'json' format.

</n></n>

Simple example for usage is like below.
</n>
=======================================================================
import toynn

#build a model</n>
model = toynn.model.ANN(input_shape=(1, 784), shape = (100, 100, 100, 10), output="softmax", activation=("relu", "relu", "relu"))</n>
model.describe()</n></n>

#train</n>
model.train(y= TRAIN_BATCH, t= ANSWER_BATCH, learning_rate=0.001, iteration=1000)</n></n>

#predict</n>
model.predict(x = INPUT)</n></n>

#export model as a 'json' file to a local directory</n>
model.export(directory = "C:\Users.......//", file_name="myModel.json")</n></n>

#import model from a local directory</n>
factory = toynn.factory.factory()</n>
model2 = factory.make(directory = "C:\User.....\myModel.json")</n></n>

=======================================================================

Updates on more types of model such as 'CNN', 'LSTM' is planned.
Thanks, and please contact the author via e-mail for any comment.

#current issues
- 'batch_normalization'
- 'dropout'
- official documentation