$(document).ready( function(){
	// $("*").css("font-size","28px","!important"); стереть если все таки надо увеличить 
	$("*").css("color", "black","!important");
	$("*").css("background-color", "white ","!important");
	$("*").css("background", "white ","!important");
	$("img").css("-webkit-filter","grayscale(100%)","!important");
	$("img").css("filter","grayscale(100%)","!important");
	$("svg").css("-webkit-filter","grayscale(100%)","!important");
	$("svg").css("filter","grayscale(100%)","!important");
	$("*").css("filter","grayscale(100%)","!important");
});
// эта функция воспроизваодит тексе при помощи функции SpeechSynthesisUtterance(); у которой мы указываем язык, посылаем текст, а потом фоспроизваодим.
function speak(text) {
    const message = new SpeechSynthesisUtterance();
    message.lang = "en-EN";//"en-EN";
    message.text = text;
    window.speechSynthesis.speak(message)
}

$(document.body).on('click', function(){
	var text = '';
	if (window.getSelection) {
		text = window.getSelection().toString();
	} else if (document.selection && document.selection.type != 'Control') {
		text = document.selection.createRange().text;
	}
	speak(text);
});
