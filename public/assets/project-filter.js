/* Progressive enhancement: all approved cases remain readable without JavaScript. */
(function () {
  var grid = document.querySelector('[data-project-grid]');
  if (!grid) return;
  var buttons = document.querySelectorAll('[data-project-filter]');
  var cards = grid.querySelectorAll('[data-project-category]');
  var count = document.querySelector('[data-project-count]');
  var chinese = document.documentElement.lang.indexOf('zh') === 0;
  buttons.forEach(function (button) {
    button.addEventListener('click', function () {
      var category = button.getAttribute('data-project-filter');
      var visible = 0;
      buttons.forEach(function (item) {
        item.setAttribute('aria-pressed', String(item === button));
      });
      cards.forEach(function (card) {
        var show = category === 'all' || card.getAttribute('data-project-category') === category;
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (count) count.textContent = chinese ? visible + ' 个已公开项目' : visible + ' published project' + (visible === 1 ? '' : 's');
    });
  });
}());
