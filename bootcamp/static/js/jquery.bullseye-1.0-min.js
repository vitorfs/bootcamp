/*!
* jQuery Bullseye v1.0
* http://pixeltango.com
*
* Copyright 2010, Mickel Andersson
* Dual licensed under the MIT or GPL Version 2 licenses.
*
* Date: Fri Aug 31 19:09:11 2010 +0100
*/
jQuery.fn.bullseye = function (b, h) { b = jQuery.extend({ offsetTop: 0, offsetHeight: 0, extendDown: false }, b); return this.each(function () { var a = $(this), c = $(h == null ? window : h), g = function () { var d = a.outerWidth(), e = a.outerHeight() + b.offsetHeight; c.width(); var f = c.height(), i = c.scrollTop(), j = c.scrollLeft() + d; f = i + f; var k = a.offset().left; d = k + d; var l = a.offset().top + b.offsetTop; e = l + e; if (f < l || (b.extendDown ? false : i > e) || j < k || j > d) { if (a.data("is-focused")) { a.data("is-focused", false); a.trigger("leaveviewport") } } else if (!a.data("is-focused")) { a.data("is-focused", true); a.trigger("enterviewport") } }; c.scroll(g).resize(g); g() }) };