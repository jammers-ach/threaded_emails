function get_url(id){
    return '/emails/m' + id + '/full'; //TODO secuirty check here
}

$(function(){
    $(".email_table tr").click(function(e){
        var msg_id = $(this).attr('data-id');
        console.log(msg_id);

        var has_email = $(this).hasClass('with-email');
        if(!has_email && msg_id){
            $(this).addClass('with-email');

            var email_field = $('<tr class="full"></tr>');
            var col = $('<td colspan="3"></td>');
            email_field.append(col);
            $(this).find('.msg_short').hide();

            $(this).after(email_field);
            col.html('<iframe src="'+get_url(msg_id)+'" frameborder="0" allowtransparency="true" scrolling="no"></iframe>');
        }
        else if(has_email && msg_id){
            $(this).find('.msg_short').show();
        }
    });

});
