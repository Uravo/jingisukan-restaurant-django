(function () {
  function escapeHtml(value) {
    return value.replace(/[&<>"]/g, function (char) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[char];
    });
  }

  function plainTextToHtml(value) {
    var trimmed = value.trim();
    if (!trimmed) return "";
    if (/<\/?[a-z][\s\S]*>/i.test(trimmed)) return trimmed;
    return trimmed.split(/\n\s*\n/).map(function (part) {
      return "<p>" + escapeHtml(part).replace(/\n/g, "<br>") + "</p>";
    }).join("");
  }

  function syncEditor(textarea, editor) {
    textarea.value = editor.innerHTML.trim();
  }

  function exec(command, value) {
    document.execCommand(command, false, value || null);
  }

  function initRichText(textarea) {
    if (!textarea || textarea.dataset.richReady === "true") return;
    textarea.dataset.richReady = "true";
    textarea.classList.add("rich-text-source");

    var wrap = document.createElement("div");
    wrap.className = "rich-text-wrap";

    var toolbar = document.createElement("div");
    toolbar.className = "rich-text-toolbar";

    var buttons = [
      ["Bold", "bold"],
      ["Italic", "italic"],
      ["H2", "formatBlock", "h2"],
      ["H3", "formatBlock", "h3"],
      ["List", "insertUnorderedList"],
      ["Link", "createLink"],
      ["Clear", "removeFormat"]
    ];

    buttons.forEach(function (item) {
      var button = document.createElement("button");
      button.type = "button";
      button.textContent = item[0];
      button.addEventListener("click", function () {
        editor.focus();
        if (item[1] === "createLink") {
          var url = window.prompt("Link URL");
          if (url) exec("createLink", url);
        } else if (item[1] === "formatBlock") {
          exec("formatBlock", item[2]);
        } else {
          exec(item[1]);
        }
        syncEditor(textarea, editor);
      });
      toolbar.appendChild(button);
    });

    var editor = document.createElement("div");
    editor.className = "rich-text-editor";
    editor.contentEditable = "true";
    editor.innerHTML = plainTextToHtml(textarea.value);
    editor.addEventListener("input", function () { syncEditor(textarea, editor); });
    editor.addEventListener("blur", function () { syncEditor(textarea, editor); });

    wrap.appendChild(toolbar);
    wrap.appendChild(editor);
    textarea.parentNode.insertBefore(wrap, textarea.nextSibling);

    var form = textarea.closest("form");
    if (form) {
      form.addEventListener("submit", function () { syncEditor(textarea, editor); });
    }
  }

  function initLanguageTabs(root) {
    root.querySelectorAll("[data-admin-language-tabs]").forEach(function (container) {
      var tabs = Array.prototype.slice.call(container.querySelectorAll("[data-admin-tab]"));
      var panels = Array.prototype.slice.call(container.querySelectorAll("[data-admin-panel]"));
      function activate(code) {
        tabs.forEach(function (tab) {
          var active = tab.dataset.adminTab === code;
          tab.classList.toggle("is-active", active);
          tab.setAttribute("aria-selected", active ? "true" : "false");
        });
        panels.forEach(function (panel) {
          var active = panel.dataset.adminPanel === code;
          panel.hidden = !active;
          panel.classList.toggle("is-active", active);
        });
      }
      tabs.forEach(function (tab) {
        tab.addEventListener("click", function () { activate(tab.dataset.adminTab); });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initLanguageTabs(document);
    document.querySelectorAll("textarea[data-rich-text]").forEach(initRichText);
  });
})();
