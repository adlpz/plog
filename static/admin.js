
updateForm = function(key) {
	$.getJSON('/blog/api/get', {'key': key}, function(data) {
		$("form #key").val(key);
		$("form #title").val(data["title"]);
		$("form #content").val(data["content"]);
		$("form #format").val(data["format"]);
		$("form").children().removeAttr("disabled").css("background", "#333");
		
	});
};

notify = function(text, callback){
	text = "<p>" + text + "</p><p><a href='#' id='yes'>Yes</a><a href='#' id='no'>No</a></p>";
	$("#notification").html(text).slideDown();
	$("#yes").click(function() {
		callback();
		$("#notification").slideUp();
	});
	$("#no").click(function(){
		$("#notification").slideUp();
	});
}


$(document).ready(function() {
	
	$("li a.post").click(function(){
		$("li").css("background", "none");
		$(this).parent().css("background", "#888");
		$("form").children().attr("disabled", "disabled").css("background", "#888");
		var hash = $(this).attr("href");
		updateForm(hash.substr(1, hash.length-1));
	});
	
	$("a.delete").click(function(){
		var hash = $(this).parent().children("a.post").attr("href");
		key = hash.substr(1, hash.length-1);
		notify("Are you sure you want to delete this post? This operation can't be undone.",
		function(){
			$.getJSON('/blog/api/pop', {'key': key}, function() {
				location.reload();
			});
		});
	});
	
	$("a#new_b").click(function(){
		notify("Are you sure you want to start a new post? All current changes will be lost.",
		function(){$("li").css("background", "none");$("form").children().val("")});
	});
	
});
