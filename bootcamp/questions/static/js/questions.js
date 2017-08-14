$(function () {
  $(".question .panel-body").click(function () {
    var question_id = $(this).closest(".question").attr("question-id");
    location.href = "/questions/" + question_id;
  });

  $(".accept").click(function () {
    var span = $(this);
    var question = $(".question").attr("question-id");
    var answer = $(this).closest(".answer").attr("answer-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".answer")).val();
    $.ajax({
      url: '/questions/answer/accept/',
      data: {
        'question': question,
        'answer': answer,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $(".accept").removeClass("accepted");
        $(".accept").prop("title", "Click to accept the answer");
        $(span).addClass("accepted");
        $(span).prop("title", "Click to unaccept the answer");
      }
    });
  });

  $(".answer-vote").click(function () {
    var span = $(this);
    var answer = $(this).closest(".answer").attr("answer-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".answer")).val();
    var vote = "";
    if ($(this).hasClass("voted")) {
      var vote = "R";
    }
    else if ($(this).hasClass("up-vote")) {
      vote = "U";
    }
    else if ($(this).hasClass("down-vote")) {
      vote = "D";
    }
    $.ajax({
      url: '/questions/answer/vote/',
      data: {
        'answer': answer,
        'vote': vote,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        var options = $(span).closest('.options');
        $('.vote', options).removeClass('voted');
        if (vote == 'U' || vote == 'D') {
          $(span).addClass('voted');
        }
        $('.votes', options).text(data);
      }
    });
  });

   $(".question-vote").click(function () {
    var span = $(this);
    var question = $(this).closest(".question").attr("question-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".question")).val();
    console.log(csrf)
    var vote = "";
    if ($(this).hasClass("voted")) {
      var vote = "R";
    }
    else if ($(this).hasClass("up-vote")) {
      vote = "U";
    }
    else if ($(this).hasClass("down-vote")) {
      vote = "D";
    }
    $.ajax({
      url: '/questions/question/vote/',
      data: {
        'question': question,
        'vote': vote,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        var options = $(span).closest('.options');
        $('.vote', options).removeClass('voted');
        if (vote == 'U' || vote == 'D') {
          $(span).addClass('voted');
        }
        $('.votes', options).text(data);
      }
    });
  });

  $(".favorite").click(function () {
    var span = $(this);
    var question = $(this).closest(".question").attr("question-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".question")).val();

    $.ajax({
      url: '/questions/favorite/',
      data: {
        'question': question,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        if ($(span).hasClass("favorited")) {
          $(span).removeClass("glyphicon-star")
            .removeClass("favorited")
            .addClass("glyphicon-star-empty");
        }
        else {
          $(span).removeClass("glyphicon-star-empty")
            .addClass("glyphicon-star")
            .addClass("favorited");
        }
        $(".favorite-count").text(data);
      }
    });

  });
});