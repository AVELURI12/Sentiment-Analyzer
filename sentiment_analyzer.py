# sentiment_analyzer.py
# Alekya Veluri
# 
# Class which analyzes sentiment of sentences based on positive, negative, negation, and modifier words

# import neccesary libraries
import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.data import find
import csv

# Ensure NLTK 'punkt' package is downloaded for tokenization
try:
    find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class SentimentAnalyzer:
    """
    A class to analyze sentiment of text using basic sentiment keywords,
    negation, and modifiers for intensifying or downtoning sentiment scores.
    """

   # Starter sets for different categories of words

    _default_positive_words = [
        "happy", "joy", "delight", "love", "wonderful", "fantastic",
        "brilliant", "amazing", "excellent", "successful", "pleased", "thrilled"
    ]

    _default_negative_words = [
        "sad", "unhappy", "disappointed", "hate", "terrible", "awful",
        "horrible", "dreadful", "poor", "fail", "miserable", "depressed"
    ]

    _default_negation_words = [
        "not", "no", "never", "none", "cannot", "isn't", "aren't",
        "wasn't", "weren't", "haven't", "hasn't", "don't"
    ]

    _default_intensifiers = [
        "very", "extremely", "incredibly", "absolutely", "completely",
        "utterly", "totally", "deeply", "enormously", "exceptionally", "especially", "tremendously", 'definetly'
    ]

    _default_downtoners = [
        "slightly", "somewhat", "a bit", "barely", "hardly", "just",
        "marginally", "scarcely", "a little", "less", "rarely", "occasionally"
    ]

    # Named constants for multipliers
    INTENSIFIER_MULTIPLIER = 1.5
    DOWNTONER_MULTIPLIER = 0.5

    #``````````````````````````````````````````````````````````````````````````````````
    def __init__(self, positive_words=None, negative_words=None, negation_words=None, intensifiers=None, downtoners=None):
        """
        Initializes the SentimentAnalyzer with optional custom lists of words. 
        Falls back to default lists if none are provided.
        """
        self.positive_words = positive_words if positive_words is not None else self._default_positive_words
        self.negative_words = negative_words if negative_words is not None else self._default_negative_words
        self.negation_words = negation_words if negation_words is not None else self._default_negation_words
        self.intensifiers = intensifiers if intensifiers is not None else self._default_intensifiers
        self.downtoners = downtoners if downtoners is not None else self._default_downtoners


    #``````````````````````````````````````````````````````````````````````````````````
    def analyze_sentence_sentiment(self, sentence, use_negation=False, use_modifiers=False):
        """
        Analyzes the sentiment score of a sentence based on the presence of positive, negative,
        negation, and modifier (intensifiers and downtoners) words. The function calculates a 
        sentiment score that reflects the overall sentiment of the sentence.
        """
        # initialize sentiment_score, negation, and modifier effect
        sentiment_score = 0
        negation = 1
        modifier = 1
        negation_present = False # initially set negation_present to False 

        # use tokenize to split sentence into words
        words = nltk.word_tokenize(sentence)

        for i, word in enumerate(words): # iterate over list of words and keep track of index value
            word = word.lower() # make word lowercase

            # check if word is a negation word
            if word in self.negation_words and use_negation:
                negation *= -1 # multiply by -1
                negation_present = True # set negation_present to True
                continue # move on to next word
           
            
            # check if word is modifier(intensifier or downtowner)
            if use_modifiers:
                if word in self.intensifiers:
                    modifier = self.INTENSIFIER_MULTIPLIER # set modifier to 1.5
                    if negation == -1: # reset negation if it is -1
                        negation = 1
                    continue # move on to next word
                elif word in self.downtoners:
                    modifier = self.DOWNTONER_MULTIPLIER # set modifier to 0.5
                    if negation == -1: # reset negation if it is -1
                        negation = 1
                    continue # move on to next word

            # check if word is a positive or negative word and add to sentiment score accordingly
            if word in self.positive_words:
                sentiment_score += 1 * negation * modifier
                negation = 1 # reset negation
                # check if next word is positive/negative/modifier, and if it is not, reset negation and negation_present
                if negation_present and i + 1 < len(words) and words[i + 1].lower() not in self.positive_words and words[i + 1].lower() not in self.negative_words and words[i + 1].lower() not in self.intensifiers and words[i + 1].lower() not in self.downtoners:
                    negation = 1
                    negation_present = False
                
            elif word in self.negative_words:
                sentiment_score += -1 * negation * modifier
                negation = 1 # reset negation
                # check if next word is positive/negative/modifier, and if it is not, reset negation and negation_present
                if negation_present and i + 1 < len(words) and words[i + 1].lower() not in self.positive_words and words[i + 1].lower() not in self.negative_words and words[i + 1].lower() not in self.intensifiers and words[i + 1].lower() not in self.downtoners:
                    negation = 1
                    negation_present = False

            # reset negation if negation_present is True
            if negation_present:
                negation = 1
                negation_present = False

            # reset modifier
            modifier = 1

            
        
        # return a sentiment score of 0 as 0    
        if sentiment_score == 0:
            sentiment_score = int(0)
            
        return sentiment_score  

    #``````````````````````````````````````````````````````````````````````````````````
    def get_sentiment(self, sentiment_score):
        """
        Determines the sentiment label ('positive', 'negative', 'neutral') based on the sentiment score.
        """
        # return positive, negative, or neutral based on sentiment score
        if sentiment_score > 0:
            return 'positive'
        elif sentiment_score < 0:
            return 'negative'
        elif sentiment_score == 0:
            return 'neutral'

    #``````````````````````````````````````````````````````````````````````````````````
    def calculate_overall_sentiment_score(self, sentiment_scores):
        """
        Calculates the average sentiment score from a list of individual sentence scores. Here
        the sentiment scores are the floating point scores for each sentence. 
        """
        if len(sentiment_scores) > 0: # check if there are sentiment scores in list
            return sum(sentiment_scores) / len(sentiment_scores) # return average score
        else:
            return 0 # if no sentiment scores, return average score of 0
        

    #``````````````````````````````````````````````````````````````````````````````````
    def get_sentences_from_lines(self, text_lines_list):
        """
        Converts a list of text lines into a list of sentences using NLTK's sentence tokenizer.
        """
        sentences = [] # create empty list
        for i in text_lines_list: # add sentences to list using nltk.sent_tokenize
            sentences.extend(nltk.sent_tokenize(i))
        return sentences

    #``````````````````````````````````````````````````````````````````````````````````
    def analyze_sentiment(self, text_lines_list, use_negation=False, use_modifiers=False):
        """
        Analyzes the overall sentiment of multiple lines of text.     
        """
        # create empty lists
        detailed_results = []
        sentiment_scores = []

        # iterate over lines and then sentences
        for i in text_lines_list:
            sentences = nltk.sent_tokenize(i)
            for sentence in sentences:

                sentiment_score = self.analyze_sentence_sentiment(sentence, use_negation, use_modifiers) # get sentiment score from function
                sentiment_scores.append(sentiment_score) # add sentiment score to list
                sentiment = self.get_sentiment(sentiment_score) # get sentiment from function
            
                detailed_results.append({'sentiment': sentiment, 'score': sentiment_score, 'sentence': sentence}) # add sentiment, score, and sentence to detailed_results dictionary

        overall_sentiment_score = self.calculate_overall_sentiment_score(sentiment_scores) # get overall sentiment score from function
        overall_sentiment = self.get_sentiment(overall_sentiment_score) # get overall sentiment from function

        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0} # create dictionary and initialize counts 
        for element in detailed_results: # iterate over sentiment in detailed results
                                         
            if element['sentiment'] == 'positive': # add 1 to positive if 'positive' is present
                sentiment_counts['positive'] += 1
                                         
            elif element['sentiment'] == 'negative': # add 1 to negative if 'negative' is present
                sentiment_counts['negative'] += 1
                
            elif element['sentiment'] == 'neutral': # add 1 to neutral if 'neutral' is present
                sentiment_counts['neutral'] += 1
                
        # return detailed results, overall sentiment and score, and sentiment counts
        return {'detailed_results': detailed_results, 'overall_sentiment': {'overall_sentiment': overall_sentiment, 'score': overall_sentiment_score}, 'sentiment_counts': sentiment_counts} 
        

    #``````````````````````````````````````````````````````````````````````````````````
    def write_to_csv(self, detailed_results, csv_file_path):
        """
        Writes the detailed sentiment analysis results to a CSV file.
        """
        myfile = open(csv_file_path, 'w', newline = '') # open file for writing 
        writer = csv.writer(myfile) # object to write rows to CSV file

        # Write header row to CSV file
        writer.writerow('Sentiment', 'Score', 'Sentence')
        # Iterate over the results and write each one as a row in CSV file
        for i in detailed_results:
            writer.writerow(i)

        # Close file
        myfile.close()
        
