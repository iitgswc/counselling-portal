/**
 * Created by Rohan on 14-03-2017.
 */
$('#chat-form').on('submit', function(event){
    event.preventDefault();
    var user=document.getElementById('username');
    $.ajax({
        url : '/chat/post2/',
        type : 'POST',
        data : { msgbox : $('#chat-msg').val(),username :  $('#username').html() },

        success : function(json){
            $('#chat-msg').val('');
            $('#msg-list').append('<li class="collection-item" style="text-align: right">' + json.msg + '</li>');
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        }
    });
});

function getMessages(){
    if (!scrolling) {
        $.get('/chat/messages2/',{'id':$('#username').html().toString()}, function(messages){
            $('#msg-list').append(messages);
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function(){
    $('#msg-list-div').on('scroll', function(){
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 2000);
});

$(document).ready(function() {
     $('#send').attr('disabled','disabled');
     $('#chat-msg').keyup(function() {
        if($(this).val() != '') {
           $('#send').removeAttr('disabled');
        }
        else {
        $('#send').attr('disabled','disabled');
        }
     });
 });

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});