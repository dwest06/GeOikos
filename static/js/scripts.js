$(document).ready(function() {
	var nav = function() {
		if ($('nav').hasClass('open')) {
			$('nav').slideUp('fast').removeClass('open');
		} else {
			$('nav').slideDown('fast').addClass('open');
		}
	}
	$('.menu-trigger').click(function(){
		nav();
		console.log('ha');
	});

	var mq = window.matchMedia( "(min-width: 700px)" );
	$(window).resize(function() {
		if (mq.matches) {
			if (!($('nav').hasClass('open'))) {
				$('nav').css('display','');
			} else {
				$('nav').removeClass('open');
			};
		};
	});
});	