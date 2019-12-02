import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer

    for word_num in range(test_set.num_items):
        d = {}
        max_logL = -1e10
        match_word = ''

        for model_word, model in models.items():
            try:
                X, lengths = test_set.get_item_Xlengths(word_num)
                logL = model.score(X, lengths)
                d[model_word] = logL
                if logL > max_logL:
                    max_logL = logL
                    match_word = model_word
            except:
                d[model_word] = 0

        probabilities.append(d)
        guesses.append(match_word)

    return probabilities, guesses

if __name__ == "__main__":
    from  asl_test_recognizer import TestRecognize

    test_recognize = TestRecognize()
    test_recognize.setUp()
    test_recognize.test_recognize_probabilities_interface()
    test_recognize.test_recognize_guesses_interface()
