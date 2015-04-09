/**
 * Loads an email in a popup box
 */
function load_email(url,to_addr){
    var target = $('#search_modal .modal-body');

    target.html('');
    var x = $('<iframe src="'+url+'" frameborder="0" onload="javascript:resizeIframe(this);" allowtransparency="true" scrolling="no"></iframe>');
    target.append(x);

    target.append('<hr/>');

    reply_form = $('<form action="'+url+'"></form>');

    email_address = $('<input name="to" type="text"/>').val(to_addr).appendTo(reply_form).addClass('form-control');
    reply_form.append('<textarea name="body" placeholder="Write a reply" class="form-control"></textarea>');
    reply_form.append('<input type="submit"/>')
    target.append(reply_form);



    $('#search_modal').modal();

    reply_form.submit(function(e){
        e.preventDefault();
        console.log($(this).serialize());
        var serialized_data = $(this).serialize();
        $(this).html('sending..');
        $.ajax({
            url:url,
            data:serialized_data,
        }).done(function(data){
            $('#search_modal').modal('hide');
        });
    });
}

function resizeIframe(obj) {
    obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
    obj.style.width = '100%';
}

$(function(e){

    if($('#search_modal').length == 0){
        console.log('added add');
        $('body').prepend(modal);
    }

    $('.email_link').click(function(e){
        e.preventDefault();
        var email_id = $(this).closest('tr').attr('data-emailid');
        var url = '/emails/m'+email_id+'/full';
        var to_addr = $(this).closest('tr').find('.to').html();
        to_addr = $('<div/>').html(to_addr).text();
        load_email(url,to_addr);
    });

});
