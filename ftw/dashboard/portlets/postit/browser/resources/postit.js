
jq(function() {

    // REFRESH ODD / EVEN
    var refreshOddEven = function(jqElm){
        var odd = false;
        jqElm.find('.portletItem').each(function(i) {
            if(odd) {
                jq(this).removeClass('even');
                jq(this).addClass('odd');
                odd = false;
            } else {
                jq(this).removeClass('odd');
                jq(this).addClass('even');
                odd = true;
            }
        });
    }

    // CREATE NOTE
    jq('form.postIt_addNote_form').submit(function() {
        var text = jq(this).find('input[name=note]')[0].value;
        var hash = jq(this).parents('.portletPostIt:first').parents('div:first')[0].id.substr('portletwrapper-'.length);
        // notify server
        jq.ajax({
            type :      'POST',
            url :       './@@ftw.postit-addnote',
            data :      {
                    hash : hash,
                    note : text
            }
        });
        // add note to portlet
        var html = '<dd class="even portletItem postIt_note clearfix">';
        html += '<span>' + text + '</span>';
        html += '<a class="close postIt_remove" title="entfernen">';
        html += '<img src="./++resource++ftw.dashboard.portlets.postit.resources/icon_remove_box.gif" alt="entfernen"/>';
        html += '</a></dd>';
        jq(this).parents('dd.postIt_addNote').before(jq(html));
        // clean input field
        jq(this).find('input[name=note]')[0].value = '';
        // prevent browser from sending form...
        refreshOddEven(jq(this).parents('.portletPostIt:first').parents('div:first'));
        return false;
    });


    // DELEETE NOTE
    jq('.postIt_remove').live('click', function() {
        var notes = jq(this).parents('.portletPostIt:first').find('.portletItem');
        var index = notes.index(jq(this).parents('.portletItem:first'));
        var hash = jq(this).parents('.portletPostIt:first').parents('div:first')[0].id.substr('portletwrapper-'.length);
        jq.ajax({
            type :          'POST',
            url :           './@@ftw.postit-removenote',
            data :          {
                    hash : hash,
                    index : index
            }
        });
        var wrapper = jq(this).parents('.portletPostIt:first').parents('div:first');
        jq(this).parents('.portletItem:first').hide().remove();
        refreshOddEven(wrapper);
    });

});
