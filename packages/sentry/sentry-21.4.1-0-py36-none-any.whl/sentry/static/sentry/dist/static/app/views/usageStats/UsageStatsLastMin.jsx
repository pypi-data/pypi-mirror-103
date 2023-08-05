import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import NotAvailable from 'app/components/notAvailable';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { DataCategory } from 'app/types';
import { Outcome } from './types';
import { formatUsageWithUnits, getFormatUsageOptions } from './utils';
/**
 * Making 1 extra API call to display this number isn't very efficient.
 * The other approach would be to fetch the data in UsageStatsOrg with 1min
 * interval and roll it up on the frontend, but that (1) adds unnecessary
 * complexity as it's gnarly to fetch + rollup 90 days of 1min intervals,
 * (3) API resultset has a limit of 1000, so 90 days of 1min would not work.
 *
 * We're going with this approach for simplicity sake. By keeping the range
 * as small as possible, this call is quite fast.
 */
var UsageStatsLastMin = /** @class */ (function (_super) {
    __extends(UsageStatsLastMin, _super);
    function UsageStatsLastMin() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UsageStatsLastMin.prototype.getEndpoints = function () {
        return [['orgStats', this.endpointPath, { query: this.endpointQuery }]];
    };
    Object.defineProperty(UsageStatsLastMin.prototype, "endpointPath", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/stats_v2/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsLastMin.prototype, "endpointQuery", {
        get: function () {
            return {
                statsPeriod: '5m',
                interval: '1m',
                groupBy: ['category', 'outcome'],
                field: ['sum(quantity)'],
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsLastMin.prototype, "minuteData", {
        get: function () {
            var dataCategory = this.props.dataCategory;
            var _a = this.state, loading = _a.loading, error = _a.error, orgStats = _a.orgStats;
            if (loading || error || !orgStats || orgStats.intervals.length === 0) {
                return undefined;
            }
            var intervals = orgStats.intervals, groups = orgStats.groups;
            var eventsLastMin = 0;
            // The last minute in the series is still "in progress"
            // Read data from 2nd last element for the latest complete minute
            var lastMin = Math.max(intervals.length - 2, 0);
            groups.forEach(function (group) {
                var _a = group.by, outcome = _a.outcome, category = _a.category;
                // HACK: The backend enum are singular, but the frontend enums are plural
                if (!dataCategory.includes("" + category) || outcome !== Outcome.ACCEPTED) {
                    return;
                }
                eventsLastMin = group.series['sum(quantity)'][lastMin];
            });
            return formatUsageWithUnits(eventsLastMin, dataCategory, getFormatUsageOptions(dataCategory));
        },
        enumerable: false,
        configurable: true
    });
    UsageStatsLastMin.prototype.renderComponent = function () {
        var _a;
        var _b = this.props, dataCategory = _b.dataCategory, dataCategoryName = _b.dataCategoryName;
        return (<Wrapper>
        <Number>{(_a = this.minuteData) !== null && _a !== void 0 ? _a : <NotAvailable />}</Number>
        <Description>
          {tct('[preposition][dataCategoryName] accepted ', {
                preposition: dataCategory === DataCategory.ATTACHMENTS ? 'of ' : '',
                dataCategoryName: dataCategoryName.toLowerCase(),
            })}
          <br />
          {t('in the last minute')}
        </Description>
      </Wrapper>);
    };
    return UsageStatsLastMin;
}(AsyncComponent));
export default UsageStatsLastMin;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  width: 200px;\n  text-align: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n  width: 200px;\n  text-align: center;\n"])));
var Number = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: 32px;\n  margin-bottom: ", ";\n"], ["\n  font-size: 32px;\n  margin-bottom: ", ";\n"])), space(1));
var Description = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.4;\n"], ["\n  font-size: ", ";\n  line-height: 1.4;\n"])), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=UsageStatsLastMin.jsx.map