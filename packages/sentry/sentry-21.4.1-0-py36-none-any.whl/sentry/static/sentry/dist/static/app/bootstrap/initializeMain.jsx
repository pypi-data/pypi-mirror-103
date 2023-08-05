import 'bootstrap/js/alert';
import 'bootstrap/js/tab';
import 'bootstrap/js/dropdown';
import './exportGlobals';
import routes from 'app/routes';
import { metric } from 'app/utils/analytics';
import { commonInitialization } from './commonInitialization';
import { initializeSdk } from './initializeSdk';
import { renderMain } from './renderMain';
import { renderOnDomReady } from './renderOnDomReady';
export function initializeMain(config) {
    commonInitialization(config);
    initializeSdk(config, { routes: routes });
    // Used for operational metrics to determine that the application js
    // bundle was loaded by browser.
    metric.mark({ name: 'sentry-app-init' });
    renderOnDomReady(renderMain);
}
//# sourceMappingURL=initializeMain.jsx.map