
  function addReview_display(){
    el = document.querySelector('.review_section');
    
    if(el.style.visibility == 'hidden'){
        el.style.visibility = 'visible'
    }else{
       el.style.visibility = 'hidden'
    }
  }


  //Slider for index page -code from Lindsey Jacks at https://codepen.io/linzjax/details/ZrqNqW
  var sheet = document.createElement('style'),  
  $rangeInput = $('.range input'),
  prefs = ['webkit-slider-runnable-track', 'moz-range-track', 'ms-track'];

document.body.appendChild(sheet);

var getTrackStyle = function (el) {  
  var curVal = el.value,
      val = (curVal - 1) *16.666666667,
      style = '';
  
  // Set active label
  $('.range-labels li').removeClass('active selected');
  
  var curLabel = $('.range-labels').find('li:nth-child(' + curVal + ')');
  
  curLabel.addClass('active selected');
  curLabel.prevAll().addClass('selected');

  return style;
}

$rangeInput.on('input', function () {
  sheet.textContent = getTrackStyle(this);
});

// Change input value on label click
$('.range-labels li').on('click', function () {
  var index = $(this).index();
  
  $rangeInput.val(index + 1).trigger('input');
  
});

//checkbox logic from https://stackoverflow.com/questions/21523730/html-checkbox-submit-button-by-agreeing-on-terms-and-condition
function disableSubmit() {
  document.getElementById("submit").disabled = false;
 }

  function activateButton(element) {

      if(element.checked) {
        document.getElementById("submit").disabled = false;
       }
       else  {
        document.getElementById("submit").disabled = true;
      }

  }
