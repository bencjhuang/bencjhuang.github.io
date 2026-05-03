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

    /* ── Gallery filter + lightbox ──────────────────────────── */
    const galleryFilters = document.querySelectorAll('.gallery-filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');

    if (galleryFilters.length && galleryItems.length) {
        galleryFilters.forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;
                galleryFilters.forEach(b => b.classList.toggle('active', b === btn));

                galleryItems.forEach(item => {
                    const match = (filter === 'all' || item.dataset.category === filter);
                    if (!match) item.classList.add('is-hiding');
                });
                setTimeout(() => {
                    galleryItems.forEach(item => {
                        const match = (filter === 'all' || item.dataset.category === filter);
                        item.classList.toggle('hidden', !match);
                        item.classList.remove('is-hiding');
                    });
                }, 200);
            });
        });
    }

    const lightbox = document.getElementById('lightbox');
    if (lightbox && galleryItems.length) {
        const lbImg = document.getElementById('lightbox-img');
        const lbCap = document.getElementById('lightbox-caption');
        const lbClose = document.getElementById('lightbox-close');
        const lbPrev = document.getElementById('lightbox-prev');
        const lbNext = document.getElementById('lightbox-next');

        const visibleItems = () => Array.from(galleryItems).filter(el =>
            !el.classList.contains('hidden') && el.querySelector('img'));
        let currentIndex = 0;

        const showAt = (i) => {
            const items = visibleItems();
            if (!items.length) return;
            currentIndex = (i + items.length) % items.length;
            const item = items[currentIndex];
            const img = item.querySelector('img');
            lbImg.src = img.src;
            lbImg.alt = img.alt;
            lbCap.textContent = item.querySelector('.gallery-caption p')?.textContent ?? '';
        };

        const open = (item) => {
            const items = visibleItems();
            currentIndex = items.indexOf(item);
            if (currentIndex < 0) currentIndex = 0;
            showAt(currentIndex);
            lightbox.hidden = false;
            document.body.style.overflow = 'hidden';
            lbClose.focus();
        };

        const close = () => {
            lightbox.hidden = true;
            document.body.style.overflow = '';
        };

        galleryItems.forEach(item => {
            const img = item.querySelector('img');
            if (!img) return;
            item.style.cursor = 'zoom-in';
            item.addEventListener('click', () => open(item));
        });

        lbClose.addEventListener('click', close);
        lbPrev.addEventListener('click', (e) => { e.stopPropagation(); showAt(currentIndex - 1); });
        lbNext.addEventListener('click', (e) => { e.stopPropagation(); showAt(currentIndex + 1); });
        lightbox.addEventListener('click', (e) => { if (e.target === lightbox) close(); });

        document.addEventListener('keydown', (e) => {
            if (lightbox.hidden) return;
            if (e.key === 'Escape') close();
            else if (e.key === 'ArrowLeft') showAt(currentIndex - 1);
            else if (e.key === 'ArrowRight') showAt(currentIndex + 1);
        });
    }

    /* ── Publications: assign stable paper numbers ──────────── */
    const peerReviewedPubs = document.querySelectorAll('#peer-reviewed .publication');
    if (peerReviewedPubs.length) {
        const total = peerReviewedPubs.length;
        peerReviewedPubs.forEach((pub, i) => {
            pub.setAttribute('data-num', total - i);
        });
    }

    /* ── Publications: filter + search ──────────────────────── */
    const pubSearch = document.getElementById('pub-search');
    const pubChips = document.querySelectorAll('.pub-chip');
    const pubGroups = document.querySelectorAll('.year-group[data-year]');
    const pubResultCount = document.getElementById('pub-result-count');

    if (pubSearch || pubChips.length) {
        let activeFilter = 'all';
        let query = '';

        const peerReviewedSection = document.getElementById('peer-reviewed');
        const conferencesSection = document.getElementById('conferences');
        const patentsSection = document.getElementById('patents');

        const applyFilter = () => {
            const q = query.trim().toLowerCase();
            const filter = activeFilter;
            const yearMatch = filter.match(/^year-(\d{4})$/);
            const targetYear = yearMatch ? yearMatch[1] : null;

            const showArticles  = (filter === 'all' || targetYear !== null);
            const showConferences = (filter === 'all' || filter === 'conferences');
            const showPatents     = (filter === 'all' || filter === 'patents');

            if (peerReviewedSection) peerReviewedSection.style.display = showArticles ? '' : 'none';
            if (conferencesSection)  conferencesSection.style.display  = showConferences ? '' : 'none';
            if (patentsSection)      patentsSection.style.display      = showPatents ? '' : 'none';

            let visible = 0;

            // Peer-reviewed by year-group
            pubGroups.forEach(group => {
                const groupYearMatch = (targetYear === null || group.dataset.year === targetYear);
                let groupVisible = 0;

                group.querySelectorAll('.publication').forEach(pub => {
                    const text = pub.textContent.toLowerCase();
                    const queryMatch = q === '' || text.includes(q);
                    const show = showArticles && groupYearMatch && queryMatch;
                    pub.classList.toggle('is-hidden', !show);
                    if (show) groupVisible++;
                });

                group.classList.toggle('is-hidden', groupVisible === 0);
                if (showArticles) visible += groupVisible;
            });

            // Conferences
            document.querySelectorAll('#conferences .publication').forEach(pub => {
                const text = pub.textContent.toLowerCase();
                const queryMatch = q === '' || text.includes(q);
                const show = showConferences && queryMatch;
                pub.classList.toggle('is-hidden', !show);
                if (show) visible++;
            });

            // Patents
            document.querySelectorAll('#patents .publication').forEach(pub => {
                const text = pub.textContent.toLowerCase();
                const queryMatch = q === '' || text.includes(q);
                const show = showPatents && queryMatch;
                pub.classList.toggle('is-hidden', !show);
                if (show) visible++;
            });

            if (pubResultCount) {
                if (q || filter !== 'all') {
                    pubResultCount.textContent = `${visible} ${visible === 1 ? 'item' : 'items'} match`;
                } else {
                    pubResultCount.textContent = '';
                }
            }
        };

        pubChips.forEach(chip => {
            chip.addEventListener('click', () => {
                pubChips.forEach(c => c.classList.toggle('active', c === chip));
                activeFilter = chip.dataset.filter;
                applyFilter();
            });
        });

        if (pubSearch) {
            let debounce;
            pubSearch.addEventListener('input', () => {
                clearTimeout(debounce);
                debounce = setTimeout(() => {
                    query = pubSearch.value;
                    applyFilter();
                }, 120);
            });
        }
    }

    /* ── Animate stat numbers counting up on scroll ─────────── */
    const statNumbers = document.querySelectorAll('.stat-number[data-count]');
    if (statNumbers.length && 'IntersectionObserver' in window) {
        const easeOut = (t) => 1 - Math.pow(1 - t, 3);
        const animateNumber = (el) => {
            const target = parseInt(el.dataset.count, 10);
            if (isNaN(target)) return;
            const duration = 1200;
            const start = performance.now();

            const tick = (now) => {
                const t = Math.min(1, (now - start) / duration);
                const value = Math.round(target * easeOut(t));
                el.textContent = value.toLocaleString();
                if (t < 1) requestAnimationFrame(tick);
                else el.textContent = target.toLocaleString();
            };
            requestAnimationFrame(tick);
        };

        const statIO = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateNumber(entry.target);
                    statIO.unobserve(entry.target);
                }
            });
        }, { threshold: 0.4 });

        statNumbers.forEach(el => {
            // Start from 0 so the count-up is visible
            el.textContent = '0';
            statIO.observe(el);
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

                tabs.forEach(t => {
                    const isActive = t === tab;
                    t.classList.toggle('active', isActive);
                    t.setAttribute('aria-selected', String(isActive));
                });

                document.querySelectorAll('.tab-panel').forEach(panel => {
                    const isActive = panel.id === ('tab-' + target);
                    panel.classList.toggle('active', isActive);
                });
            });
        });
    }

})();
