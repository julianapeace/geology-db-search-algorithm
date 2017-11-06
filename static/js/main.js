$(document).ready(function () {
//add jquery to toggle year = range || exact
// $('#pub_year_range').hide();
// $('#exact_pub_year').hide();
console.log('testinggg')
$('#pub_year_range').hide();
$('#exact_pub_year').hide();

var x = $( "input[type=radio][name=year]:checked" ).val();
console.log(x)
     $('input[type="radio"][name=year]').click(function() {
         if($(this).attr('id') == 'range') {
              $('#pub_year_range').slideToggle();
              $('#exact_pub_year').hide();
         }

         else {
           $('#pub_year_range').hide();
           $('#exact_pub_year').slideToggle();
         }
     });

});
