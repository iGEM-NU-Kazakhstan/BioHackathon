"use strict"; // Without [strict] mode many errors will prevent the code from working
// For the developers who want to use this library: don't forget to add <select id = "selectionOfVoices"></select> in your html code. 
// This part of this JS Library reades the selected text for people with poor sight
// AllVoicesAvailable function creates a selector with Google's all available voices from which user can pick what they want
let selectionOfVoices = document.getElementById("selectionOfVoices");
let allVoices = [];

var allVoicesAvailable = function() {
    allVoices = speechSynthesis.getVoices();

    for (let t = 0; t < allVoices.length; t++) {
        var dropdownOptions = document.createElement('option');
        dropdownOptions.textContent = allVoices[t].name + ' {' + allVoices[t].lang + '}';
        dropdownOptions.textContent += allVoices[t].default ? ' >> default <<' : '';
        dropdownOptions.setAttribute('lang', allVoices[t].lang);
        dropdownOptions.setAttribute('name', allVoices[t].name);
        document.getElementById("selectionOfVoices").appendChild(dropdownOptions);
    }
}

// Trigger function detects the change in language selection and says the text in a new selected language  
var trigger = function() {
    let sayIt = new SpeechSynthesisUtterance(text);
    let selectedOption = selectionOfVoices.selectedOptions[0].getAttribute('name');

    for (let i = 0; i < allVoices.length; i++) {
        if (allVoices[i].name === selectedOption)
            sayIt.voice = allVoices[i];
    }
    speechSynthesis.speak(sayIt);
};

let text = 'Welcome to Text to Speech by GHS';
// selectedTextReceiver function receives the selected text from the user 
var selectedTextReceiver = function() {
    let text = "";
    if (window.getSelection)
        text = window.getSelection().toString();
    else if (document.selection && document.selection.type != "Control")
        text = document.selection.createRange().text;

    return text;
}

// Onmouse event of js helps to detect the change of the cursor and helps to pronounce the new selected words by calling needed functions such as selectedTextReceiver and trigger.   
document.onmouseup = function() {
    setTimeout(function() {
        speechSynthesis.cancel();
        text = selectedTextReceiver();
        trigger();
    });
};

// Running all functions created above
allVoicesAvailable();
if (typeof speechSynthesis.onvoiceschanged !== undefined)
    speechSynthesis.onvoiceschanged = allVoicesAvailable;

selectionOfVoices.onchange = trigger;
setTimeout(trigger, 50);

/*  
    This part of JS library decreases the beightness for people with achromatopsia
    Don't forget to add: 
    <button onclick="myFunction()">Make it readable!</button>
    <button onclick="cancelTheChange()">Make it normal!</button>
    to you HTML file !!!

    There's another way to decrease the brightness of an image without using buttons, which is also shorter.
    Just add these lines to you CSS file:

    img:hover {
    filter: brightness(50%);
    
*/

function myFunction() { // decreases the brightness of all images
    var images = document.getElementsByTagName("img");
    for (var i = 0; i < images.length; i++) {
        images[i].style.filter = "brightness(50%)";
    }
}

function cancelTheChange() { // makes brightness normal for all images
    var images = document.getElementsByTagName("img");
    for (var i = 0; i < images.length; i++) {
        images[i].style.filter = "brightness(100%)";
    }
}

/*  
    This part of JS library increases font size for people with poor eyesight to make it easily readable
    Don't forget to add: 
    <button onclick="makeBigger()">Make it bigger!</button>
    <button onclick="makeSmaller()">Make it smaller!</button>
    to you HTML file !!!

    To apply these changes not only for <p> tag, add your own text tags to change them too. 
    
*/

function makeBigger() {
    var texts = document.getElementsByTagName("p")

    for (var i = 0; i < texts.length; i++) {
        texts[i].style.fontSize = "200%";
    }
}

function makeSmaller() {
    var texts = document.getElementsByTagName("p")

    for (var i = 0; i < texts.length; i++) {
        texts[i].style.fontSize = "100%";
    }
}

// Made by GenomeHackSquad in the scope of Code-on event by iGem