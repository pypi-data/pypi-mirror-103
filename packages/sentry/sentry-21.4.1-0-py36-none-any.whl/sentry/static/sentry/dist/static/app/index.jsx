import { __awaiter, __generator } from "tslib";
// These imports (core-js and regenerator-runtime) are replacements for deprecated `@babel/polyfill`
import 'core-js/stable';
import 'regenerator-runtime/runtime';
var BOOTSTRAP_URL = '/api/client-config/';
var bootApplication = function (data) {
    window.csrfCookieName = data.csrfCookieName;
    // Once data hydration is done we can initialize the app
    var initializeMain = require('./bootstrap/initializeMain').initializeMain;
    initializeMain(data);
};
function bootWithHydration() {
    return __awaiter(this, void 0, void 0, function () {
        var response, data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(BOOTSTRAP_URL)];
                case 1:
                    response = _a.sent();
                    return [4 /*yield*/, response.json()];
                case 2:
                    data = _a.sent();
                    window.__initialData = data;
                    bootApplication(data);
                    return [2 /*return*/];
            }
        });
    });
}
var bootstrapData = window.__initialData;
// If __initialData is not already set on the window, we are likely running in
// pure SPA mode, meaning django is not serving our frontend application and we
// need to make an API request to hydrate the bootstrap data to boot the app.
if (bootstrapData === undefined) {
    bootWithHydration();
}
else {
    bootApplication(bootstrapData);
}
//# sourceMappingURL=index.jsx.map