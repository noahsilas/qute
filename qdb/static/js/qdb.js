QDB = (function($){
    function init(){
        setup_votes()
        csrf_protect()
    }

    function csrf_protect(){
        $(document).ajaxSend(function(event, xhr, settings) {
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
            function sameOrigin(url) {
                // url could be relative or scheme relative or absolute
                var host = document.location.host; // host + port
                var protocol = document.location.protocol;
                var sr_origin = '//' + host;
                var origin = protocol + sr_origin;
                // Allow absolute or scheme relative URLs to same origin
                return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                    // or any other URL that isn't scheme relative or absolute i.e relative.
                    !(/^(\/\/|http:|https:).*/.test(url));
            }
            function safeMethod(method) {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        });
    }

    function setup_votes(){
        function add_handler(selector, delta){
            $('ul').on('click', selector, function(evt){
                evt.preventDefault();
                var target = $(evt.target);
                var quote_id = target.data('quote');

                $.post(
                    '/qdb/vote',
                    { quote: quote_id,
                      score: delta
                    },
                    function(score){
                        adjust_vote(target, score);
                    }
                );
            });
        }
        add_handler('.upvote', 1)
        add_handler('.downvote', -1)
        add_handler('.novote', 0)
    }

    function adjust_vote(target, score){
        container = target.parent().find('span');
        container.html(score);
        container.animate({backgroundColor: '#eaff00'}
                ).delay(500
                ).animate({backgroundColor: '#ffffff'});
    }

    return {
        init: init,
        setup_votes: setup_votes
    }
})(jQuery);
QDB.init()
