import { __extends } from "tslib";
import React from 'react';
import { ThemeProvider } from 'emotion-theming';
import AlertStore from 'app/stores/alertStore';
import { lightTheme } from 'app/utils/theme';
import AlertMessage from './alertMessage';
var Alerts = /** @class */ (function (_super) {
    __extends(Alerts, _super);
    function Alerts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.unlistener = AlertStore.listen(function (alerts) { return _this.setState({ alerts: alerts }); }, undefined);
        return _this;
    }
    Alerts.prototype.getInitialState = function () {
        return {
            alerts: AlertStore.getInitialState(),
        };
    };
    Alerts.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    Alerts.prototype.render = function () {
        var className = this.props.className;
        var alerts = this.state.alerts;
        return (<ThemeProvider theme={lightTheme}>
        <div className={className}>
          {alerts.map(function (alert, index) { return (<AlertMessage alert={alert} key={alert.id + "-" + index} system/>); })}
        </div>
      </ThemeProvider>);
    };
    return Alerts;
}(React.Component));
export default Alerts;
//# sourceMappingURL=systemAlerts.jsx.map