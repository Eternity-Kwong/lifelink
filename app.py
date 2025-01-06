from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# Define the dictionary of words and their alternatives
paraphrasing_dict = {
    "stupid": {
        "parent_to_teen": ["thoughtless", "misinformed", "not well-thought-out", "silly", "short-sighted", "unfocused", "uninformed"],
        "teen_to_parent": ["misguided", "confused", "disoriented", "not thinking clearly", "illogical", "not considering", "off-track"]
    },
    "lazy": {
        "parent_to_teen": ["unmotivated", "not in the mood", "unproductive", "uninspired", "reluctant", "slow-moving", "unfocused"],
        "teen_to_parent": ["tired", "unfocused", "drained", "uninspired", "feeling off", "unengaged", "a bit low-energy"]
    },
    "messy": {
        "parent_to_teen": ["disorganized", "cluttered", "unarranged", "untidy", "chaotic", "unstructured", "scrambled", "unkept"],
        "teen_to_parent": ["disorganized", "unclean", "untidy", "unarranged", "cluttered", "uncoordinated", "disordered"]
    },
    "useless": {
        "parent_to_teen": ["unhelpful", "ineffective", "not useful in this situation", "unnecessary", "pointless", "redundant", "insignificant"],
        "teen_to_parent": ["not helpful", "unnecessary", "irrelevant", "pointless", "unproductive", "not contributing", "unimportant"]
    },
    "boring": {
        "parent_to_teen": ["uninspiring", "dull", "lacking energy", "unexciting", "monotonous", "stale", "dull-witted", "flat"],
        "teen_to_parent": ["unexciting", "uninteresting", "repetitive", "lackluster", "stale", "monotonous", "dry"]
    },
    "idiot": {
        "parent_to_teen": ["misguided", "not thinking clearly", "having a rough time", "confused", "disoriented", "in the wrong mindset", "off-track"],
        "teen_to_parent": ["misunderstood", "confused", "inexperienced", "misguided", "uncertain", "uninformed", "not seeing the bigger picture"]
    },
    "shut up": {
        "parent_to_teen": ["let's take a break", "maybe we can talk later", "could we have a calm conversation?", "let's be quiet for a moment", "please stop talking"],
        "teen_to_parent": ["I need some space", "can we talk later?", "let's take a moment", "let's pause for now", "I need a break"]
    },
    "hate": {
        "parent_to_teen": ["dislike", "strongly disagree", "don’t feel positively about", "not a fan", "have negative feelings towards", "feel frustrated with", "not fond of"],
        "teen_to_parent": ["not a fan", "disagree strongly", "don’t feel positively about", "frustrated with", "feel disconnected", "not in agreement with"]
    },
    "dumb": {
        "parent_to_teen": ["not very smart", "not the best idea", "you could rethink that", "a little misinformed", "a little misguided", "underthought", "incorrect"],
        "teen_to_parent": ["misinformed", "ill-advised", "underconsidered", "not well thought-out", "not practical", "unrealistic", "not the best plan"]
    },
    "annoying": {
        "parent_to_teen": ["frustrating", "a little overwhelming", "distracting", "irritating", "exasperating", "tedious", "a bit of a hassle", "nagging"],
        "teen_to_parent": ["frustrating", "irritating", "exasperating", "a bit much", "overwhelming", "nagging", "distracting"]
    },
    "stressed": {
        "parent_to_teen": ["overwhelmed", "feeling pressured", "under pressure", "feeling burdened", "having a lot to handle", "in a tough spot", "a bit overloaded"],
        "teen_to_parent": ["feeling overwhelmed", "stressed out", "under pressure", "a lot to handle", "feeling burdened", "in a rough spot"]
    },
    "angry": {
        "parent_to_teen": ["upset", "frustrated", "annoyed", "irritated", "disappointed", "distressed", "displeased", "exasperated"],
        "teen_to_parent": ["irritated", "upset", "frustrated", "angry", "disappointed", "distressed", "peeved"]
    },
    "sad": {
        "parent_to_teen": ["down", "feeling low", "disheartened", "disappointed", "gloomy", "in a slump", "not feeling great", "blue"],
        "teen_to_parent": ["down", "not feeling well", "low", "disheartened", "feeling off", "a bit blue", "in a slump"]
    },
    "ugly": {
        "parent_to_teen": ["unappealing", "not attractive", "unpleasant to the eyes", "not aesthetically pleasing", "unattractive", "lacking charm", "not eye-catching"],
        "teen_to_parent": ["unappealing", "not very attractive", "plain", "unlovely", "not pleasing to the eye", "lacking charm", "not very fashionable"]
    },
    "gross": {
        "parent_to_teen": ["unpleasant", "disgusting", "not pleasant", "off-putting", "icky", "unappetizing", "not appetizing", "unappealing"],
        "teen_to_parent": ["disgusting", "unpleasant", "gross", "nasty", "icky", "off-putting", "unappealing"]
    },
    "weird": {
        "parent_to_teen": ["unusual", "quirky", "out of the ordinary", "different", "unique", "eccentric", "unconventional", "odd"],
        "teen_to_parent": ["different", "unique", "unconventional", "out of the box", "eccentric", "unusual", "quirky"]
    },
    "fat": {
        "parent_to_teen": ["overweight", "carrying extra weight", "larger", "a bit fuller", "not at your healthiest", "out of shape", "not as fit as you could be"],
        "teen_to_parent": ["larger", "overweight", "a bit fuller", "not at your healthiest", "out of shape", "not as fit"]
    },
    "skinny": {
        "parent_to_teen": ["slender", "lean", "light build", "thin", "in good shape", "slim", "underweight", "small-framed"],
        "teen_to_parent": ["slender", "thin", "lean", "slim", "small-framed", "in good shape", "light build"]
    },
    "poor": {
        "parent_to_teen": ["economically challenged", "financially struggling", "not rich", "in a tough financial spot", "living paycheck to paycheck", "struggling with money", "not well-off"],
        "teen_to_parent": ["struggling financially", "economically challenged", "not well-off", "in a tight spot", "financially limited", "living paycheck to paycheck"]
    },
    "rich": {
        "parent_to_teen": ["wealthy", "financially secure", "well-off", "comfortable", "prosperous", "affluent", "financially stable", "loaded"],
        "teen_to_parent": ["wealthy", "financially secure", "well-off", "prosperous", "comfortable", "affluent", "stable"]
    },
    "weak": {
        "parent_to_teen": ["not strong", "a bit fragile", "fragile", "lacking strength", "a bit feeble", "not robust", "underpowered", "not resilient"],
        "teen_to_parent": ["fragile", "not strong", "not as resilient", "a bit fragile", "not robust", "lacking strength"]
    },
    "strong": {
        "parent_to_teen": ["powerful", "resilient", "tough", "robust", "muscular", "solid", "forceful", "tough as nails"],
        "teen_to_parent": ["strong", "resilient", "powerful", "tough", "solid", "robust", "tough as nails"]
    },
    "slow": {
        "parent_to_teen": ["taking your time", "not fast", "deliberate", "methodical", "not in a rush", "unhurried", "leisurely", "steady"],
        "teen_to_parent": ["taking your time", "slow-moving", "methodical", "deliberate", "not in a rush", "unhurried", "steady"]
    },
    "fast": {
        "parent_to_teen": ["quick", "rapid", "speedy", "swift", "on the go", "zippy", "quick-witted", "accelerated"],
        "teen_to_parent": ["quick", "speedy", "rapid", "swift", "on the go", "accelerated", "zippy"]
    },
    "awkward": {
        "parent_to_teen": ["uncomfortable", "a little off", "uneasy", "stiff", "socially uncomfortable", "out of place", "uncoordinated", "ungraceful"],
        "teen_to_parent": ["awkward", "uneasy", "uncomfortable", "out of place", "socially uncomfortable", "stiff", "uncoordinated"]
    },
    "annoying": {
        "parent_to_teen": ["frustrating", "a little overwhelming", "distracting", "irritating", "exasperating", "tedious", "a bit of a hassle", "nagging"],
        "teen_to_parent": ["frustrating", "irritating", "exasperating", "a bit much", "overwhelming", "nagging", "distracting"]
    },
    "silly": {
        "parent_to_teen": ["playful", "light-hearted", "fun", "goofy", "whimsical", "amusing", "jovial", "carefree"],
        "teen_to_parent": ["playful", "fun", "light-hearted", "goofy", "amusing", "whimsical", "carefree"]
    },
    "stubborn": {
        "parent_to_teen": ["persistent", "determined", "strong-willed", "resolute", "unyielding", "tenacious", "inflexible", "set in your ways"],
        "teen_to_parent": ["persistent", "strong-willed", "resolute", "tenacious", "unyielding", "determined", "set in your ways"]
    },
    "cheating": {
        "parent_to_teen": ["dishonest", "breaking the rules", "unethical", "sneaky", "unfair", "untrustworthy", "misleading", "deceptive"],
        "teen_to_parent": ["dishonest", "sneaky", "unethical", "unfair", "deceptive", "untrustworthy", "misleading"]
    },
    "whiny": {
        "parent_to_teen": ["complaining", "a little needy", "petulant", "crying out for attention", "acting like a child", "moaning", "nagging", "fussing"],
        "teen_to_parent": ["complaining", "a bit needy", "fussing", "crying out for attention", "nagging", "whining", "petulant"]
    },
    "mean": {
        "parent_to_teen": ["harsh", "unkind", "cruel", "callous", "rude", "hurtful", "cold", "unfriendly"],
        "teen_to_parent": ["harsh", "unkind", "rude", "disrespectful", "hurtful", "cold", "callous"]
    },
    "broke": {
        "parent_to_teen": ["financially strained", "without much cash", "tight on money", "struggling with finances", "low on funds", "cash-strapped", "in need of some cash"],
        "teen_to_parent": ["broke", "tight on cash", "struggling", "low on funds", "financially strapped", "in need of money"]
    },
    "ungrateful": {
        "parent_to_teen": ["not appreciative", "thankless", "unthankful", "not showing gratitude", "taking things for granted", "not thankful", "unappreciative"],
        "teen_to_parent": ["not appreciative", "ungrateful", "not thankful", "thankless", "unappreciative", "taking things for granted"]
    },
    "overweight": {
        "parent_to_teen": ["larger", "bigger", "carrying some extra weight", "on the heavier side", "not at your healthiest", "fuller", "not as fit"],
        "teen_to_parent": ["larger", "heavier", "not at your healthiest", "fuller", "a bit overweight", "not as fit"]
    },
    "underweight": {
        "parent_to_teen": ["slender", "lean", "a little thin", "not at an ideal weight", "a bit too light", "lacking some weight"],
        "teen_to_parent": ["slender", "thin", "lean", "too light", "underweight"]
    },
}

