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
            popover: {
                title: 'Welcome to PQC Signatures',
                description:
                    'This webapp lets you explore and compare Post-Quantum Cryptography (PQC) digital ' +
                    'signature algorithms. This short tour explains how to use the website. ' +
                    '<strong>It will only take a minute!</strong>',
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
                    'five axes: public key size, private key size, signature size, signing time, and ' +
                    'verification time. <strong>The smaller the enclosed area, the better</strong>. ' +
                    'It means smaller keys and signatures, and faster operations.',
            },
        },
        {
            element: '#content-overview',
            popover: {
                title: 'Select Algorithms to Compare',
                description:
                    'We have clicked on five algorithms for you: <strong>RSA (2048)</strong>, ' +
                    '<strong>P-256</strong>, <strong>ML-DSA-44</strong>, <strong>MAYO-1</strong>, ' +
                    'and one variant of <strong>SLH-DSA</strong>. ' +
                    'You can tick the checkbox above any radar chart to change the selection ' +
                    '(up to 5 algorithms). Click Next when you are ready.',
            },
        },
        {
            element: '#compare-button',
            popover: {
                title: 'Compare',
                description:
                    'Once you have selected some algorithms, click <strong>Compare</strong> to open ' +
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
                    "algorithm's name in the legend. An algorithm with a <strong>smaller enclosed " +
                    'area</strong> uses smaller keys and signatures, and runs faster public ' +
                    'operations, so closer to the centre is always better.',
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

    // Reset filters, wait for a stable post-reset state (all checkboxes
    // visible and unchecked for two consecutive polls ≈ 400 ms), then fire
    // the hidden Dash button that triggers the Python preselect callback.
    function preselectTourAlgorithms() {
        clickButton('#reset-button');

        var elapsed = 0;
        var stableCount = 0;
        var timer = setInterval(function () {
            elapsed += 200;
            var inputs = document.querySelectorAll('#content-overview input[type="checkbox"]');
            var ready = inputs.length > 0 &&
                Array.from(inputs).every(function (inp) { return !inp.checked; });
            stableCount = ready ? stableCount + 1 : 0;

            if (stableCount >= 2 || elapsed >= 8000) {
                clearInterval(timer);
                clickButton('#tour-preselect-btn');
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

    window.pqcTour = {

        startOverview: function (force) {
            if (!force && localStorage.getItem(TOUR_SEEN_KEY)) return;
            if (!window.driver || !window.driver.js || !window.driver.js.driver) return;

            var driver = window.driver.js.driver;

            waitForElement('#content-overview', function () {
                var driverObj = driver({
                    showProgress: true,
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

            waitForElement('#compare-radar', function () {
                var driverObj = driver({
                    showProgress: true,
                    allowClose: true,
                    nextBtnText: 'Next',
                    prevBtnText: 'Back',
                    doneBtnText: 'Done',
                    steps: compareSteps,

                    onNextClick: function (element, step, options) {
                        if (!driverObj.hasNextStep()) {
                            localStorage.removeItem(TOUR_PHASE_KEY);
                            driverObj.destroy();
                            var overviewBtn = document.querySelector('#overview-button');
                            if (overviewBtn) {
                                var link = overviewBtn.closest('a');
                                if (link) link.click();
                            }
                            setTimeout(function () {
                                clickButton('#reset-button');
                            }, 600);
                        } else {
                            driverObj.moveNext();
                        }
                    },

                    onDestroyStarted: function () {
                        localStorage.removeItem(TOUR_PHASE_KEY);
                        driverObj.destroy();
                    },
                });

                driverObj.drive();
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
