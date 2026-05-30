(function () {
    'use strict';

    var TOUR_SEEN_KEY = 'pqcTourSeen';
    var TOUR_PHASE_KEY = 'pqcTourPhase';

    // Poll until an element matching `selector` exists in the DOM, then invoke
    // `callback`. Gives up after `maxMs` milliseconds.
    function waitForElement(selector, callback, maxMs) {
        var elapsed = 0;
        var interval = 150;
        var timer = setInterval(function () {
            var el = document.querySelector(selector);
            if (el) {
                clearInterval(timer);
                callback(el);
            } else if (elapsed >= (maxMs || 8000)) {
                clearInterval(timer);
            }
            elapsed += interval;
        }, interval);
    }

    // -------------------------------------------------------------------------
    // Tour step definitions
    // -------------------------------------------------------------------------

    var overviewSteps = [
        {
            title: 'Welcome to PQC Signatures',
            intro:
                'This webapp lets you explore and compare Post-Quantum Cryptography (PQC) digital ' +
                ' signature algorithms. This short tour explains how to use the website. <strong>It ' +
                'will only take a minute!</strong>',
        },
        {
            element: '#alg-search',
            title: 'Algorithm Search',
            intro:
                'Type here to filter algorithms by name. For example, try <em>ML-DSA</em> or ' +
                '<em>MAYO</em> to jump straight to a family of schemes.',
        },
        {
            element: '#nist-level-filter-section',
            title: 'NIST Security Level',
            intro:
                'Toggle security levels to narrow the list. Levels 1 to 5 map to the official ' +
                'NIST categories. <strong>Level 0 is not a standard NIST level</strong> and ' +
                'we use it to mark classical algorithms such as Rivest-Shamir-Adleman (RSA) ' +
                'and Elliptic Curve Cryptography (ECC) that offer <em>no</em> quantum-safety.',
        },
        {
            element: '#sizes-filter-section',
            title: 'Key &amp; Signature Sizes',
            intro:
                'Drag these range sliders to keep only algorithms whose <strong>public key</strong> ' +
                ', <strong>private key</strong>, and <strong>signature</strong> sizes fall within ' +
                'your requirements.',
        },
        {
            element: '#performance-filter-section',
            title: 'Performance',
            intro:
                'Filter by the speed of the three public operations: ' +
                '<strong>key pair generation</strong>, <strong>signing</strong>, and ' +
                '<strong>signature verification</strong>.',
        },
        {
            element: '#dataset-selector',
            title: 'Benchmark Dataset',
            intro:
                'Benchmarks were run on different hardware platforms. Switch between ' +
                'datasets here to see how algorithm performance changes across machines.',
        },
        {
            element: '#reset-button',
            title: 'Reset All Filters',
            intro:
                'Made a mess of the filters? Click <strong>Reset All</strong> to restore every ' +
                'slider and checkbox to its default value and show all algorithms at once.',
        },
        {
            element: '#content-overview',
            title: 'Algorithm Overview',
            intro:
                'Algorithms matching your filters are shown here as radar charts. Each chart has ' +
                'five axes: public key size, private key size, signature size, signing time, and ' +
                'verification time. <strong>The smaller the enclosed area, the better</strong>. ' +
                'It means smaller keys and signatures, and faster operations.',
        },
        {
            element: '#content-overview',
            title: 'Select Algorithms to Compare',
            intro:
                'We have pre-selected five algorithms for you: <strong>RSA (2048)</strong>, ' +
                '<strong>P-256</strong>, <strong>ML-DSA-44</strong>, <strong>MAYO-1</strong>, ' +
                'and one variant of <strong>SLH-DSA</strong>. ' +
                'You can tick the checkbox above any radar chart to change the selection ' +
                '(up to 5 algorithms). Click Next when you are ready.',
        },
        {
            element: '#compare-button',
            title: 'Compare',
            intro:
                'Once you have selected some algorithms, click <strong>Compare</strong> to open ' +
                'the detailed comparison view. The tour will continue there automatically.',
            position: 'bottom',
        },
    ];

    var compareSteps = [
        {
            title: 'Detailed Comparison',
            intro:
                'Here you can analyse the selected algorithms side by side. The view has two ' +
                'parts: a <strong>radar chart</strong> and a <strong>raw data table</strong>.',
        },
        {
            element: '#compare-radar',
            title: 'Radar Chart',
            intro:
                'All selected algorithms are overlaid on one chart, each in a different colour. ' +
                'You can highlight the area of one algorithm by moving your mouse on top of the ' +
                'algorithm\'s name in the legend. An algorithm with a <strong>smaller enclosed ' +
                'area</strong> uses smaller keys and signatures, and runs faster public ' +
                'operations, so closer to the centre is always better.',
        },
        {
            element: '#compare-table',
            title: 'Data Table',
            intro:
                'The table lists exact values for every metric: <strong>NIST security level</strong> ' +
                ', <strong>public key</strong>, <strong>private key</strong>, and ' +
                '<strong>signature</strong> sizes in <em>bytes</em>, and ' +
                '<strong>key generation</strong>, <strong>signing</strong>, and ' +
                '<strong>verification</strong> times in <em>microseconds</em>. Use it for precise ' +
                'numerical comparisons.',
        },
        {
            title: 'Tour Complete!',
            intro:
                '<strong>You are all set!</strong> Remember: <strong>1)</strong> use the ' +
                'sidebar <em>filters</em> to narrow down candidates, <strong>2)</strong> ' +
                '<em>select</em> up to five algorithms, and <strong>3)</strong> open the ' +
                '<em>comparison</em> page for a detailed view. You can restart this tour ' +
                'at any time using the <strong>?</strong> button in the top-right corner.',
        },
    ];

    // -------------------------------------------------------------------------
    // Algorithm pre-selection for the tour
    // -------------------------------------------------------------------------

    var TOUR_ALGORITHMS = [
        'RSA-PSS-2048',
        'P-256',
        'ML-DSA-44',
        'MAYO-1',
        'SLH_DSA_PURE_SHA2_128F',
    ];

    // Find the <input type="checkbox"> for a given algorithm.
    // Primary strategy: match via Dash's JSON-serialised pattern-matching id
    // using JS indexOf — avoids CSS selector issues with { and " characters.
    // Fallback: walk the Mantine Checkbox label text for robustness.
    function findCheckboxInput(algName) {
        var needle = '"checkbox-' + algName + '"';
        var candidates = document.querySelectorAll('#content-overview [id]');
        for (var i = 0; i < candidates.length; i++) {
            var id = candidates[i].getAttribute('id');
            if (id && id.indexOf(needle) !== -1) {
                var input = candidates[i].querySelector('input[type="checkbox"]');
                if (input) return input;
            }
        }
        // Fallback: label text search (strips U+200B added by soft_break_on_underscore)
        var inputs = document.querySelectorAll('#content-overview input[type="checkbox"]');
        for (var j = 0; j < inputs.length; j++) {
            var root = inputs[j].closest('.mantine-Checkbox-root');
            if (!root) continue;
            var label = root.querySelector('label, [class*="Checkbox-label"]');
            if (!label) continue;
            var text = label.textContent.replace(/​/g, '').trim();
            if (text === algName) return inputs[j];
        }
        return null;
    }

    // Reset all filters first (so target algorithms are guaranteed to be
    // visible), then click each algorithm. The 2000 ms base delay gives the
    // full reset → update_filtered_algorithms → update_shown_charts callback
    // chain time to complete before any click lands, preventing a race where
    // the reset re-render unchecks an early click. After all clicks, restore
    // the scroll position so the tooltip stays visible.
    function preselectTourAlgorithms() {
        var resetBtn = document.querySelector('#reset-button');
        if (resetBtn) resetBtn.click();

        TOUR_ALGORITHMS.forEach(function (name, i) {
            setTimeout(function () {
                var input = findCheckboxInput(name);
                if (input && !input.checked) input.click();
            }, 2000 + i * 300);
        });

        setTimeout(function () {
            var main = document.querySelector('.mantine-AppShell-main');
            if (main) main.scrollTop = 0;
        }, 2000 + TOUR_ALGORITHMS.length * 300 + 300);
    }

    // -------------------------------------------------------------------------
    // Helpers that resolve selector strings to DOM elements at call-time
    // -------------------------------------------------------------------------

    function resolveSteps(steps) {
        return steps.map(function (step) {
            var s = Object.assign({}, step);
            if (s.element) {
                s.element = document.querySelector(s.element);
            }
            return s;
        });
    }

    function commonOptions(extra) {
        return Object.assign(
            {
                showProgress: true,
                showBullets: false,
                exitOnOverlayClick: false,
                exitOnEsc: true,
                scrollToElement: true,
                disableInteraction: false,
                nextLabel: 'Next',
                prevLabel: 'Back',
                skipLabel: '✕',
            },
            extra || {}
        );
    }

    // -------------------------------------------------------------------------
    // Public API
    // -------------------------------------------------------------------------

    window.pqcTour = {

        // Start the overview-page tour. Pass force=true to ignore the
        // "already seen" flag (used by the Replay button).
        startOverview: function (force) {
            if (!force && localStorage.getItem(TOUR_SEEN_KEY)) return;
            if (typeof introJs === 'undefined') return;

            // Wait until the overview grid has rendered at least one chart.
            waitForElement('#content-overview', function () {
                var tour = introJs();
                tour.setOptions(
                    commonOptions({
                        steps: resolveSteps(overviewSteps),
                        doneLabel: 'Go to Compare',
                    })
                );

                // Pre-select the five demo algorithms when the user reaches
                // the "Select Algorithms to Compare" step (index 8).
                tour.onchange(function () {
                    if (tour.currentStep() === 8) {
                        preselectTourAlgorithms();
                    }
                });

                // User completed all steps: mark phase 2, then navigate to
                // the Compare page so the tour continues there automatically.
                tour.oncomplete(function () {
                    localStorage.setItem(TOUR_PHASE_KEY, '2');
                    localStorage.setItem(TOUR_SEEN_KEY, 'true');
                    var compareBtn = document.querySelector('#compare-button');
                    if (compareBtn) {
                        var link = compareBtn.closest('a');
                        if (link) link.click();
                    }
                });

                // User exited early: clean up. If oncomplete already set the
                // phase key to '2' (normal completion), leave it so the compare
                // tour can pick it up — onexit fires after oncomplete in Intro.js.
                tour.onexit(function () {
                    localStorage.setItem(TOUR_SEEN_KEY, 'true');
                    if (localStorage.getItem(TOUR_PHASE_KEY) !== '2') {
                        localStorage.removeItem(TOUR_PHASE_KEY);
                    }
                });

                tour.start();
            }, 8000);
        },

        // Start the compare-page tour. Only runs if phase 2 was stored by the
        // overview tour.
        startCompare: function () {
            if (localStorage.getItem(TOUR_PHASE_KEY) !== '2') return;
            if (typeof introJs === 'undefined') return;

            // Wait for the radar chart to appear (requires algorithms to be
            // selected before navigating here).
            waitForElement('#compare-radar', function () {
                var tour = introJs();
                tour.setOptions(
                    commonOptions({
                        steps: resolveSteps(compareSteps),
                        doneLabel: 'Done!',
                    })
                );

                tour.oncomplete(function () {
                    localStorage.removeItem(TOUR_PHASE_KEY);
                    var overviewBtn = document.querySelector('#overview-button');
                    if (overviewBtn) {
                        var link = overviewBtn.closest('a');
                        if (link) link.click();
                    }
                    setTimeout(function () {
                        var resetBtn = document.querySelector('#reset-button');
                        if (resetBtn) resetBtn.click();
                    }, 300);
                });

                tour.onexit(function () {
                    localStorage.removeItem(TOUR_PHASE_KEY);
                });

                tour.start();
            }, 10000);
        },

        // Reset tour state and restart from the overview page.
        restart: function () {
            localStorage.removeItem(TOUR_SEEN_KEY);
            localStorage.removeItem(TOUR_PHASE_KEY);

            // Navigate to overview if we are not already there, then start.
            var overviewAnchor = document.querySelector('#overview-button');
            if (overviewAnchor) {
                var link = overviewAnchor.closest('a');
                if (link) link.click();
            }
            setTimeout(function () {
                window.pqcTour.startOverview(true);
            }, 400);
        },
    };
})();