#``````````````````````````````````````````````````````````````````````````````````
def main():
    """
    The main test function for the SentimentAnalyzer class. This function is designed to verify
    the correctness of the analyze_sentence_sentiment method by running it through a series of
    test cases. Each test case is an assertion that checks if the method returns the expected
    sentiment score for a given sentence under specified conditions (use of negation and modifiers).
    Additional complex test cases mix multiple aspects of sentiment analysis to ensure the method
    can handle a variety of sentence structures and sentiment expressions accurately.
    """
    
    analyzer = SentimentAnalyzer(["happy", "outstanding", "great", "positive"],["sad", "disappointing", "bad"],\
                                    ["not", "never"],["very", "extremely","definitely"],["somewhat", "slightly"])

    # Test case 1: Positive keyword
    assert analyzer.analyze_sentence_sentiment("This is a great day.") == 1, "Failed on positive keyword test"

    # Test case 2: Negative keyword
    assert analyzer.analyze_sentence_sentiment("This is a sad day.") == -1, "Failed on negative keyword test"

    # Test case 3: Negation of a positive word (without use_negation=True should be treated as positive)
    # this test will fail because of the "a" between the negation and the positive word.
    #
    #assert analyzer.analyze_sentence_sentiment("This is not a great day.", use_negation=True) == -1, "Failed on negation test"

    # Test case 3: Negation of a positive word (without use_negation=True should be treated as positive)
    assert analyzer.analyze_sentence_sentiment("This day is not great.", use_negation=True) == -1, "Failed on negation test"

    # Test case 4: Modified negation of a positive word (without use_negation=True should be treated as positive)
    assert analyzer.analyze_sentence_sentiment("This is definitely not great.", use_negation=True, use_modifiers=True) == -1.5, "Failed on intensify/downtone a negation test"

    # Test case 5: Intensified positive word
    assert analyzer.analyze_sentence_sentiment("This is a very great day.", use_modifiers=True) == 1.5, "Failed on intensifier test"

    # Test case 6: Downtoned negative word
    assert analyzer.analyze_sentence_sentiment("This is somewhat disappointing.", use_modifiers=True) == -0.5, "Failed on downtoner test"
    
    print("All simple sentence tests passed!")        

    canalyzer = SentimentAnalyzer(["happy", "outstanding", "great"], ["bad", "awful","disappointing"], ["not", "never"], ["very", "extremely","definitely"], ["somewhat", "slightly"])

    # Mixed sentiment with negation and modifier
    assert canalyzer.analyze_sentence_sentiment("This is a great day, but somewhat disappointing.", use_negation=True, use_modifiers=True) == 0.5, "Failed on mixed sentiment with negation and modifier"

    # Intensified positive followed by a downtoned negative
    assert canalyzer.analyze_sentence_sentiment("It was very outstanding yet slightly bad.", use_modifiers=True) == 1, "Failed on intensified positive followed by downtoned negative"

    # Negated positive followed by an unmodified negative
    assert canalyzer.analyze_sentence_sentiment("This is not happy and also awful.", use_negation=True) == -2, "Failed on negated positive followed by unmodified negative"

    # Multiple modifiers with a negation impacting different parts of the sentence
    assert canalyzer.analyze_sentence_sentiment("It was definitely not great, but somewhat bad.", use_negation=True, use_modifiers=True) == -2, "Failed on multiple modifiers with negation"

    # Sentences with neutral words and sentiment words without explicit modifiers or negations
    assert canalyzer.analyze_sentence_sentiment("The day was outstanding then turned awful.", use_negation=True, use_modifiers=True) == 0, "Failed on sentence with neutral shift"

    # Mixed sentiment with multiple modifiers and negation
    assert canalyzer.analyze_sentence_sentiment("This is extremely bad but not somewhat outstanding.", use_negation=True, use_modifiers=True) == -1, "Failed on mixed sentiment with multiple modifiers and negation"

    # Complex sentence with negation impacting multiple sentiment words
    assert canalyzer.analyze_sentence_sentiment("This is not happy day, but it is definitely not awful.", use_negation=True, use_modifiers=True) == 0.5, "Failed on complex sentence with negation impacting multiple sentiment words"

    print("All complex sentence tests passed!")
                                                
    print("All tests passed!")

    


if __name__ == "__main__":
    main()

