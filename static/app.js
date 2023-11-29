class Chatbox {

    

    
    constructor() {
        this.args = {          
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            chatBotButton: document.querySelector('.chat__bot'),
            quizBotButton: document.querySelector('.quiz_bot'),
            randomQuizButton: document.querySelector('.randon__quiz'),
            topicQuizButton: document.querySelector('.topic__list')

        }

        this.state = false;
        this.messages = [];
        this.evaluate = false;
        this.isChatBot = false;

        this.currentQuestionIndex = 0;
        this.score = 0;

        // List of questions for the quiz
        this.quizQuestions = [];
        this.quizAnswers = [];
        this.topics = ["Public Key Cryptography","SYMMETRIC BLOCK ENCRYPTION","RANDOM NUMBERS","Stream Cipher", "Message Authentication","MAC"]

    }

    
    display() {
        const {openButton, chatBox, sendButton, quizBotButton, randomQuizButton, topicQuizButton, chatBotButton} = this.args;
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))
        randomQuizButton.addEventListener('click',() => this.randomQuiz(chatBox))
        topicQuizButton.addEventListener('change',() => this.topicQuiz(chatBox))
        chatBotButton.addEventListener('click', () => this.chatBot(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
        

        // this.displayQuizQuestion(chatBox);
    }
    displayQuizQuestion(chatbox) {
        console.log("In display")
        const quizQuestion = this.quizQuestions[this.currentQuestionIndex];
        const quizMessage = { name: "Bot", message: `Quiz: ${quizQuestion}` };
        this.messages.push(quizMessage);
        this.updateChatText(chatbox);
    }

    onSendButton(chatbox) {
        if(this.evaluate === true){
            console.log("answer check");
            var textField = chatbox.querySelector('input');
            let userAnswer = textField.value;
            if (userAnswer === "") {
                return;
            }
    
            let userMessage = { name: "User", message: userAnswer };
            this.messages.push(userMessage);
            
            console.log(userAnswer)
            console.log(this.quizAnswers[this.currentQuestionIndex])
            // Check the user's answer if needed
            if(userAnswer === this.quizAnswers[this.currentQuestionIndex]){
                this.score++
            }
               
            // Move to the next quiz question
            this.currentQuestionIndex++
    
            if (this.currentQuestionIndex < this.quizQuestions.length) {
                // Display the next quiz question
                this.displayQuizQuestion(chatbox);
            } else {


                let scoreMessage = { name: "Bot", message: "Quiz completed. Your score is "+this.score+" out of "+this.quizQuestions.length };
                this.messages.push(scoreMessage);
                this.updateChatText(chatbox);
                // Display a message when all quiz questions are answered
                let finalMessage = { name: "Bot", message: "Thanks for participating!" };
                this.messages.push(finalMessage);
                this.updateChatText(chatbox);
                this.evaluate = false;
            }
    
            // Clear the user input
            textField.value = '';
        }
        else{
            console.log("Api call");
            var textField = chatbox.querySelector('input')
            let text1 = textField.value
            textField.value = '';
            if (text1 === "") {
                return;
            }

            if(this.isChatBot === true){
                this.generateChatApi(chatbox,text1)
            }
            else{
                this.generateQuizApi(chatbox,text1)
            }
        }
    }


    chatBot(chatBox){
        this.isChatBot = true;
        displayFooter();
    }
    randomQuiz(chatbox){
        var num =  Math.floor(Math.random() * 11);
        console.log(num);
        displayFooter();
        let intial_input = "Generate a quiz on "+this.topics[num];
        console.log(intial_input)
        this.generateQuizApi(chatbox,intial_input)
     }

    topicQuiz(chatbox){
        displayFooter();

        var dropdown = document.getElementById("myDropdown");

        const selectedOption = dropdown.options[dropdown.selectedIndex];

        // Get the text of the selected option
        const selectedOptionText = selectedOption.text;
        console.log(selectedOptionText)
        let intial_input = "Generate a quiz on "+selectedOptionText;
        console.log(intial_input)
        this.generateQuizApi(chatbox,intial_input)
        
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Bot")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

    generateQuizApi(chatbox, text1){

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1)
        this.updateChatText(chatbox)
        const timeoutInMilliseconds = 300000;
        fetch($SCRIPT_ROOT + '/generateQuiz', {
            method: 'POST',
            body: JSON.stringify({ question: text1 }),
            mode: 'cors',
            timeout: timeoutInMilliseconds,
            headers: {
            'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            this.quizAnswers = r.answers
            this.quizQuestions = r.questions
            this.evaluate = true
            this.displayQuizQuestion(chatbox)
            // let msg2 = { name: "Bot", message: r.answer + " --- " + r.citation };
            // this.messages.push(msg2);
            // this.updateChatText(chatbox)
            textField.value = ''
            

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
        });
    }

    generateChatApi(chatbox, text1){

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1)
        this.updateChatText(chatbox)
        const timeoutInMilliseconds = 300000;
        fetch($SCRIPT_ROOT + '/generateChat', {
            method: 'POST',
            body: JSON.stringify({ question: text1 }),
            mode: 'cors',
            timeout: timeoutInMilliseconds,
            headers: {
            'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(r => {
            let msg2 = { name: "Bot", message: r.answer + " ---Slide : " + r.citation+ " , Page : "+r.pageNo };
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
        });
    }
}



const chatbox = new Chatbox();
chatbox.display();
