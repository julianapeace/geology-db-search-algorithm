$(document).ready(function () {
//add jquery to toggle year = range || exact
// $('#pub_year_range').hide();
// $('#exact_pub_year').hide();
console.log('testinggg')
$('#pub_year_range').hide();
$('#exact_pub_year').hide();

$('#basic-tooltip').hide();
$('#year-tooltip').hide();
$('#geography-tooltip').hide();
$('#output-tooltip').hide();
$('#sample-tooltip').hide();


$('#basic').click(function(event){
  $('#basic-tooltip').slideToggle()
  })
  $('#year').click(function(event){
    $('#year-tooltip').slideToggle()
    })
    $('#geography').click(function(event){
      $('#geography-tooltip').slideToggle()
      })
      $('#output').click(function(event){
        $('#output-tooltip').slideToggle()
      })
        $('#sample').click(function(event){
          $('#sample-tooltip').slideToggle()
          })
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

$('table').addClass('classname');
$('.ectable table').addClass('2classname');
$('.ectable').addClass('3classname');


});
