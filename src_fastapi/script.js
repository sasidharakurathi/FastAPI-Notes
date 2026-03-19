(function (c, l, a, r, i, t, y) {
    c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments) };
    t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
    y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
})(window, document, "clarity", "script", "vxhj0j0zwn");

(function () {
    const pages = Array.from(document.querySelectorAll('.page'));
    const tocContainer = document.getElementById('toc');
    const prevBtn = document.getElementById('btn-prev-page');
    const nextBtn = document.getElementById('btn-next-page');
    const topBtn = document.getElementById('btn-top');
    const linkStatus = document.getElementById('link-status');
    if (!pages.length || !prevBtn || !nextBtn || !topBtn) {
        return;
    }

    let currentPage = 0;
    let activeAnimation = null;

    function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function animateTo(targetY, duration) {
        const startY = window.scrollY || document.documentElement.scrollTop || 0;
        const maxY = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
        const clampedTarget = Math.min(Math.max(targetY, 0), maxY);
        const distance = clampedTarget - startY;

        if (Math.abs(distance) < 1) {
            window.scrollTo(0, clampedTarget);
            return;
        }

        if (activeAnimation) {
            cancelAnimationFrame(activeAnimation);
            activeAnimation = null;
        }

        const startTime = performance.now();

        function step(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = easeInOutCubic(progress);
            window.scrollTo(0, startY + (distance * eased));

            if (progress < 1) {
                activeAnimation = requestAnimationFrame(step);
            } else {
                activeAnimation = null;
            }
        }

        activeAnimation = requestAnimationFrame(step);
    }

    function getCurrentPageIndex() {
        const mid = window.innerHeight * 0.5;
        let bestIndex = 0;
        let bestDistance = Number.POSITIVE_INFINITY;

        pages.forEach(function (page, index) {
            const rect = page.getBoundingClientRect();
            const pageMid = rect.top + rect.height * 0.5;
            const distance = Math.abs(pageMid - mid);
            if (distance < bestDistance) {
                bestDistance = distance;
                bestIndex = index;
            }
        });

        return bestIndex;
    }

    function updateButtonStates() {
        currentPage = getCurrentPageIndex();
        prevBtn.disabled = currentPage <= 0;
        nextBtn.disabled = currentPage >= pages.length - 1;
    }

    function scrollToPage(index) {
        if (index < 0 || index >= pages.length) {
            return;
        }
        const targetY = pages[index].offsetTop;
        animateTo(targetY, 560);
    }

    function getPreviewUrl(targetSelector) {
        return window.location.origin + window.location.pathname + targetSelector;
    }

    function showLinkStatus(targetSelector) {
        if (!linkStatus || !targetSelector) {
            return;
        }

        linkStatus.textContent = getPreviewUrl(targetSelector);
        linkStatus.classList.add('is-visible');
    }

    function hideLinkStatus() {
        if (!linkStatus) {
            return;
        }

        linkStatus.classList.remove('is-visible');
    }

    prevBtn.addEventListener('click', function () {
        updateButtonStates();
        scrollToPage(currentPage - 1);
    });

    nextBtn.addEventListener('click', function () {
        updateButtonStates();
        scrollToPage(currentPage + 1);
    });

    topBtn.addEventListener('click', function () {
        animateTo(0, 560);
    });

    if (tocContainer) {
        tocContainer.addEventListener('mouseover', function (event) {
            const target = event.target;
            if (!(target instanceof Element)) {
                return;
            }

            const link = target.closest('.toc-link[data-target]');
            if (!(link instanceof HTMLElement)) {
                hideLinkStatus();
                return;
            }

            showLinkStatus(link.dataset.target || '');
        });

        tocContainer.addEventListener('mouseout', function (event) {
            const relatedTarget = event.relatedTarget;
            if (relatedTarget instanceof Node && tocContainer.contains(relatedTarget)) {
                return;
            }

            hideLinkStatus();
        });

        tocContainer.addEventListener('focusin', function (event) {
            const target = event.target;
            if (!(target instanceof HTMLElement)) {
                return;
            }

            const link = target.closest('.toc-link[data-target]');
            if (!(link instanceof HTMLElement)) {
                return;
            }

            showLinkStatus(link.dataset.target || '');
        });

        tocContainer.addEventListener('focusout', function (event) {
            const relatedTarget = event.relatedTarget;
            if (relatedTarget instanceof Node && tocContainer.contains(relatedTarget)) {
                return;
            }

            hideLinkStatus();
        });

        tocContainer.addEventListener('click', function (event) {
            const target = event.target;
            if (!(target instanceof Element)) {
                return;
            }

            const link = target.closest('.toc-link[data-target]');
            if (!(link instanceof HTMLElement)) {
                return;
            }

            const targetSelector = link.dataset.target;
            if (!targetSelector || targetSelector.length < 2) {
                return;
            }

            const section = document.querySelector(targetSelector);
            if (!(section instanceof HTMLElement)) {
                return;
            }

            event.preventDefault();
            hideLinkStatus();
            animateTo(section.offsetTop, 620);

            if (history && typeof history.replaceState === 'function') {
                history.replaceState(null, '', targetSelector);
            }
        });
    }

    window.addEventListener('scroll', updateButtonStates, { passive: true });
    window.addEventListener('resize', updateButtonStates);
    updateButtonStates();

    // Keyboard navigation (ArrowLeft/Right for prev/next page)
    document.addEventListener('keydown', function (event) {
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }
        if (event.key === 'ArrowLeft') {
            updateButtonStates();
            scrollToPage(currentPage - 1);
        } else if (event.key === 'ArrowRight') {
            updateButtonStates();
            scrollToPage(currentPage + 1);
        }
    });

    // Reading progress bar
    var progressBar = document.getElementById('progress-bar');
    if (progressBar) {
        window.addEventListener('scroll', function () {
            var scrollTop = window.scrollY || document.documentElement.scrollTop || 0;
            var docHeight = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
            var scrollPercent = (scrollTop / docHeight) * 100;
            progressBar.style.width = scrollPercent + '%';
        }, { passive: true });
    }

    // Page counter in the Top button
    function updatePageCounter() {
        var idx = getCurrentPageIndex();
        topBtn.textContent = (idx + 1) + ' / ' + pages.length;
    }
    window.addEventListener('scroll', updatePageCounter, { passive: true });
    updatePageCounter();

    // Deep linking: scroll to hash target on page load
    if (window.location.hash && window.location.hash.length > 1) {
        var target = document.querySelector(window.location.hash);
        if (target instanceof HTMLElement) {
            setTimeout(function () {
                animateTo(target.offsetTop, 620);
            }, 300);
        }
    }
})();
