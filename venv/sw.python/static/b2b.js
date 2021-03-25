//Inspired by Add Review code from index.js

function addDiscount_display(){
    el = document.querySelector('.content_section');
    
    if(el.style.visibility == 'hidden'){
        el.style.visibility = 'visible'
    }else{
       el.style.visibility = 'hidden'
    }
  }

  $('showreviews').click(function() { 
 
    el = document.querySelector('.divreviews');
    if(el.style.visibility == 'hidden'){
        el.style.visibility = 'visible'
    }else{
       el.style.visibility = 'hidden'
    }
  } ) 

