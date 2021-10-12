let hidden = document.querySelector('#hidden');
let Voices = document.querySelector('#Voices');
let Start_button = document.querySelector('#Start_button');
let speech_types = window.speechSynthesis;
let voices_list = [];

Users_choice_of_speech();

if(speechSynthesis !== undefined){
    speechSynthesis.onvoiceschanged = Users_choice_of_speech;
}

Start_button.addEventListener('click', function() {
    let Pronouncing = new SpeechSynthesisUtterance(hidden.value);
    let Name_of_chosen_item = Voices.selectedOptions[0].getAttribute('data-name');
    voices_list.forEach((voice)=>{
        if(voice.name === Name_of_chosen_item){
            Pronouncing.voice = voice;
        }
    });
    speech_types.speak(Pronouncing);
});

function Users_choice_of_speech(){
    voices_list = speech_types.getVoices();
    voices_list.forEach((voice)=>{
        let Selection = document.createElement('option');
        Selection.textContent = voice.name;
        Selection.setAttribute('data-lang', voice.lang);
        Selection.setAttribute('data-name', voice.name);
        Voices.appendChild(Selection);
    });

    Voices.selectedIndex = 0;
}