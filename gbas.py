# gbas.py 
# Alekya Veluri
# 
# Takes a text as input, extracts lines and chapters and computes sentiment score using SentimentAnalyzer. Calculates moving average and plots results.

# import necessary libraries and Sentiment Analyzer
import sys
import csv
from sentiment_analyzer import SentimentAnalyzer
import matplotlib.pyplot as plt

#``````````````````````````````````````````````````````````````````````````````````
# words for analysis  
starter_positive_words = [
    "happy", "joy", "delight", "love", "wonderful", "fantastic",
    "brilliant", "amazing", "excellent", "success", "pleasure", 
    "positive", "scrupulous", "ingenious", "cordial", "gratify",
    "endear", "genius", "propriety", "wit", "solicitude", "amiable",
    "soberly", "earnest", "obliging", "stately", "jovial", "amicable",
    "magnanimous", "prudent", "affable", "stalwart", "propitious", "weal"  
]

starter_negative_words = [
    "sad", "anger", "disappoint", "hate", "terrible", "awful",
    "horrible", "worse", "worst", "negative", "failure", "bad",
    "vex", "affectation", "haughty", "supercilious", "mortified",
    "impertinent", "contempt", "detestable", "folly", "libel",
    "impertinent","impetuous", "mortified", "frivolous", "unbecoming",
    "indolent", "chagrin", "morose", "untoward", "contrite"    
]

starter_negation_words = [
    "not", "never", "no", "nothing", "nowhere", "none",
    "cannot", "can't", "don't", "isn't", "aren't", "wasn't"
]

starter_intensifiers = [
    "very", "extremely", "incredibly", "absolutely", "completely",
    "utterly", "highly", "totally", "exceptionally", "especially", 
    "extraordinarily", "most", "really", "quite", "vastly", "excessively"
]

starter_downtoners = [
    "slightly", "somewhat", "a bit", "barely", "hardly", "just",
    "less", "little", "marginally", "rarely", "scarcely", "sparsely"
]


#``````````````````````````````````````````````````````````````````````````````````
# function which extracts lines from text and returns list of lines

def extract_gutenberg_text(lines):
    start_phrase = "*** START OF THE PROJECT GUTENBERG EBOOK" # assign start phrase
    end_phrase = "*** END OF THE PROJECT GUTENBERG EBOOK" # assign end phrase
    start_index = None
    end_index = None

    # Find the start and end indexes
    for i, line in enumerate(lines): # iterate over lines and keep track of index
        if line.strip().startswith(start_phrase): # check if line has start phrase
            start_index = i + 1  # Start after the line with the start phrase
        elif line.strip().startswith(end_phrase): # check if line has end phrase
            end_index = i  # End before the line with the end phrase
            break

    # Extract and return the lines between start and end indexes
    if start_index is not None and end_index is not None:
        return lines[start_index:end_index]
    else:
        # Return an empty list if the start or end phrases are not found
        return []

#``````````````````````````````````````````````````````````````````````````````````
# function which returns chapters that have clear markings
def extract_chapters_from_gutenberg_lines(lines, epilogue="Epilogue"):
    chapters = {} # create empty dictionary for chapters
    current_chapter = ""
    chapter_lines = [] # create empty list for chapter lines
    in_chapter = False

    for line in lines: # iterate over lines
        # Check for chapter start
        if line.strip().startswith("CHAPTER") or line.strip() == epilogue:
            # Save the previous chapter if it exists
            if in_chapter and current_chapter:
                chapters[current_chapter] = chapter_lines # chapter name is key and the lines are value
                chapter_lines = [] # reset chapter lines
            current_chapter = line.strip()
            in_chapter = True # set to True when in new chapter
        elif in_chapter: # if still in same chapter
            chapter_lines.append(line) # add lines to list

    # Add the last chapter if it exists
    if in_chapter and current_chapter:
        chapters[current_chapter] = chapter_lines

    return chapters # return dictionary

