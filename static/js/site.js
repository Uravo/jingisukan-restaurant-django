(function () {
  function csrfToken() {
    const match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function setMenu(header, open) {
    const toggle = header && header.querySelector("[data-toggle]");
    if (!header || !toggle) return;
    header.toggleAttribute("data-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("menu-open", open);
  }

  document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector("[data-header]");
    const toggle = document.querySelector("[data-toggle]");
    const panel = document.querySelector("[data-panel]");
    const modal = document.querySelector("[data-modal]");

    toggle && toggle.addEventListener("click", function () {
      setMenu(header, !header.hasAttribute("data-open"));
    });

    panel && panel.addEventListener("click", function (event) {
      if (event.target && event.target.matches("a")) {
        setMenu(header, false);
      }
    });

    document.querySelectorAll(".lang-switcher--dropdown").forEach(function (details) {
      document.addEventListener("pointerdown", function (event) {
        if (!details.contains(event.target)) details.open = false;
      });
    });

    function openModal() {
      if (!modal) return;
      modal.hidden = false;
      window.setTimeout(function () {
        modal.setAttribute("data-open", "");
        document.body.classList.add("menu-open");
      }, 20);
    }

    function closeModal() {
      if (!modal || modal.hidden) return;
      modal.removeAttribute("data-open");
      window.setTimeout(function () {
        modal.hidden = true;
        document.body.classList.remove("menu-open");
      }, 220);
    }

    document.addEventListener("click", function (event) {
      if (event.target && event.target.matches("[data-close]")) closeModal();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        setMenu(header, false);
        closeModal();
      }
    });

    const form = document.querySelector("[data-booking-form]");
    if (form) {
      form.addEventListener("submit", async function (event) {
        event.preventDefault();
        const message = form.querySelector("[data-message]");
        const submitText = form.querySelector("[data-submit-text]");

        if (!form.checkValidity()) {
          if (message) message.textContent = form.dataset.validationMessage || "Please complete the form.";
          return;
        }

        const formData = new FormData(form);
        const payload = {
          customer_name: String(formData.get("customer_name") || ""),
          phone: String(formData.get("phone") || ""),
          booking_date: String(formData.get("booking_date") || ""),
          booking_time: String(formData.get("booking_time") || ""),
          people_count: Number(formData.get("people_count") || 0),
          locale: form.dataset.locale || "en"
        };

        form.dataset.loading = "true";
        if (submitText) submitText.textContent = form.dataset.submitLoading || "Saving";
        if (message) message.textContent = "";

        try {
          const response = await fetch(form.action, {
            method: "POST",
            headers: {
              "content-type": "application/json",
              "accept": "application/json",
              "X-CSRFToken": csrfToken()
            },
            body: JSON.stringify(payload)
          });

          if (!response.ok) throw new Error("Booking failed");
          form.reset();
          openModal();
        } catch (error) {
          console.error(error);
          if (message) message.textContent = form.dataset.errorMessage || "Sorry, booking could not be saved.";
        } finally {
          delete form.dataset.loading;
          if (submitText) submitText.textContent = form.dataset.submitDefault || "Reserve table";
        }
      });
    }

    if ("IntersectionObserver" in window) {
      const revealEarly = window.matchMedia("(max-width: 759px)").matches;
      const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      }, {
        rootMargin: revealEarly ? "0px 0px 18% 0px" : "0px 0px -8% 0px",
        threshold: revealEarly ? 0.06 : 0.14
      });

      document.querySelectorAll(".reveal").forEach(function (element, index) {
        element.style.transitionDelay = String(Math.min(index % 4, 3) * 60) + "ms";
        observer.observe(element);
      });
    } else {
      document.querySelectorAll(".reveal").forEach(function (element) {
        element.classList.add("visible");
      });
    }
  });
})();
