$(document).ready(function () {
  // add toggle functionality to abstract, award and bibtex buttons
  $("a.abstract").click(function () {
    $(this).parent().parent().find(".abstract.hidden").toggleClass("open");
    $(this).parent().parent().find(".award.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden.open").toggleClass("open");
  });
  $("a.award").click(function () {
    $(this).parent().parent().find(".abstract.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".award.hidden").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden.open").toggleClass("open");
  });
  $("a.bibtex").click(function () {
    $(this).parent().parent().find(".abstract.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".award.hidden.open").toggleClass("open");
    $(this).parent().parent().find(".bibtex.hidden").toggleClass("open");
  });
  $("a").removeClass("waves-effect waves-light");

  // bootstrap-toc
  if ($("#toc-sidebar").length) {
    // remove related publications years from the TOC
    $(".publications h2").each(function () {
      $(this).attr("data-toc-skip", "");
    });
    var navSelector = "#toc-sidebar";
    var $myNav = $(navSelector);
    Toc.init($myNav);
    $("body").scrollspy({
      target: navSelector,
    });
  }

  // add css to jupyter notebooks
  const cssLink = document.createElement("link");
  cssLink.href = "../css/jupyter.css";
  cssLink.rel = "stylesheet";
  cssLink.type = "text/css";

  let jupyterTheme = determineComputedTheme();

  $(".jupyter-notebook-iframe-container iframe").each(function () {
    $(this).contents().find("head").append(cssLink);

    if (jupyterTheme == "dark") {
      $(this).bind("load", function () {
        $(this).contents().find("body").attr({
          "data-jp-theme-light": "false",
          "data-jp-theme-name": "JupyterLab Dark",
        });
      });
    }
  });

  // trigger popovers (non-annotation)
  $('[data-toggle="popover"]').popover({
    trigger: "hover",
  });

  // Annotation tooltips with MathJax support
  function typesetAnnotation($tooltip) {
    if (typeof MathJax === "undefined") return;
    // MathJax v3: clear previous typeset marks, then re-typeset
    if (MathJax.startup && MathJax.startup.promise) {
      MathJax.startup.promise.then(function () {
        MathJax.typesetClear([$tooltip[0]]);
        MathJax.typesetPromise([$tooltip[0]]);
      });
    }
  }

  $(".annotation-container").each(function () {
    var $container = $(this);
    var $tooltip = $container.find(".annotation-tooltip");
    var mathjaxDone = false;

    $container.on("mouseenter", function () {
      if (!mathjaxDone) {
        typesetAnnotation($tooltip);
        mathjaxDone = true;
      }
    });

    // Also support click/tap for mobile
    $container.find(".annotation-toggle").on("click", function (e) {
      e.stopPropagation();
      $container.toggleClass("active");
      if (!mathjaxDone) {
        typesetAnnotation($tooltip);
        mathjaxDone = true;
      }
    });
  });

  // Close annotation tooltips when clicking outside
  $(document).on("click", function () {
    $(".annotation-container.active").removeClass("active");
  });

  // Clickable publication cards — navigate to publisher/preprint URL
  $(".publications ol.bibliography li").each(function () {
    var $li = $(this);
    var $link = $li.find(".pub-link");
    if ($link.length) {
      var url = $link.data("url");
      $li.css("cursor", "pointer");
      $li.on("click", function (e) {
        // Don't navigate if clicking on an interactive element
        if ($(e.target).closest("a, button, .annotation-container, .author, .links, .badges, .hidden.open").length) {
          return;
        }
        window.open(url, "_blank");
      });
    }
  });
});
