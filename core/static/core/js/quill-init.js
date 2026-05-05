(function () {
  var toolbars = {
    rich: [
      [{ header: [2, 3, false] }],
      ['bold', 'italic', 'underline'],
      [{ list: 'ordered' }, { list: 'bullet' }],
      ['blockquote', 'link'],
      ['clean']
    ],
    simple: [
      ['bold', 'italic', 'underline'],
      [{ list: 'ordered' }, { list: 'bullet' }],
      ['link'],
      ['clean']
    ]
  };

  function initQuill() {
    document.querySelectorAll('textarea[data-quill]').forEach(function (textarea) {
      if (textarea._quillInitialized) return;
      textarea._quillInitialized = true;

      var mode = textarea.getAttribute('data-quill');
      var wrapper = document.createElement('div');
      textarea.parentNode.insertBefore(wrapper, textarea);
      textarea.style.display = 'none';

      var quill = new Quill(wrapper, {
        theme: 'snow',
        modules: { toolbar: toolbars[mode] || toolbars.simple }
      });

      if (textarea.value) {
        quill.root.innerHTML = textarea.value;
      }

      textarea.closest('form').addEventListener('submit', function () {
        var html = quill.root.innerHTML;
        textarea.value = (html === '<p><br></p>') ? '' : html;
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initQuill);
  } else {
    initQuill();
  }
})();
