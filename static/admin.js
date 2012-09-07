// Global var (yeeah... I mean...)
var changed = false;


// Updates the form with the current editing post
updateForm = function(key) {
    unset_edited();
    $("form .button.delete").show();
	$.getJSON(document.base_url + '/api/get', {'key': key}, function(data) {
		$("form #key").val(key);
		$("form #title").val(data["title"]);
		$("form #secontent").val(data["content"]);
		$("form #format").val(data["format"]);
		
	});
};

// Notifier function
notify = function(text, callback){
	text = "<p>" + text + "</p>";
    if (callback != null) {
        text += "<p><a href='#' id='yes'>Yes</a><a href='#' id='no'>No</a></p>";
    } else {
        text += "<p><a href='#' id='no'>Dismiss</a></p>";
    }
	$("#notification").html(text).fadeIn();
	$("#yes").click(function() {
		callback();
		$("#notification").fadeOut();
	});
	$("#no").click(function(){
		$("#notification").fadeOut();
	});
}

// Clear forms for new post
newpost = function(){
    unset_edited();
    $("li").removeClass("selected");
    $("form .clearable").val("");
    $("section#editor button.discard").hide();
    $("section#editor button.delete").hide();
}

// Set/Unset edited status
set_edited = function() { 
    changed = true;
    $("form .button.discard").show();
}
unset_edited = function() {
    changed = false;
    $("form .button.discard").hide();
    $("form .button.delete").hide();
}

$(document).ready(function() {

    // Refresh
    unset_edited();
	
    // Set handler for click in post titles
	$("section#list li.post").click(function(){
		var hash = $(this).children("a.post").attr("href");
        var key = hash.substr(1, hash.length-1);
        if (changed == false) {
            $("section#list li").removeClass("selected");
		    $(this).addClass("selected");
		    updateForm(key);
        } else {
            notify("You have unsaved changes in this post. Are you sure you want to discard them?", 
                function() {
                    $("section#list li").removeClass("selected");
		            $(this).addClass("selected");
		            updateForm(key);
                });
        }
	});
	
	// Set handler for the new post button
	$("section#list li.new_post").click(function(){
        if (changed == true) {
            notify("Are you sure you want to start a new post? All current changes will be lost.", newpost);
        } else {
            newpost();
        }
	});

    // Set handler for submit button
    $("form .button.save").click(function() {
        $(this).parent().submit();
    });

    // Set handler for delete button
    $("form .button.delete").click(function() {
        var key = $(this).parent().children("input#key").attr("value");
        if (key == "") {
            // This should never happen!
            notify("You haven't selected any post. This shoudln't be possible!", null);
            return 0;
        }
        notify("Are you sure you want to delete this post? This operation cannot be undone.",
            function(){
                $.getJSON(document.base_url + '/api/pop', {'key':key}, function() {
                    location.reload();
                });
            });
    });

    // Set handler for discard button
    $("form .button.discard").click(function() {
        if (changed == true) {
            notify("Are you sure you want to discard the changes? All current changes will be lost.", newpost);
        } else {
            newpost();
        }
    });

    // Set handler for edited content
    $("form textarea, form input, form select").keyup(function() {
        set_edited();
    });

});
