import { __extends, __rest } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import withOrganization from 'app/utils/withOrganization';
import Detail from './detail';
var DashboardsV2Container = /** @class */ (function (_super) {
    __extends(DashboardsV2Container, _super);
    function DashboardsV2Container() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DashboardsV2Container.prototype.render = function () {
        var _a = this.props, organization = _a.organization, props = __rest(_a, ["organization"]);
        return (<Feature features={['dashboards-basic']} organization={organization}>
        <Detail {...props} organization={organization}/>
      </Feature>);
    };
    return DashboardsV2Container;
}(React.Component));
export default withOrganization(DashboardsV2Container);
//# sourceMappingURL=index.jsx.map