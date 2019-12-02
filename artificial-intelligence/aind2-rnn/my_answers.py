import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # The maximum item in the series is window_size items from the end
    max_item = len(series) - window_size
    
    # Create NumPy arrays to hold the transformed series
    X = np.ndarray(shape=(max_item, window_size), dtype=series.dtype)
    y = np.ndarray(shape=(max_item, 1), dtype=series.dtype)

    # Transform the items
    for i in range(max_item):
        target = i + window_size
        
        # For X, take a slice of window_size entries
        X[i] = series[i:target]
        
        # y is simply a scalar
        y[i] = series[target]
        
    return X, y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(step_size, window_size):
    # given - fix random seed - so we can all reproduce the same results on our default time series
    np.random.seed(0)

    # TODO: build an RNN to perform regression on our time series input/output data
    model = Sequential()
    # Layer 1 with 5 hidden units and window_size inputs
    model.add(LSTM(5, input_shape=(window_size, 1)))
    # Layer 2 with a fully connected module of 1 unit
    model.add(Dense(1))

    # build model using keras documentation recommended optimizer initialization
    optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

    # compile the model
    model.compile(loss='mean_squared_error', optimizer=optimizer)
    return model

### TODO: list all unique characters in the text and remove any non-english ones
def clean_text(text):
    # find all unique characters in the text
    unique = sorted(list(set(text)))
    #print("Before: " + str(unique))

    # remove as many non-english characters and character sequences as you can 
    # we'll just keep the printable characters
    import string
    text = ''.join(filter(lambda x:x in string.printable, text))
    
    # shorten any extra dead space created above
    text = text.replace('  ',' ')

    #unique = sorted(list(set(text)))
    #print("After: " + str(unique))
    return text

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text,window_size,step_size):
    # The maximum item in the series is window_size items from the end
    max_item = len(text) - window_size
    
    inputs = []
    outputs = []

    # Transform the items, starting step_size items later each time
    for i in range(0, max_item, step_size):
        target = i + window_size
        
        # For inputs, take a slice of window_size characters
        inputs.append(text[i:target])
        
        # For outputs, take a single character
        outputs.append(text[target])
    
    return inputs,outputs