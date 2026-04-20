document.addEventListener("DOMContentLoaded", () => {
    const reveals = document.querySelectorAll(".reveal");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.14, rootMargin: "0px 0px -30px 0px" }
    );

    reveals.forEach((node) => observer.observe(node));

    const heroVisual = document.querySelector(".hero-visual img");
    if (!heroVisual) {
        return;
    }

    window.addEventListener(
        "scroll",
        () => {
            const offset = Math.min(window.scrollY * 0.06, 18);
            heroVisual.style.transform = `translateY(${offset}px)`;
        },
        { passive: true }
    );
});
