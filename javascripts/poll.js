/**
 * Created by thomas on 2014/06/10.
 */
function updateProgress(){
    $.getJSON('/poll',function(data){
        if (data == $("#progress").attr('max')) {
            $('#progress').remove();
            $('body').append('<h5>Process finished</h5>');
        } else {
            $("#progress").attr('value', data);
            setTimeout(updateProgress,5000);
        }
    })
}
//Execute the function
updateProgress();