$(window).scroll(function() {
  
    // selectors
    var $window = $(window),
        $body = $('body'),
        $panel = $('.panel');
    
    // Change 33% earlier than scroll position so colour is there when you arrive.
    var scroll = $window.scrollTop() + ($window.height() / 3);
   
    $panel.each(function () {
      var $this = $(this);
      
      // if position is within range of this panel.
      // So position of (position of top of div <= scroll position) && (position of bottom of div > scroll position).
      // Remember we set the scroll to 33% earlier in scroll var.
      if ($this.position().top <= scroll && $this.position().top + $this.height() > scroll) {
            
        // Remove all classes on body with color-
        $body.removeClass(function (index, css) {
          return (css.match (/(^|\s)color-\S+/g) || []).join(' ');
        });
         
        // Add class of currently active div
        $body.addClass('color-' + $(this).data('color'));
      }
    });    
    
  }).scroll();

  //Read input in textbox, find the length of the string, the word count, the character count without the spaces and the amount of lines in the text, return the lengths and change the HTML 

$("textarea").keyup(function(){
  
    //Gets the value from the text-area
    var text = $('#text').val();
    
    //Trims trailing white space
    var textTrim = text.trim();
    
    //Set everything to zero if nothing is entered
    if (textTrim.length === 0) {
      $('.details').html('<p>Words: 0 <br>Characters with spaces: 0 <br>Characters without spaces: 0 <br>Lines: 0')
    } else {
    
      //finds a white space character and replaces it with a single space then splits it to create an array of words
    var words = textTrim.replace(/\s+/gi, ' ').split(' ');
    
      //returns the length of the total string
    var charWith = textTrim.length;
    
      //removes all spaces and returns the length of the string
      var charWithout = textTrim.replace(/\s+/gi, '').length;
      
      //looks for the return character and finds the new line character to calculate how many lines there are 
      var lines = textTrim.split(/\r*\n/).length;
      
      //sets the value of the details class div
    $('.details').html('<p>Words: ' + words.length + '<br>Characters with spaces: ' + charWith + '<br>Characters without spaces: ' + charWithout + '<br>Lines: ' + lines);
    }
  });