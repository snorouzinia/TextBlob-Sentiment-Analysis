from textblob import TextBlob
def analyze(text) -> dict:
    #input check
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    
    stripped_text = text.strip()

    #input check
    if not stripped_text:
        raise ValueError("String cannot be empty")

    blob = TextBlob(stripped_text)
    sentiment = blob.sentiment
    return analyze_sentiment(sentiment)

def analyze_sentiment(sentiment):
    #polarity [-1,1]
    #subjectivity [0,1] 
    POS_THRESH = 0.1 #for subjectivity
    NEG_THRESH = -0.1
    polarity = "" #0 for neutral, 1 for positive, -1 for negative
    subjectivity = ""#[0, 0.5] factual and (0.5, 1] opinion based

    if sentiment.polarity < NEG_THRESH:
        polarity = "Negative"
    elif sentiment.polarity > POS_THRESH:
        polarity = "Positive"
    else:
        polarity = "Neutral"

    if sentiment.subjectivity > 0.5:
        subjectivity = "Opinion-based"
    else:
        subjectivity = "Fatual"

    return polarity, subjectivity

TEST_SENTENCES = [
    #positives
    ("I love computer science it makes me so happy!", "Positive"),
    ("Today I ate a good meal for lunch.", "Positive"),
    ("I did a great job on my quiz today, which made me happy because I studied for a long time.", "Positive"),
    ("I am having so much fun studying abroad in France!", "Positive"),

    #negatives
    ("I had a bad experience in Amsterdam last weekend.", "Negative"),
    ("Eating bananas makes my stomach hurt, but I love bananas so it makes me sad.", "Negative"),
    ("I am very stressed because I have a lot of tests coming up.", "Negative"),
    ("The stray dog got aggressive and started barking and chasing me.", "Negative"),

    #neutrals
    ("Water is necessary to survive.", "Neutral"),
    ("The sun comes up in the morning and sets at night.", "Neutral"),
    ("Blue and red combined make the color purple.", "Neutral"),
    ("Paper is made from trees.", "Neutral")
]

def tests(test_sentences):
    results = []
    correct = 0

    for i, (sentence, expected) in enumerate(test_sentences, 1):
        result, subjectivity = analyze(sentence)

        if result == expected:
            correct += 1
        
        results.append({
            "num": i,
            "sentence": sentence,
            "expected": expected,
            "result": result,
            "correct": result == expected
        })

    print(f"\n  Accuracy: {correct}/{len(test_sentences)}  ({correct/len(test_sentences)*100:.1f}%)\n")
    return results
        
def analyze_incorrect(incorrect_sentences):
    for sentence, expected, num in incorrect_sentences[:2]:
        result, _ = analyze(sentence)
        blob = TextBlob(sentence)
        sentiment = blob.sentiment
        print(f"sentence {num} had a polarity of {sentiment.polarity}")
        print(f"result: {result}, expected: {expected}")


if __name__ == "__main__":
    results = tests(TEST_SENTENCES)

    print("Analyzing 2 incorrect or uncertain predictions...")
    incorrect = []
    for result in results:
        value = result["correct"]
        if value != True:
            incorrect.append([result["sentence"], result["expected"], result["num"]])
    
    analyze_incorrect(incorrect)

