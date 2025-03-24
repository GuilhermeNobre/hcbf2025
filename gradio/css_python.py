def result_text():
    return """
    #warning {font-size: 24px !important; font-weight: bold !important;}
    .feedback textarea {font-size: 24px !important; font-weight: bold !important;}
    """

def title_text_animation():
    return """
    function createGradioAnimation() {
        var container = document.createElement('div');
        container.id = 'gradio-animation';
        container.style.fontSize = '4em';
        container.style.fontWeight = 'bold';
        container.style.textAlign = 'center';
        container.style.marginBottom = '20px';
        container.style.marginTop = '50px';

        var text = 'Hub Life 🧬';
        for (var i = 0; i < text.length; i++) {
            (function(i){
                setTimeout(function(){
                    var letter = document.createElement('span');
                    letter.style.opacity = '0';
                    letter.style.transition = 'opacity 0.5s';
                    letter.innerText = text[i];

                    container.appendChild(letter);

                    setTimeout(function() {
                        letter.style.opacity = '1';
                    }, 50);
                }, i * 250);
            })(i);
        }

        var gradioContainer = document.querySelector('.gradio-container');
        gradioContainer.insertBefore(container, gradioContainer.firstChild);

        return 'Animation created';
    }
    """