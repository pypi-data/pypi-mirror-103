import { __awaiter, __generator } from "tslib";
import React from 'react';
import ReactDOM from 'react-dom';
import * as Router from 'react-router';
import * as Sentry from '@sentry/react';
import createReactClass from 'create-react-class';
import jQuery from 'jquery';
import moment from 'moment';
import PropTypes from 'prop-types';
import Reflux from 'reflux';
import plugins from 'app/plugins';
// The password strength component is very heavyweight as it includes the
// zxcvbn, a relatively byte-heavy password strength estimation library. Load
// it on demand.
function loadPasswordStrength(callback) {
    return __awaiter(this, void 0, void 0, function () {
        var module_1, err_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, import(
                        /* webpackChunkName: "passwordStrength" */ 'app/components/passwordStrength')];
                case 1:
                    module_1 = _a.sent();
                    callback(module_1);
                    return [3 /*break*/, 3];
                case 2:
                    err_1 = _a.sent();
                    return [3 /*break*/, 3];
                case 3: return [2 /*return*/];
            }
        });
    });
}
var globals = {
    // The following globals are used in sentry-plugins webpack externals
    // configuration.
    PropTypes: PropTypes,
    React: React,
    Reflux: Reflux,
    Router: Router,
    Sentry: Sentry,
    moment: moment,
    ReactDOM: {
        findDOMNode: ReactDOM.findDOMNode,
        render: ReactDOM.render,
    },
    // jQuery is still exported to the window as some bootsrap functionality
    // and legacy plugins like youtrack make use of it.
    $: jQuery,
    jQuery: jQuery,
    // django templates make use of these globals
    createReactClass: createReactClass,
    SentryApp: {},
};
// The SentryApp global contains exported app modules for use in javascript
// modules that are not compiled with the sentry bundle.
globals.SentryApp = {
    // The following components are used in sentry-plugins.
    Form: require('app/components/forms/form').default,
    FormState: require('app/components/forms/index').FormState,
    LoadingIndicator: require('app/components/loadingIndicator').default,
    plugins: {
        add: plugins.add,
        addContext: plugins.addContext,
        BasePlugin: plugins.BasePlugin,
        DefaultIssuePlugin: plugins.DefaultIssuePlugin,
    },
    // The following components are used in legacy django HTML views
    passwordStrength: { load: loadPasswordStrength },
    U2fSign: require('app/components/u2f/u2fsign').default,
    ConfigStore: require('app/stores/configStore').default,
    SystemAlerts: require('app/views/app/systemAlerts').default,
    Indicators: require('app/components/indicators').default,
    SetupWizard: require('app/components/setupWizard').default,
    HookStore: require('app/stores/hookStore').default,
    Modal: require('app/actionCreators/modal'),
};
// Make globals available on the window object
Object.keys(globals).forEach(function (name) { return (window[name] = globals[name]); });
//# sourceMappingURL=exportGlobals.jsx.map