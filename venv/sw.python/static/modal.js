
const ToggleModal = () => {
    document.querySelector('.modal')
     .classList.toggle('modal--hidden');
};

document.querySelector('#show-modal')
.addEventListener('click', ToggleModal) ;

function CopyFunction() {
    /* Get the text field */
    var copyText = document.getElementById("myInput");
  
    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /* For mobile devices */
  
    /* Copy the text inside the text field */
    document.execCommand("copy");
  
    /* Alert the copied text */
    alert(`Discount Code Copied: ${copyText.value}`);
  }

  document.querySelector('.modal_close-bar span')
    .addEventListener('click', ToggleModal)