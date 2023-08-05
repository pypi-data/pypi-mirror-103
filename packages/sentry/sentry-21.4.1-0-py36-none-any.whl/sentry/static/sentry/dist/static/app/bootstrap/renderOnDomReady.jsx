export function renderOnDomReady(renderFn) {
    if (document.readyState !== 'loading') {
        renderFn();
    }
    else {
        document.addEventListener('DOMContentLoaded', renderFn);
    }
}
//# sourceMappingURL=renderOnDomReady.jsx.map