#``````````````````````````````````````````````````````````````````````````````````
# function which processes texts that do not have clear chapter bounderies.
# It will give an equal division of lines based  on the number of lines_per_chater that you pass in. 
def create_fake_chapters(lines, lines_per_chapter):
    """
    This function takes a list of lines from a text and divides it into fake chapters
    based on a specified number of lines per chapter.
    Each chapter is given a sequential title (Chapter 1, Chapter 2, etc.), and the lines are distributed accordingly.
    """
    chapters = {} # create empty dictionary
    chapter_count = 1 # initilaize chapter count to 1
    for i in range(0, len(lines), lines_per_chapter): # iterate over lines through an even distribution
        chapter_title = f"Chapter {chapter_count}" # assign title of chapter
        chapters[chapter_title] = lines[i:i + lines_per_chapter] # assign key and value to dictionary
        chapter_count += 1 # increment chapter count
    return chapters # dictionary with chapter titles as keys and lists of lines as values

#``````````````````````````````````````````````````````````````````````````````````
# function will plot sentiment for two sets of scores.

def plot_dual_sentiment(results1, results2, label1='First Analysis', label2='Second Analysis', xlabel="Sentence Index", title="Title"):
    plt.figure(figsize=(10, 6))
    
    # 'results1' and 'results2' are the lists of numeric scores to plot
    plt.plot(results1, marker='o', linestyle='-', color='blue', label=label1) # first analysis
    plt.plot(results2, marker='o', linestyle='-', color='green', label=label2) # second analysis
    
    plt.title(f'Sentiment Trend Comparison\n{title}') # create plot title, have overall title and additional title
    plt.xlabel('Chapter Index') # x axis
    plt.ylabel('Sentiment Score') # y axis
    plt.legend() # show legend
    plt.grid(True) # show grid
    plt.show() # show graph


#``````````````````````````````````````````````````````````````````````````````````
# function which will compute the moving average of a list of values.

def moving_average(values, window_size=20):
    """Calculate the moving average of a list of values given a window size."""
    averages = [] # create empty list for averages
    for i in range(len(values)): # iterate over the length of the list
        if i+1 < window_size:
            # Not enough data points to calculate the average, append None or keep as is
            averages.append(None)
        else:
            # Calculate the moving average
            averages.append(sum(values[i-window_size+1:i+1]) / window_size)
    return averages # return list of scores
    

#``````````````````````````````````````````````````````````````````````````````````
# main script for this analyzer

def main():
    # simulate command line arguments, pass in texts that need to be analyzed
    sys.argv = ['gbas.py', 'Pride and Prejudice.txt', 'Little Women.txt', 'Sense and Sensibility.txt'] 
    if len(sys.argv) < 4: # print usage statement
        print("Usage: python final_project.py <path_to_file1> <path_to_file2> <path_to_file3>")
        sys.exit(1)

    # call sentiment analyzer
    analyzer = SentimentAnalyzer(starter_positive_words, starter_negative_words, starter_negation_words, starter_intensifiers, starter_downtoners)
    for i in range(1,4): # go through each text file
        file = open(sys.argv[i],"r") # open file for reading
        lines = file.readlines(); # get lines
        file.close # close file
        glines = extract_gutenberg_text(lines) # use function to get list of lines and assign variable to this

        # Using the extract_chapters_from_gutenberg method to get chapters
        # and get sentiment results using the chapters
        gutlines = extract_chapters_from_gutenberg_lines(glines)
        gutresults = [analyzer.analyze_sentiment(text, True, True)['overall_sentiment']['score'] for text in gutlines.values()]

        # integer division to approximate the lines per chapter by looking at the number
        # of chapters extracted by the gutenberg chapter method
        lines_per_chapter = len(glines) // len(gutresults)

        # Create fake chapters with some number of lines per chapter
        # and get sentiment results using fake chapters
        fakelines = create_fake_chapters(glines,lines_per_chapter)
        fakeresults = [analyzer.analyze_sentiment(text, True, True)['overall_sentiment']['score'] for text in fakelines.values()]

        # Create two labels, one for each of the results
        lbl1 = "Chapters from Gutenberg"
        lbl2 = f"Chapters with {lines_per_chapter} lines per chapter"

        # plot both sentiment values using the same plot window
        ma1 = moving_average(gutresults)
        ma2 = moving_average(fakeresults)

        # Create title using text file name and remove '.txt.'
        title = str(sys.argv[i].replace('.txt', ''))

        # plot results
        plot_dual_sentiment(ma1, ma2,lbl1 ,lbl2, "Chapter Index", title)
        
if __name__ == "__main__":
    main()
