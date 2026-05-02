/* ════════════════════════════════════════════════════════════════
   CJHuang Group — interactions
   - rAF-throttled scroll handlers
   - IntersectionObserver for reveals
   - Animated news filter (fade out → unhide → fade in)
   - Accessible hamburger (aria-expanded sync)
   ════════════════════════════════════════════════════════════════ */

(() => {
    'use strict';

    /* ── rAF-throttle utility ───────────────────────────────── */
    const rafThrottle = (fn) => {
        let queued = false;
        return (...args) => {
            if (queued) return;
            queued = true;
            requestAnimationFrame(() => {
                fn(...args);
                queued = false;
            });
        };
    };

    /* ── Reveal on scroll ───────────────────────────────────── */
    const revealTargets = document.querySelectorAll(
        'section, .research-card, .quick-nav-card, .news-item, ' +
        '.research-detail-card, .technique-card, .team-member, ' +
        '.equipment-card, .position-card, .stat-card'
    );

    revealTargets.forEach(el => el.classList.add('reveal'));

    if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        revealTargets.forEach(el => io.observe(el));
    } else {
        // No IO support — just show everything
        revealTargets.forEach(el => el.classList.add('is-visible'));
    }

    /* ── Navbar shadow on scroll (rAF-throttled) ────────────── */
    const navbar = document.getElementById('navbar');
    if (navbar) {
        const onScroll = rafThrottle(() => {
            navbar.classList.toggle('scrolled', window.scrollY > 24);
        });
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ── Hamburger / mobile menu (with aria-expanded) ───────── */
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');

    if (hamburger && mobileMenu) {
        hamburger.setAttribute('aria-expanded', 'false');
        hamburger.setAttribute('aria-controls', 'mobile-menu');

        const setMenu = (open) => {
            mobileMenu.classList.toggle('open', open);
            hamburger.classList.toggle('open', open);
            hamburger.setAttribute('aria-expanded', String(open));
            document.body.style.overflow = open ? 'hidden' : '';
        };

        hamburger.addEventListener('click', () => {
            setMenu(!mobileMenu.classList.contains('open'));
        });

        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => setMenu(false));
        });

        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
                setMenu(false);
                hamburger.focus();
            }
        });
    }

    /* ── Back to top ────────────────────────────────────────── */
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        const onBackScroll = rafThrottle(() => {
            backToTop.classList.toggle('visible', window.scrollY > 600);
        });
        window.addEventListener('scroll', onBackScroll, { passive: true });

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    /* ── Smooth scrolling for in-page anchors ───────────────── */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const id = this.getAttribute('href');
            if (id === '#' || id.length < 2) return;
            const target = document.querySelector(id);
            if (!target) return;
            e.preventDefault();
            const offset = (navbar?.offsetHeight ?? 64) + 16;
            window.scrollTo({
                top: target.getBoundingClientRect().top + window.scrollY - offset,
                behavior: 'smooth'
            });
        });
    });

    /* ── Quick-nav cards (replaces inline onclick) ──────────── */
    document.querySelectorAll('[data-href]').forEach(card => {
        card.style.cursor = 'pointer';
        card.setAttribute('role', 'link');
        card.setAttribute('tabindex', '0');
        const go = () => { window.location.href = card.dataset.href; };
        card.addEventListener('click', go);
        card.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
        });
    });

    /* ── Animated news filter ───────────────────────────────── */
    const filterSelect = document.getElementById('news-category-filter');
    if (filterSelect) {
        const items = document.querySelectorAll('.news-item');

        filterSelect.addEventListener('change', function () {
            const cat = this.value;

            // Phase 1: fade out non-matching
            items.forEach(item => {
                const match = (cat === 'all' || cat === item.dataset.category);
                if (!match) item.classList.add('is-hiding');
            });

            // Phase 2: after fade, hide + reveal new matches
            setTimeout(() => {
                items.forEach(item => {
                    const match = (cat === 'all' || cat === item.dataset.category);
                    item.classList.toggle('hidden', !match);
                    item.classList.remove('is-hiding');
                });
            }, 200);
        });
    }

    /* ── Research page sticky ToC active state ──────────────── */
    const tocLinks = document.querySelectorAll('.toc-link');
    if (tocLinks.length) {
        const sectionMap = new Map();
        tocLinks.forEach(link => {
            const id = link.dataset.target;
            const section = document.getElementById(id);
            if (section) sectionMap.set(section, link);
        });

        if ('IntersectionObserver' in window) {
            const tocIO = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    const link = sectionMap.get(entry.target);
                    if (!link) return;
                    if (entry.isIntersecting) {
                        tocLinks.forEach(l => l.classList.remove('is-active'));
                        link.classList.add('is-active');
                    }
                });
            }, {
                rootMargin: '-30% 0px -60% 0px',
                threshold: 0
            });
            sectionMap.forEach((_, section) => tocIO.observe(section));
        }
    }

    /* ── People page tabs (if present) ──────────────────────── */
    const tabs = document.querySelectorAll('.people-tab');
    if (tabs.length) {
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.dataset.tab;
                tabs.forEach(t => t.classList.toggle('active', t === tab));
                document.querySelectorAll('.tab-panel').forEach(panel => {
                    panel.classList.toggle('active', panel.id === target);
                });
            });
        });
    }

})();
