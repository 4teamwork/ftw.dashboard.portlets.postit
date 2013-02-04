jQuery(function($) {

    // REFRESH ODD / EVEN
    var refreshOddEven = function(jqElm){
        var odd = false;
        jqElm.find('.portletItem').each(function(i) {
            if(odd) {
                $(this).removeClass('even');
                $(this).addClass('odd');
                odd = false;
            } else {
                $(this).removeClass('odd');
                $(this).addClass('even');
                odd = true;
            }
        });
    };

    // CREATE NOTE
    $('form.postIt_addNote_form').submit(function() {
        var text = $(this).find('input[name=note]')[0].value;
        var hash = $(this).parents('.portletPostIt:first').parents('div:first')[0].id.substr('portletwrapper-'.length);
        // notify server
        $.ajax({
            type :      'POST',
            url :       './@@ftw.postit-addnote',
            data :      {
                    hash : hash,
                    note : text
            }
        });

        //escape the text
        text = text.replace(/</g, '&lt;');
        text = text.replace(/>/g, '&gt;');
        text = text.replace(/"/g, '&quot;');

        // add note to portlet
        var html = '<dd class="even portletItem postIt_note clearfix">';
        html += '<span>' + text + '</span>';
        html += '<a class="close postIt_remove" title="entfernen">';
        html += '<img src="./++resource++ftw.dashboard.portlets.postit.resources/icon_remove_box.gif" alt="entfernen"/>';
        html += '</a></dd>';
        $(this).parents('dd.postIt_addNote').before($(html));
        // clean input field
        $(this).find('input[name=note]')[0].value = '';
        // prevent browser from sending form...
        refreshOddEven($(this).parents('.portletPostIt:first').parents('div:first'));
        return false;
    });


    // DELEETE NOTE
    $('.postIt_remove').live('click', function(){
        var notes = $(this).parents('.portletPostIt:first').find('.portletItem');
        var index = notes.index($(this).parents('.portletItem:first'));
        var hash = $(this).parents('.portletPostIt:first').parents('div:first')[0].id.substr('portletwrapper-'.length);
        $.ajax({
            type :          'POST',
            url :           './@@ftw.postit-removenote',
            data :          {
                    hash : hash,
                    index : index
            }
        });
        var wrapper = $(this).parents('.portletPostIt:first').parents('div:first');
        $(this).parents('.portletItem:first').hide().remove();
        refreshOddEven(wrapper);
    });

});
