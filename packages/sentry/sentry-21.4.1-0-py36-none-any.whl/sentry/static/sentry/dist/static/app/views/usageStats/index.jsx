import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import pick from 'lodash/pick';
import { SectionHeading } from 'app/components/charts/styles';
import { getInterval } from 'app/components/charts/utils';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import ErrorBoundary from 'app/components/errorBoundary';
import PageHeading from 'app/components/pageHeading';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { DEFAULT_RELATIVE_PERIODS, DEFAULT_STATS_PERIOD } from 'app/constants';
import { t, tct } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { DataCategory, DataCategoryName, } from 'app/types';
import { parsePeriodToHours } from 'app/utils/dates';
import { CHART_OPTIONS_DATACATEGORY } from './usageChart';
import UsageStatsLastMin from './UsageStatsLastMin';
import UsageStatsOrg from './usageStatsOrg';
import UsageStatsProjects from './usageStatsProjects';
var PAGE_QUERY_PARAMS = [
    'pageStart',
    'pageEnd',
    'pagePeriod',
    'pageUtc',
    'dataCategory',
    'chartTransform',
    'sort',
];
var OrganizationStats = /** @class */ (function (_super) {
    __extends(OrganizationStats, _super);
    function OrganizationStats() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getNextLocations = function (project) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var nextLocation = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { project: project.id }) });
            // Do not leak out page-specific keys
            nextLocation.query = omit(nextLocation.query, PAGE_QUERY_PARAMS);
            return {
                performance: __assign(__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/performance/" }),
                projectDetail: __assign(__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/projects/" + project.slug + "/" }),
                issueList: __assign(__assign({}, nextLocation), { pathname: "/organizations/" + organization.slug + "/issues/" }),
                settings: {
                    pathname: "/settings/" + organization.slug + "/projects/" + project.slug + "/",
                },
            };
        };
        /**
         * TODO: Enable user to set dateStart/dateEnd
         *
         * See PAGE_QUERY_PARAMS for list of accepted keys on nextState
         */
        _this.setStateOnUrl = function (nextState, options) {
            if (options === void 0) { options = {
                willUpdateRouter: true,
            }; }
            var _a = _this.props, location = _a.location, router = _a.router;
            var nextQueryParams = pick(nextState, PAGE_QUERY_PARAMS);
            var nextLocation = __assign(__assign({}, location), { query: __assign(__assign({}, location === null || location === void 0 ? void 0 : location.query), nextQueryParams) });
            if (options.willUpdateRouter) {
                router.push(nextLocation);
            }
            return nextLocation;
        };
        return _this;
    }
    Object.defineProperty(OrganizationStats.prototype, "dataCategory", {
        get: function () {
            var _a, _b;
            var dataCategory = (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.dataCategory;
            switch (dataCategory) {
                case DataCategory.ERRORS:
                case DataCategory.TRANSACTIONS:
                case DataCategory.ATTACHMENTS:
                    return dataCategory;
                default:
                    return DataCategory.ERRORS;
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "dataCategoryName", {
        get: function () {
            var _a;
            var dataCategory = this.dataCategory;
            return (_a = DataCategoryName[dataCategory]) !== null && _a !== void 0 ? _a : t('Unknown Data Category');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "dataPeriod", {
        get: function () {
            var _a, _b;
            var _c = (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) !== null && _b !== void 0 ? _b : {}, pagePeriod = _c.pagePeriod, pageStart = _c.pageStart, pageEnd = _c.pageEnd;
            if (!pagePeriod && !pageStart && !pageEnd) {
                return { period: DEFAULT_STATS_PERIOD };
            }
            // Absolute date range is more specific than period
            if (pageStart && pageEnd) {
                return { start: pageStart, end: pageEnd };
            }
            var keys = Object.keys(DEFAULT_RELATIVE_PERIODS);
            return pagePeriod && keys.includes(pagePeriod)
                ? { period: pagePeriod }
                : { period: DEFAULT_STATS_PERIOD };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "chartTransform", {
        // Validation and type-casting should be handled by chart
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.chartTransform;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OrganizationStats.prototype, "tableSort", {
        // Validation and type-casting should be handled by table
        get: function () {
            var _a, _b;
            return (_b = (_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.sort;
        },
        enumerable: false,
        configurable: true
    });
    OrganizationStats.prototype.renderPageControl = function () {
        var _this = this;
        var organization = this.props.organization;
        // Might deviate from server-side but this is cosmetic at the moment
        var interval = getInterval(this.dataPeriod);
        var period = this.dataPeriod.period;
        // Remove options for relative periods shorter than 1 week
        var relativePeriods = Object.keys(DEFAULT_RELATIVE_PERIODS).reduce(function (acc, key) {
            var periodDays = parsePeriodToHours(key) / 24;
            if (periodDays >= 7) {
                acc[key] = DEFAULT_RELATIVE_PERIODS[key];
            }
            return acc;
        }, {});
        return (<Header>
        <HeaderItemRow>
          <HeaderItemRow>
            <ItemPagePeriod>
              <SectionHeading>{t('Display')}</SectionHeading>
              <DropdownControl label={<DropdownLabel>
                    {DEFAULT_RELATIVE_PERIODS[period || DEFAULT_STATS_PERIOD]}
                  </DropdownLabel>}>
                {Object.keys(relativePeriods).map(function (key) { return (<DropdownItem key={key} eventKey={key} onSelect={function (val) {
                    return _this.setStateOnUrl({ pagePeriod: val });
                }}>
                    {DEFAULT_RELATIVE_PERIODS[key]}
                  </DropdownItem>); })}
              </DropdownControl>
            </ItemPagePeriod>

            <ItemDataCategory>
              <SectionHeadingInRow>{t('of')}</SectionHeadingInRow>
              <DropdownControl label={<DropdownLabel>{this.dataCategoryName}</DropdownLabel>}>
                {CHART_OPTIONS_DATACATEGORY.map(function (option) { return (<DropdownItem key={option.value} eventKey={option.value} onSelect={function (val) {
                    return _this.setStateOnUrl({ dataCategory: val });
                }}>
                    {option.label}
                  </DropdownItem>); })}
              </DropdownControl>
            </ItemDataCategory>
          </HeaderItemRow>
          <HeaderItemColumn>
            <SectionHeading>{t('Interval')}</SectionHeading>
            <HeaderItemValue>
              <span>{interval}</span>
            </HeaderItemValue>
          </HeaderItemColumn>
        </HeaderItemRow>

        <ErrorBoundary mini>
          <UsageStatsLastMin organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName}/>
        </ErrorBoundary>
      </Header>);
    };
    OrganizationStats.prototype.render = function () {
        var organization = this.props.organization;
        return (<SentryDocumentTitle title="Usage Stats">
        <PageContent>
          <PageHeader>
            <PageHeading>{t('Organization Usage Stats')}</PageHeading>
          </PageHeader>

          {this.renderPageControl()}

          <p>
            {t('The chart below reflects events that Sentry has received across your entire organization. We collect usage metrics on three types of events: errors, transactions, and attachments. Sessions are not included in this chart.')}
          </p>

          <ErrorBoundary mini>
            <UsageStatsOrg organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName} dataDatetime={this.dataPeriod} chartTransform={this.chartTransform} handleChangeState={this.setStateOnUrl}/>
          </ErrorBoundary>

          <PageHeader>
            <PageHeading>
              {tct('Project Usage Stats for [dataCategory]', {
                dataCategory: this.dataCategoryName,
            })}
            </PageHeading>
          </PageHeader>

          <p>{t('Only usage stats for your projects are displayed here.')}</p>

          <ErrorBoundary mini>
            <UsageStatsProjects organization={organization} dataCategory={this.dataCategory} dataCategoryName={this.dataCategoryName} dataDatetime={this.dataPeriod} tableSort={this.tableSort} handleChangeState={this.setStateOnUrl} getNextLocations={this.getNextLocations}/>
          </ErrorBoundary>
        </PageContent>
      </SentryDocumentTitle>);
    };
    return OrganizationStats;
}(React.Component));
export default OrganizationStats;
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: flex-end;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: flex-end;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(3));
var HeaderItem = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  margin-right: ", ";\n"])), space(3));
var HeaderItemRow = styled(HeaderItem)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-direction: row;\n  align-items: flex-end;\n  justify-content: flex-start;\n"], ["\n  flex-direction: row;\n  align-items: flex-end;\n  justify-content: flex-start;\n"])));
var HeaderItemColumn = styled(HeaderItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: flex-start;\n"], ["\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: flex-start;\n"])));
var HeaderItemValue = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  min-height: 40px;\n\n  > span {\n    font-weight: 600;\n    font-size: ", ";\n    color: ", "; /* Make it same as dropdown */\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  min-height: 40px;\n\n  > span {\n    font-weight: 600;\n    font-size: ", ";\n    color: ", "; /* Make it same as dropdown */\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.gray500; });
var ItemPagePeriod = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  margin-right: ", ";\n"])), space(2));
var ItemDataCategory = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  margin-right: ", ";\n"])), space(2));
var SectionHeadingInRow = styled(SectionHeading)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(2));
var DropdownLabel = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  min-width: 100px;\n  text-align: left;\n"], ["\n  min-width: 100px;\n  text-align: left;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=index.jsx.map