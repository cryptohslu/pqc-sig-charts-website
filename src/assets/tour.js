(function () {
    'use strict';

    var TOUR_SEEN_KEY = 'pqcTourSeen';
    var TOUR_PHASE_KEY = 'pqcTourPhase';

    // Driver.js calls stopImmediatePropagation() on pointerdown in a capture
    // listener, which prevents Firefox from applying the :active CSS state.
    // By registering our capture listeners first (before driverObj.drive() is
    // ever called), we fire before Driver.js's listener and can manually toggle
    // a class to produce the pressed effect cross-browser.
    document.addEventListener('pointerdown', function (e) {
        var btn = e.target.closest && e.target.closest('.driver-popover-footer button');
        if (btn) btn.classList.add('driver-btn-pressed');
    }, true);
    ['pointerup', 'pointercancel'].forEach(function (evt) {
        document.addEventListener(evt, function () {
            document.querySelectorAll('.driver-btn-pressed').forEach(function (btn) {
                btn.classList.remove('driver-btn-pressed');
            });
        }, true);
    });

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
            popover: {
                title: 'Welcome to PQC Signatures',
                description:
                    'This webapp lets you explore and compare Post-Quantum Cryptographic (PQC) digital ' +
                    'signature algorithms. This short tour explains how to use the website. ' +
                    '<strong>It will only take 2-3 minutes!</strong>',
            },
        },
        {
            element: '#alg-search',
            popover: {
                title: 'Algorithm Search',
                description:
                    'Type here to filter algorithms by name. For example, try <em>ML-DSA</em> or ' +
                    '<em>MAYO</em> to jump straight to a family of schemes.',
            },
        },
        {
            element: '#nist-level-filter-section',
            popover: {
                title: 'NIST Security Level',
                description:
                    'Toggle security levels to narrow the list. Levels 1 to 5 map to the official ' +
                    'NIST categories. <strong>Level 0 is not a standard NIST level</strong> and ' +
                    'we use it to mark classical algorithms such as Rivest-Shamir-Adleman (RSA) ' +
                    'and Elliptic Curve Cryptography (ECC) that offer <em>no</em> quantum-safety.',
            },
        },
        {
            element: '#sizes-filter-section',
            popover: {
                title: 'Key &amp; Signature Sizes',
                description:
                    'Drag these range sliders to keep only algorithms whose <strong>public key</strong>, ' +
                    '<strong>private key</strong>, and <strong>signature</strong> sizes fall within ' +
                    'your requirements.',
            },
        },
        {
            element: '#performance-filter-section',
            popover: {
                title: 'Performance',
                description:
                    'Filter by the speed of the three public operations: ' +
                    '<strong>key pair generation</strong>, <strong>signing</strong>, and ' +
                    '<strong>signature verification</strong>.',
            },
        },
        {
            element: '#dataset-selector',
            popover: {
                title: 'Benchmark Dataset',
                description:
                    'Benchmarks were run on different hardware platforms. Switch between ' +
                    'datasets here to see how algorithm performance changes across machines.',
            },
        },
        {
            element: '#reset-button',
            popover: {
                title: 'Reset All Filters',
                description:
                    'Made a mess of the filters? Click <strong>Reset All</strong> to restore every ' +
                    'slider and checkbox to its default value and show all algorithms at once.',
            },
        },
        {
            element: '#content-overview',
            popover: {
                title: 'Algorithm Overview',
                description:
                    'Algorithms matching your filters are shown here as radar charts. Each chart has ' +
                    '<strong>six axes</strong>: <em>public key size</em>, <em>private key size</em>, ' +
                    '<em>signature size</em>, <em>key generation</em>, <em>signing</em>, and ' +
                    '<em>verification times</em>. <strong>The smaller the enclosed area, the better</strong>. ' +
                    'It means smaller keys and signatures, and faster operations.',
            },
        },
        {
            element: '#content-overview',
            popover: {
                title: 'Select Algorithms to Compare',
                description:
                    'You can <em>click</em> on any radar chart to change the selection ' +
                    '(up to 5 algorithms). For this tour, we have just selected five algorithms for you: ' +
                    '<strong>RSA (2048)</strong>, <strong>P-256</strong>, <strong>ML-DSA-44</strong>, ' +
                    '<strong>MAYO-1</strong>, and one variant of <strong>SLH-DSA</strong>.'
            },
        },
        {
            element: '#compare-button',
            popover: {
                title: 'Compare',
                description:
                    'Once you have selected one or multiple algorithms, click <strong>Compare</strong> to open ' +
                    'the detailed comparison view. The tour will continue there automatically.',
                side: 'bottom',
            },
        },
    ];

    var compareSteps = [
        {
            popover: {
                title: 'Detailed Comparison',
                description:
                    'Here you can analyse the selected algorithms side by side. The view has two ' +
                    'parts: a <strong>radar chart</strong> and a <strong>raw data table</strong>.',
            },
        },
        {
            element: '#compare-radar',
            popover: {
                title: 'Radar Chart',
                description:
                    'All selected algorithms are overlaid on one chart, each in a different colour. ' +
                    'You can highlight the area of one algorithm by moving your mouse on top of the ' +
                    'algorithm\'s name in the legend. A point closer to the center on any axis means ' +
                    'smaller keys and signatures, and faster operations. Therefore, a <strong>smaller ' +
                    'enclosed area is always better</strong>.',
            },
        },
        {
            element: '#compare-table',
            popover: {
                title: 'Data Table',
                description:
                    'The table lists exact values for every metric: <strong>NIST security level</strong>, ' +
                    '<strong>public key</strong>, <strong>private key</strong>, and ' +
                    '<strong>signature</strong> sizes in <em>bytes</em>, and ' +
                    '<strong>key generation</strong>, <strong>signing</strong>, and ' +
                    '<strong>verification</strong> times in <em>microseconds</em>. Use it for precise ' +
                    'numerical comparisons.',
            },
        },
        {
            element: '#compare-dataset-select-wrapper',
            popover: {
                title: 'Compare Across Datasets',
                description:
                    'Benchmarks were collected on several different hardware platforms. Use this ' +
                    'selector to pick a <strong>second dataset</strong> and see how the same ' +
                    'algorithms perform on a different machine. ' +
                    'Click <strong>Next</strong> to see what happens when a second dataset is selected.',
            },
        },
        {
            element: '#compare-radar-pair',
            popover: {
                title: 'Side-by-Side Radar Charts',
                description:
                    'With a second dataset selected, two radar charts are shown side by side: the ' +
                    '<strong>base</strong> platform on the left and the <strong>comparison</strong> ' +
                    'platform on the right.',
            },
        },
        {
            element: '#compare-table',
            popover: {
                title: 'Cross-Dataset Table',
                description:
                    'The table now pairs every timing metric: the <strong>base</strong> value on the ' +
                    'left and the <strong>comparison</strong> value on the right. For convenience, a ' +
                    'coloured percentage shows the relative difference: ' +
                    '<strong style="color:#51cf66">green</strong> indicates the comparison is faster' +
                    ', <strong style="color:#ff6b6b">red</strong> indicates it is slower.',
            },
        },
        {
            popover: {
                title: 'Tour Complete!',
                description:
                    '<strong>You are all set!</strong> Remember: <strong>1)</strong> use the ' +
                    'sidebar <em>filters</em> to narrow down candidates, <strong>2)</strong> ' +
                    '<em>select</em> up to five algorithms, and <strong>3)</strong> open the ' +
                    '<em>comparison</em> page for a detailed view. You can restart this tour ' +
                    'at any time using the <strong>?</strong> button in the top-right corner.',
            },
        },
    ];

    // -------------------------------------------------------------------------
    // Algorithm pre-selection for the tour
    // -------------------------------------------------------------------------

    // Click a button reliably: if the Dash id landed on a wrapper div rather
    // than the <button> itself, find the button inside it.
    function clickButton(selector) {
        var el = document.querySelector(selector);
        if (!el) return;
        var btn = el.tagName === 'BUTTON' ? el : el.querySelector('button');
        if (btn) btn.click();
    }

    // Reset filters, wait for a stable post-reset state (cards visible and
    // none selected for two consecutive polls ≈ 400 ms), then set the
    // pre-selected algorithms directly via set_props.
    function preselectTourAlgorithms() {
        clickButton('#reset-button');

        var elapsed = 0;
        var stableCount = 0;
        var timer = setInterval(function () {
            elapsed += 200;
            var cards = document.querySelectorAll('#content-overview .radar-card');
            var selected = document.querySelectorAll('#content-overview .radar-card--selected');
            var ready = cards.length > 0 && selected.length === 0;
            stableCount = ready ? stableCount + 1 : 0;

            if (stableCount >= 2 || elapsed >= 8000) {
                clearInterval(timer);
                window.dash_clientside.set_props('clicked-algs', {
                    data: {
                        'RSA-PSS-2048': true,
                        'P-256': true,
                        'ML-DSA-44': true,
                        'MAYO-1': true,
                        'SLH_DSA_PURE_SHA2_128F': true,
                    },
                });
                setTimeout(function () {
                    var main = document.querySelector('.mantine-AppShell-main');
                    if (main) main.scrollTop = 0;
                }, 600);
            }
        }, 200);
    }

    // -------------------------------------------------------------------------
    // Public API
    // -------------------------------------------------------------------------

    var TOTAL_STEPS = overviewSteps.length + compareSteps.length;

    window.pqcTour = {

        startOverview: function (force) {
            if (!force && localStorage.getItem(TOUR_SEEN_KEY)) return;
            if (!window.driver || !window.driver.js || !window.driver.js.driver) return;

            var driver = window.driver.js.driver;

            waitForElement('#content-overview', function () {
                var driverObj = driver({
                    showProgress: true,
                    progressText: '{{current}} / ' + TOTAL_STEPS,
                    allowClose: true,
                    nextBtnText: 'Next',
                    prevBtnText: 'Back',
                    doneBtnText: 'Go to Compare',
                    steps: overviewSteps,

                    // onNextClick overrides automatic step-advance; we must
                    // call moveNext() or destroy() manually.
                    onNextClick: function (element, step, options) {
                        // Trigger preselection as we leave the Overview step
                        // (index 7) and enter the Select Algorithms step (index 8).
                        if (options.state.activeIndex === 7) {
                            preselectTourAlgorithms();
                        }
                        if (!driverObj.hasNextStep()) {
                            // Done button on last step — complete the tour.
                            localStorage.setItem(TOUR_PHASE_KEY, '2');
                            localStorage.setItem(TOUR_SEEN_KEY, 'true');
                            driverObj.destroy();
                            var compareBtn = document.querySelector('#compare-button');
                            if (compareBtn) {
                                var link = compareBtn.closest('a');
                                if (link) link.click();
                            }
                        } else {
                            driverObj.moveNext();
                        }
                    },

                    // onDestroyStarted fires on X / Escape (NOT when we call
                    // driverObj.destroy() programmatically). We must call
                    // destroy() here to actually close the tour.
                    onDestroyStarted: function () {
                        localStorage.setItem(TOUR_SEEN_KEY, 'true');
                        if (localStorage.getItem(TOUR_PHASE_KEY) !== '2') {
                            localStorage.removeItem(TOUR_PHASE_KEY);
                        }
                        driverObj.destroy();
                    },
                });

                driverObj.drive();
            }, 8000);
        },

        startCompare: function () {
            if (localStorage.getItem(TOUR_PHASE_KEY) !== '2') return;
            if (!window.driver || !window.driver.js || !window.driver.js.driver) return;

            var driver = window.driver.js.driver;

            // Defined before waitForElement to avoid any hoisting ambiguity.
            var startDriver = function () {
                var offset = overviewSteps.length;
                var steps = compareSteps.map(function (step, i) {
                    return Object.assign({}, step, {
                        popover: Object.assign({}, step.popover, {
                            progressText: (offset + i + 1) + ' / ' + TOTAL_STEPS,
                        }),
                    });
                });

                var driverObj = driver({
                    showProgress: true,
                    allowClose: true,
                    nextBtnText: 'Next',
                    prevBtnText: 'Back',
                    doneBtnText: 'Done',
                    steps: steps,

                    onNextClick: function (element, step, options) {
                        var idx = options.state.activeIndex;
                        if (!driverObj.hasNextStep()) {
                            localStorage.removeItem(TOUR_PHASE_KEY);
                            driverObj.destroy();
                            window.dash_clientside.set_props('compare-dataset-selector', { value: null });
                            var overviewBtn = document.querySelector('#overview-button');
                            if (overviewBtn) {
                                var link = overviewBtn.closest('a');
                                if (link) link.click();
                            }
                            setTimeout(function () {
                                clickButton('#reset-button');
                            }, 600);
                        } else if (idx === 3) {
                            window.dash_clientside.set_props('compare-dataset-selector', {
                                value: 'dataset_v6_x86_64_c8a.large.zst',
                            });
                            waitForElement('#compare-radar-2', function () {
                                driverObj.moveNext();
                            }, 10000);
                        } else {
                            driverObj.moveNext();
                        }
                    },

                    onDestroyStarted: function () {
                        localStorage.removeItem(TOUR_PHASE_KEY);
                        window.dash_clientside.set_props('compare-dataset-selector', { value: null });
                        driverObj.destroy();
                    },
                });

                driverObj.drive();
            };

            waitForElement('#compare-radar', function () {
                if (document.querySelector('#compare-radar-2')) {
                    // A compare dataset was selected before arriving here.
                    // Use Dash's set_props API to update the selector value
                    // directly on the client, bypassing any server round-trip,
                    // then wait for update_comparison to re-render the
                    // single-radar layout before starting the driver.
                    window.dash_clientside.set_props(
                        'compare-dataset-selector',
                        { value: null }
                    );
                    var elapsed = 0;
                    var timer = setInterval(function () {
                        elapsed += 150;
                        var radar = document.querySelector('#compare-radar');
                        var radar2 = document.querySelector('#compare-radar-2');
                        if (radar && !radar2) {
                            clearInterval(timer);
                            startDriver();
                        } else if (elapsed >= 8000) {
                            clearInterval(timer);
                        }
                    }, 150);
                } else {
                    startDriver();
                }
            }, 10000);
        },

        restart: function () {
            localStorage.removeItem(TOUR_SEEN_KEY);
            localStorage.removeItem(TOUR_PHASE_KEY);
            var overviewBtn = document.querySelector('#overview-button');
            if (overviewBtn) {
                var link = overviewBtn.closest('a');
                if (link) link.click();
            }
            setTimeout(function () {
                window.pqcTour.startOverview(true);
            }, 400);
        },
    };
})();
