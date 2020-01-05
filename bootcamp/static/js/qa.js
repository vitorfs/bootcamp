$(function () {
  function getCookie(name) {
    // Function to get any cookie available in the session.
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  function toogleVote(voteIcon, vote, data, isAnswer) {
    var idPrefix = isAnswer ? 'answer' : 'question';
    var isOwner = data.is_owner;
    if (isOwner === false) {
      if (vote === "U") {
        voteIcon.addClass('voted');
        voteIcon.siblings(`#${idPrefix}DownVote`).removeClass('voted');
      } else {
        voteIcon.addClass('voted');
        voteIcon.siblings(`#${idPrefix}UpVote`).removeClass('voted');
      }
      voteIcon.siblings(`#${idPrefix}Votes`).text(data.votes);
    }
  }

  var csrftoken = getCookie('csrftoken');
  var page_title = $(document).attr("title");
  // This sets up every ajax call with proper headers.
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  $("#publish").click(function () {
    // function to operate the Publish button in the question form, marking
    // the question status as published.
    $("input[name='status']").val("O");
    $("#question-form").submit();
  });

  $("#draft").click(function () {
    // Function to operate the Draft button in the question form, marking
    // the question status as draft.
    $("input[name='status']").val("D");
    $("#question-form").submit();
  });

  $(".question-vote").click(function () {
    // Vote on a question.
    var voteIcon = $(this);
    var question = $(this).closest(".question").attr("question-id");
    if ($(this).hasClass("up-vote")) {
      vote = "U";
    } else {
      $('#questionDownVote').addClass('voted');
      $('#questionUpVote').removeClass('voted');
    }
    $.ajax({
      url: '/qa/question/vote/',
      data: {
        'question': question,
        'value': vote
      },
      type: 'post',
      cache: false,
      success: function (data) {
        toogleVote(voteIcon, vote, data, false);
      }
    });
  });

  $(".answer-vote").click(function () {
    // Vote on an answer.
    var voteIcon = $(this);
    var answer = $(this).closest(".answer").attr("answer-id");
    if ($(this).hasClass("up-vote")) {
      vote = "U";
    } else {
      $('#answerDownVote').addClass('voted');
      $('#answerUpVote').removeClass('voted');
    }
    $.ajax({
      url: '/qa/answer/vote/',
      data: {
        'answer': answer,
        'value': vote
      },
      type: 'post',
      cache: false,
      success: function (data) {
        toogleVote(voteIcon, vote, data, true);
      }
    });
  });

  $("#acceptAnswer").click(function () {
    // Mark an answer as accepted.
    var span = $(this);
    var answer = $(this).closest(".answer").attr("answer-id");
    $.ajax({
      url: '/qa/accept-answer/',
      data: {
        'answer': answer
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $("#acceptAnswer").removeClass("accepted");
        $("#acceptAnswer").prop("title", "Click to accept the answer");
        $("#acceptAnswer").addClass("accepted");
        $("#acceptAnswer").prop("title", "Click to unaccept the answer");
      }
    });
  });
});
