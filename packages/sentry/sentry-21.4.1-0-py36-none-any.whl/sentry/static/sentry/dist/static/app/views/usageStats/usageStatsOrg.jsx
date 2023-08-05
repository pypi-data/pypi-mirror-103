import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import moment from 'moment';
import AsyncComponent from 'app/components/asyncComponent';
import Card from 'app/components/card';
import OptionSelector from 'app/components/charts/optionSelector';
import { ChartControls, HeaderTitle, InlineContainer } from 'app/components/charts/styles';
import { getInterval } from 'app/components/charts/utils';
import NotAvailable from 'app/components/notAvailable';
import QuestionTooltip from 'app/components/questionTooltip';
import TextOverflow from 'app/components/textOverflow';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { FORMAT_DATETIME_DAILY, FORMAT_DATETIME_HOURLY, getDateFromMoment, } from './usageChart/utils';
import { Outcome } from './types';
import UsageChart, { CHART_OPTIONS_DATA_TRANSFORM, ChartDataTransform, } from './usageChart';
import { formatUsageWithUnits, getFormatUsageOptions } from './utils';
var UsageStatsOrganization = /** @class */ (function (_super) {
    __extends(UsageStatsOrganization, _super);
    function UsageStatsOrganization() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderChartFooter = function () {
            var handleChangeState = _this.props.handleChangeState;
            var _a = _this.chartData, chartTransform = _a.chartTransform, chartDateStartDisplay = _a.chartDateStartDisplay, chartDateEndDisplay = _a.chartDateEndDisplay;
            return (<ChartControls>
        <InlineContainer>
          {tct('Usage for [start] — [end]', {
                    start: chartDateStartDisplay,
                    end: chartDateEndDisplay,
                })}
        </InlineContainer>
        <InlineContainer>
          <OptionSelector title={t('Type')} selected={chartTransform} options={CHART_OPTIONS_DATA_TRANSFORM} onChange={function (val) {
                    return handleChangeState({ chartTransform: val });
                }}/>
        </InlineContainer>
      </ChartControls>);
        };
        return _this;
    }
    UsageStatsOrganization.prototype.componentDidUpdate = function (prevProps) {
        var prevDateTime = prevProps.dataDatetime;
        var currDateTime = this.props.dataDatetime;
        if (prevDateTime.start !== currDateTime.start ||
            prevDateTime.end !== currDateTime.end ||
            prevDateTime.period !== currDateTime.period) {
            this.reloadData();
        }
    };
    UsageStatsOrganization.prototype.getEndpoints = function () {
        return [['orgStats', this.endpointPath, { query: this.endpointQuery }]];
    };
    Object.defineProperty(UsageStatsOrganization.prototype, "endpointPath", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/stats_v2/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsOrganization.prototype, "endpointQuery", {
        get: function () {
            var dataDatetime = this.props.dataDatetime;
            // TODO: Enable user to use dateStart/dateEnd
            return {
                statsPeriod: (dataDatetime === null || dataDatetime === void 0 ? void 0 : dataDatetime.period) || DEFAULT_STATS_PERIOD,
                interval: getInterval(dataDatetime),
                groupBy: ['category', 'outcome'],
                field: ['sum(quantity)'],
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsOrganization.prototype, "chartData", {
        get: function () {
            var orgStats = this.state.orgStats;
            return __assign(__assign(__assign({}, this.mapSeriesToChart(orgStats)), this.chartDateRange), this.chartTransform);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsOrganization.prototype, "chartTransform", {
        get: function () {
            var chartTransform = this.props.chartTransform;
            switch (chartTransform) {
                case ChartDataTransform.CUMULATIVE:
                case ChartDataTransform.PERIODIC:
                    return { chartTransform: chartTransform };
                default:
                    return { chartTransform: ChartDataTransform.PERIODIC };
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsOrganization.prototype, "chartDateRange", {
        get: function () {
            var orgStats = this.state.orgStats;
            // Use fillers as loading/error states will not display datetime at all
            if (!orgStats || !orgStats.intervals || orgStats.intervals.length < 2) {
                var now = moment();
                return {
                    chartDateInterval: '1d',
                    chartDateStart: now.format(),
                    chartDateEnd: now.format(),
                    chartDateStartDisplay: now.local().format(FORMAT_DATETIME_DAILY),
                    chartDateEndDisplay: now.local().format(FORMAT_DATETIME_DAILY),
                };
            }
            var intervals = orgStats.intervals;
            var startTime = moment(intervals[0]);
            var endTime = moment(intervals[intervals.length - 1]);
            var intervalMinutes = moment(endTime).diff(startTime, 'm') / (intervals.length - 1);
            // If interval is a day or more, use UTC to format date. Otherwise, the date
            // may shift ahead/behind when converting to the user's local time.
            var isPerDay = intervalMinutes >= 24 * 60;
            var FORMAT_DATETIME = isPerDay ? FORMAT_DATETIME_DAILY : FORMAT_DATETIME_HOURLY;
            var xAxisStart = moment(startTime);
            var xAxisEnd = moment(endTime);
            var displayStart = isPerDay ? moment(startTime).utc() : moment(startTime).local();
            var displayEnd = isPerDay
                ? moment(endTime).utc()
                : moment(endTime).local().add(intervalMinutes, 'm');
            return {
                chartDateInterval: intervalMinutes + "m",
                chartDateStart: xAxisStart.format(),
                chartDateEnd: xAxisEnd.format(),
                chartDateStartDisplay: displayStart.format(FORMAT_DATETIME),
                chartDateEndDisplay: displayEnd.format(FORMAT_DATETIME),
            };
        },
        enumerable: false,
        configurable: true
    });
    UsageStatsOrganization.prototype.mapSeriesToChart = function (orgStats) {
        var _this = this;
        var cardStats = {
            total: undefined,
            accepted: undefined,
            dropped: undefined,
            filtered: undefined,
        };
        var chartStats = {
            accepted: [],
            dropped: [],
            projected: [],
        };
        if (!orgStats) {
            return { cardStats: cardStats, chartStats: chartStats };
        }
        try {
            var dataCategory_1 = this.props.dataCategory;
            var chartDateInterval_1 = this.chartDateRange.chartDateInterval;
            var usageStats_1 = orgStats.intervals.map(function (interval) {
                var dateTime = moment(interval);
                return {
                    date: getDateFromMoment(dateTime, chartDateInterval_1),
                    total: 0,
                    accepted: 0,
                    filtered: 0,
                    dropped: { total: 0 },
                };
            });
            // Tally totals for card data
            var count_1 = {
                total: 0,
                accepted: 0,
                dropped: 0,
                invalid: 0,
                filtered: 0,
            };
            orgStats.groups.forEach(function (group) {
                var _a = group.by, outcome = _a.outcome, category = _a.category;
                // HACK: The backend enum are singular, but the frontend enums are plural
                if (!dataCategory_1.includes("" + category)) {
                    return;
                }
                count_1.total += group.totals['sum(quantity)'];
                count_1[outcome] += group.totals['sum(quantity)'];
                group.series['sum(quantity)'].forEach(function (stat, i) {
                    if (outcome === Outcome.DROPPED || outcome === Outcome.INVALID) {
                        usageStats_1[i].dropped.total += stat;
                    }
                    usageStats_1[i][outcome] += stat;
                });
            });
            // Invalid data is dropped
            count_1.dropped += count_1.invalid;
            delete count_1.invalid;
            usageStats_1.forEach(function (stat) {
                stat.total = stat.accepted + stat.filtered + stat.dropped.total;
                // Chart Data
                chartStats.accepted.push({ value: [stat.date, stat.accepted] });
                chartStats.dropped.push({ value: [stat.date, stat.dropped.total] });
            });
            return {
                cardStats: {
                    total: formatUsageWithUnits(count_1.total, dataCategory_1, getFormatUsageOptions(dataCategory_1)),
                    accepted: formatUsageWithUnits(count_1.accepted, dataCategory_1, getFormatUsageOptions(dataCategory_1)),
                    dropped: formatUsageWithUnits(count_1.dropped, dataCategory_1, getFormatUsageOptions(dataCategory_1)),
                    filtered: formatUsageWithUnits(count_1.filtered, dataCategory_1, getFormatUsageOptions(dataCategory_1)),
                },
                chartStats: chartStats,
            };
        }
        catch (err) {
            Sentry.withScope(function (scope) {
                scope.setContext('query', _this.endpointQuery);
                scope.setContext('body', orgStats);
                Sentry.captureException(err);
            });
            return {
                cardStats: cardStats,
                chartStats: chartStats,
                dataError: new Error('Failed to parse stats data'),
            };
        }
    };
    UsageStatsOrganization.prototype.renderCards = function () {
        var _a = this.props, dataCategory = _a.dataCategory, dataCategoryName = _a.dataCategoryName;
        var _b = this.chartData.cardStats, total = _b.total, accepted = _b.accepted, dropped = _b.dropped, filtered = _b.filtered;
        var cardMetadata = [
            {
                title: tct('Total [dataCategory]', { dataCategory: dataCategoryName }),
                value: total,
            },
            {
                title: t('Accepted'),
                description: tct('Accepted [dataCategory] were successfully processed by Sentry.', { dataCategory: dataCategory }),
                value: accepted,
            },
            {
                title: t('Filtered'),
                description: tct('Filtered [dataCategory] were blocked due to your inbound data filter rules', { dataCategory: dataCategory }),
                value: filtered,
            },
            {
                title: t('Dropped'),
                description: tct('Dropped [dataCategory] were discarded due to invalid data, rate-limits, quota limits, or spike protection', { dataCategory: dataCategory }),
                value: dropped,
            },
        ];
        return (<CardWrapper>
        {cardMetadata.map(function (c, i) {
                var _a;
                return (<StyledCard key={i}>
            <HeaderTitle>
              <TextOverflow>{c.title}</TextOverflow>
              {c.description && (<QuestionTooltip size="sm" position="top" title={c.description}/>)}
            </HeaderTitle>
            <CardContent>
              <TextOverflow>{(_a = c.value) !== null && _a !== void 0 ? _a : <NotAvailable />}</TextOverflow>
            </CardContent>
          </StyledCard>);
            })}
      </CardWrapper>);
    };
    UsageStatsOrganization.prototype.renderChart = function () {
        var dataCategory = this.props.dataCategory;
        var _a = this.state, error = _a.error, errors = _a.errors, loading = _a.loading;
        var _b = this.chartData, chartStats = _b.chartStats, dataError = _b.dataError, chartDateInterval = _b.chartDateInterval, chartDateStart = _b.chartDateStart, chartDateEnd = _b.chartDateEnd, chartTransform = _b.chartTransform;
        var hasError = error || !!dataError;
        var chartErrors = dataError ? __assign(__assign({}, errors), { data: dataError }) : errors; // TODO(ts): AsyncComponent
        return (<UsageChart isLoading={loading} isError={hasError} errors={chartErrors} title=" " // Force the title to be blank
         footer={this.renderChartFooter()} dataCategory={dataCategory} dataTransform={chartTransform} usageDateStart={chartDateStart} usageDateEnd={chartDateEnd} usageDateInterval={chartDateInterval} usageStats={chartStats}/>);
    };
    UsageStatsOrganization.prototype.renderComponent = function () {
        return (<React.Fragment>
        {this.renderCards()}
        {this.renderChart()}
      </React.Fragment>);
    };
    return UsageStatsOrganization;
}(AsyncComponent));
export default UsageStatsOrganization;
var CardWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: 1fr;\n  grid-auto-rows: 1fr;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: 1fr;\n  grid-auto-rows: 1fr;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-auto-flow: row;\n  }\n"])), space(2), space(3), function (p) { return p.theme.breakpoints[0]; });
var StyledCard = styled(Card)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  align-items: flex-start;\n  min-height: 95px;\n  padding: ", " ", ";\n  color: ", ";\n"], ["\n  align-items: flex-start;\n  min-height: 95px;\n  padding: ", " ", ";\n  color: ", ";\n"])), space(2), space(3), function (p) { return p.theme.textColor; });
var CardContent = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: ", ";\n  font-size: 32px;\n"], ["\n  margin-top: ", ";\n  font-size: 32px;\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=usageStatsOrg.jsx.map