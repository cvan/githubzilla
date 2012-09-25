var x = {};
x.capabilities = {
    'JSON': window.JSON && typeof JSON.parse == 'function',
    'console': window.console && (typeof window.console.log == 'function'),
    'replaceState': typeof history.replaceState === 'function',
    'chromeless': window.locationbar && !window.locationbar.visible,
    'localStorage': false,
    'sessionStorage': false,
    'webApps': !!(navigator.mozApps && navigator.mozApps.install),
    'fileAPI': !!window.FileReader,
    'touch': ('ontouchstart' in window) || window.DocumentTouch && document instanceof DocumentTouch,
    'nativeScroll': (function() {
        return 'WebkitOverflowScrolling' in document.createElement('div').style;
    })(),
    'performance': !!(window.performance || window.msPerformance || window.webkitPerformance || window.mozPerformance)
};

try {
    if ('localStorage' in window && window['localStorage'] !== null) {
        x.capabilities.localStorage = true;
    }
} catch (e) {
}

try {
    if ('sessionStorage' in window && window['sessionStorage'] !== null) {
        x.capabilities.sessionStorage = true;
    }
} catch (e) {
}
