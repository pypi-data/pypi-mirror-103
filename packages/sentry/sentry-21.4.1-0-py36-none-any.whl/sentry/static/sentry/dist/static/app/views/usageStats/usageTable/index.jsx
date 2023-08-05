import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ErrorPanel from 'app/components/charts/errorPanel';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import { SettingsIconLink } from 'app/components/organizations/headerItem';
import { Panel } from 'app/components/panels';
import PanelTable from 'app/components/panels/panelTable';
import TextOverflow from 'app/components/textOverflow';
import { IconSettings, IconWarning } from 'app/icons';
import space from 'app/styles/space';
import { DataCategory } from 'app/types';
import theme from 'app/utils/theme';
import { formatUsageWithUnits } from '../utils';
var UsageTable = /** @class */ (function (_super) {
    __extends(UsageTable, _super);
    function UsageTable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(UsageTable.prototype, "formatUsageOptions", {
        get: function () {
            var dataCategory = this.props.dataCategory;
            return {
                isAbbreviated: dataCategory !== DataCategory.ATTACHMENTS,
                useUnitScaling: dataCategory === DataCategory.ATTACHMENTS,
            };
        },
        enumerable: false,
        configurable: true
    });
    UsageTable.prototype.renderTableRow = function (stat) {
        var dataCategory = this.props.dataCategory;
        var project = stat.project, total = stat.total, accepted = stat.accepted, filtered = stat.filtered, dropped = stat.dropped;
        return [
            <CellProject key={0}>
        <TextOverflow>
          <StyledIdBadge project={project} avatarSize={16} hideOverflow displayName={<Link to={stat.projectLink}>{project.slug}</Link>}/>
        </TextOverflow>
        <SettingsIconLink to={stat.projectSettingsLink}>
          <IconSettings size={theme.iconSizes.sm}/>
        </SettingsIconLink>
      </CellProject>,
            <CellStat key={1}>
        {formatUsageWithUnits(total, dataCategory, this.formatUsageOptions)}
      </CellStat>,
            <CellStat key={2}>
        {formatUsageWithUnits(accepted, dataCategory, this.formatUsageOptions)}
      </CellStat>,
            <CellStat key={3}>
        {formatUsageWithUnits(filtered, dataCategory, this.formatUsageOptions)}
      </CellStat>,
            <CellStat key={4}>
        {formatUsageWithUnits(dropped, dataCategory, this.formatUsageOptions)}
      </CellStat>,
        ];
    };
    UsageTable.prototype.render = function () {
        var _this = this;
        var _a = this.props, isEmpty = _a.isEmpty, isLoading = _a.isLoading, isError = _a.isError, errors = _a.errors, headers = _a.headers, usageStats = _a.usageStats;
        if (isError) {
            return (<Panel>
          <ErrorPanel height="256px">
            <IconWarning color="gray300" size="lg"/>
            <ErrorMessages>
              {errors &&
                    Object.keys(errors).map(function (k) { var _a; return <span key={k}>{(_a = errors[k]) === null || _a === void 0 ? void 0 : _a.message}</span>; })}
            </ErrorMessages>
          </ErrorPanel>
        </Panel>);
        }
        return (<StyledPanelTable isLoading={isLoading} isEmpty={isEmpty} headers={headers}>
        {usageStats.map(function (s) { return _this.renderTableRow(s); })}
      </StyledPanelTable>);
    };
    return UsageTable;
}(React.Component));
export default UsageTable;
export var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: auto 100px 100px 100px 100px;\n"], ["\n  grid-template-columns: auto 100px 100px 100px 100px;\n"])));
export var CellStat = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-shrink: 1;\n  text-align: right;\n"], ["\n  flex-shrink: 1;\n  text-align: right;\n"])));
export var CellProject = styled(CellStat)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  text-align: left;\n"], ["\n  display: flex;\n  align-items: center;\n  text-align: left;\n"])));
export var CellSetting = styled(CellStat)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: 0;\n"])));
var StyledIdBadge = styled(IdBadge)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"], ["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"])));
var ErrorMessages = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n\n  margin-top: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n\n  margin-top: ", ";\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map