# Function to paraphrase text based on dictionary
def paraphrase_text(text, direction):
    words = text.split()
    paraphrased_words = []
    
    for word in words:
        # Check if the word exists in the paraphrasing dictionary
        word_lower = word.lower()
        if word_lower in paraphrasing_dict:
            # Select the appropriate direction (parent_to_teen or teen_to_parent)
            if direction in paraphrasing_dict[word_lower]:
                paraphrased_words.append(random.choice(paraphrasing_dict[word_lower][direction]))
            else:
                paraphrased_words.append(word)  # If no direction, keep original word
        else:
            paraphrased_words.append(word)  # If word is not in dictionary, keep original word
    
    # Join the words back into a single string
    return ' '.join(paraphrased_words)

# Root route to display the HTML interface
@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Paraphrasing Tool</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <h1>Paraphrasing Tool</h1>
            <form action="/paraphrase" method="POST">
                <textarea name="text" placeholder="Enter your text here" rows="4" cols="50"></textarea><br><br>
                <label for="direction">Select Communication Direction:</label>
                <select name="direction" id="direction">
                    <option value="parent_to_teen">Parent to Teen</option>
                    <option value="teen_to_parent">Teen to Parent</option>
                </select><br><br>
                <input type="submit" value="Paraphrase">
            </form>
        </body>
        </html>
    ''')

# Route to handle the paraphrasing request
@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    text = request.form['text']
    direction = request.form['direction']
    paraphrased_text = paraphrase_text(text, direction)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Paraphrasing Tool - Result</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <h1>Paraphrased Text</h1>
            <p><strong>Original Text:</strong></p>
            <p>{{ original_text }}</p>
            <p><strong>Paraphrased Text:</strong></p>
            <p>{{ paraphrased_text }}</p>
            <br>
            <a href="/">Go Back</a>
        </body>
        </html>
    ''', original_text=text, paraphrased_text=paraphrased_text)

if __name__ == '__main__':
    app.run(debug=True)