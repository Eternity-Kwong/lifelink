// Paraphrasing logic
function paraphraseText(inputText) {
    // Replace "mean" words with "nice" words
    const meanWords = {
        "hate": "dislike",
        "stupid": "silly",
        "ugly": "not my favorite",
        "dumb": "misunderstood",
        "annoying": "a bit much"
    };

    let outputText = inputText;

    // Replace each mean word with a nicer one
    for (let word in meanWords) {
        let regex = new RegExp("\\b" + word + "\\b", "gi");
        outputText = outputText.replace(regex, meanWords[word]);
    }

    return outputText;
}

// Show words that can be improved
function showImprovements(inputText) {
    const meanWords = ["hate", "stupid", "ugly", "dumb", "annoying"];
    let wordsToImprove = [];

    // Find words that need improvement
    let words = inputText.split(" ");
    words.forEach(word => {
        if (meanWords.includes(word.toLowerCase())) {
            wordsToImprove.push(word);
        }
    });

    return wordsToImprove;
}

// DOM elements
const homeScreen = document.getElementById("home-screen");
const chatScreen = document.getElementById("chat-screen");
const startChatButton = document.getElementById("start-chat");
const backToHomeButton = document.getElementById("back-to-home");
const paraphraseButton = document.getElementById("paraphrase-button");
const improvementButton = document.getElementById("improvement-button");
const inputTextArea = document.getElementById("input-text");
const paraphrasedText = document.getElementById("paraphrased-text");
const improvementList = document.getElementById("improvement-list");
const improvementOutput = document.getElementById("improvement-output");

// Switch to chat screen
startChatButton.addEventListener("click", () => {
    homeScreen.classList.add("hidden");
    chatScreen.classList.remove("hidden");
});

// Switch back to home screen
backToHomeButton.addEventListener("click", () => {
    chatScreen.classList.add("hidden");
    homeScreen.classList.remove("hidden");
});

// Paraphrase button functionality
paraphraseButton.addEventListener("click", () => {
    const inputText = inputTextArea.value;
    const paraphrased = paraphraseText(inputText);
    paraphrasedText.textContent = paraphrased;
});

// Show improvements button functionality
improvementButton.addEventListener("click", () => {
    const inputText = inputTextArea.value;
    const improvements = showImprovements(inputText);

    improvementList.innerHTML = ""; // Clear previous list

    if (improvements.length === 0) {
        improvementList.innerHTML = "<li>No words to improve!</li>";
    } else {
        improvements.forEach(word => {
            const listItem = document.createElement("li");
            listItem.textContent = `Consider changing "${word}" to something nicer!`;
            improvementList.appendChild(listItem);
        });
    }

    improvementOutput.classList.remove("hidden");
});