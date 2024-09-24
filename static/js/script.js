
 document.getElementById('add-option').addEventListener('click', function () {
    const optionsContainer = document.getElementById('poll-options');
    const newOption = document.createElement('input');
    newOption.type = 'text';
    newOption.className = 'form-control mb-3';
    newOption.name = 'option_' + (optionsContainer.children.length + 1);
    newOption.placeholder = 'Option ' + (optionsContainer.children.length + 1);
    newOption.autocomplete = 'off';
    optionsContainer.appendChild(newOption);
  });


function copyLink(url) {
    navigator.clipboard.writeText(url).then(() => {
        alert('Link copied to clipboard: ' + url);
    }).catch(err => {
        console.error('Error copying text: ', err);
    });
}