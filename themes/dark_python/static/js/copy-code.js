(function () {
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    return Promise.resolve();
  }

  function wrapBlock(el) {
    if (!el || el.closest(".code-block-wrap")) return;
    const wrap = document.createElement("div");
    wrap.className = "code-block-wrap";
    el.parentNode.insertBefore(wrap, el);
    wrap.appendChild(el);

    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "code-copy-btn";
    btn.setAttribute("aria-label", "Copy code");
    btn.textContent = "Copy";
    wrap.appendChild(btn);

    btn.addEventListener("click", function () {
      const pre = el.querySelector("pre") || el;
      const text = pre.innerText.replace(/\n$/, "");
      copyText(text).then(
        function () {
          btn.textContent = "Copied!";
          btn.classList.add("copied");
          setTimeout(function () {
            btn.textContent = "Copy";
            btn.classList.remove("copied");
          }, 1600);
        },
        function () {
          btn.textContent = "Failed";
          setTimeout(function () {
            btn.textContent = "Copy";
          }, 1600);
        }
      );
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("article.post .post-content .highlight").forEach(wrapBlock);
    document.querySelectorAll("article.post .post-content > pre").forEach(wrapBlock);
  });
})();
