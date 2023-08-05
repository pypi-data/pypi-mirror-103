import { __assign, __extends } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import AsyncComponent from 'app/components/asyncComponent';
import SortLink from 'app/components/gridEditable/sortLink';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { t } from 'app/locale';
import { DataCategory } from 'app/types';
import withProjects from 'app/utils/withProjects';
import UsageTable, { CellProject, CellStat } from './usageTable';
export var SortBy;
(function (SortBy) {
    SortBy["PROJECT"] = "project";
    SortBy["TOTAL"] = "total";
    SortBy["ACCEPTED"] = "accepted";
    SortBy["FILTERED"] = "filtered";
    SortBy["DROPPED"] = "dropped";
    SortBy["INVALID"] = "invalid";
})(SortBy || (SortBy = {}));
var UsageStatsProjects = /** @class */ (function (_super) {
    __extends(UsageStatsProjects, _super);
    function UsageStatsProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeSort = function (nextKey) {
            var handleChangeState = _this.props.handleChangeState;
            var _a = _this.tableSort, key = _a.key, direction = _a.direction;
            var nextDirection = 1; // Default to descending
            if (key === nextKey) {
                nextDirection = direction * -1; // Toggle if clicking on the same column
            }
            else if (nextKey === SortBy.PROJECT) {
                nextDirection = -1; // Default PROJECT to ascending
            }
            return handleChangeState({ sort: "" + (nextDirection > 0 ? '-' : '') + nextKey }, { willUpdateRouter: false });
        };
        return _this;
    }
    UsageStatsProjects.prototype.componentDidUpdate = function (prevProps) {
        var prevDateTime = prevProps.dataDatetime;
        var currDateTime = this.props.dataDatetime;
        if (prevDateTime.start !== currDateTime.start ||
            prevDateTime.end !== currDateTime.end ||
            prevDateTime.period !== currDateTime.period) {
            this.reloadData();
        }
    };
    UsageStatsProjects.prototype.getEndpoints = function () {
        return [['projectStats', this.endpointPath, { query: this.endpointQuery }]];
    };
    Object.defineProperty(UsageStatsProjects.prototype, "endpointPath", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/stats_v2/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "endpointQuery", {
        get: function () {
            var dataDatetime = this.props.dataDatetime;
            // We do not need more granularity in the data so interval is '1d'
            return {
                statsPeriod: (dataDatetime === null || dataDatetime === void 0 ? void 0 : dataDatetime.period) || DEFAULT_STATS_PERIOD,
                interval: '1d',
                groupBy: ['category', 'outcome', 'project'],
                field: ['sum(quantity)'],
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "tableData", {
        get: function () {
            var projectStats = this.state.projectStats;
            return __assign({ headers: this.tableHeader }, this.mapSeriesToTable(projectStats));
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "tableSort", {
        get: function () {
            var tableSort = this.props.tableSort;
            if (!tableSort) {
                return {
                    key: SortBy.TOTAL,
                    direction: 1,
                };
            }
            var key = tableSort;
            var direction = -1;
            if (tableSort.charAt(0) === '-') {
                key = key.slice(1);
                direction = 1;
            }
            switch (key) {
                case SortBy.PROJECT:
                case SortBy.TOTAL:
                case SortBy.ACCEPTED:
                case SortBy.FILTERED:
                case SortBy.DROPPED:
                    return { key: key, direction: direction };
                default:
                    return { key: SortBy.ACCEPTED, direction: -1 };
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageStatsProjects.prototype, "tableHeader", {
        get: function () {
            var _this = this;
            var _a = this.tableSort, key = _a.key, direction = _a.direction;
            var getArrowDirection = function (linkKey) {
                if (linkKey !== key) {
                    return undefined;
                }
                return direction > 0 ? 'desc' : 'asc';
            };
            return [
                {
                    key: SortBy.PROJECT,
                    title: t('Project'),
                    align: 'left',
                    direction: getArrowDirection(SortBy.PROJECT),
                    onClick: function () { return _this.handleChangeSort(SortBy.PROJECT); },
                },
                {
                    key: SortBy.TOTAL,
                    title: t('Total'),
                    align: 'right',
                    direction: getArrowDirection(SortBy.TOTAL),
                    onClick: function () { return _this.handleChangeSort(SortBy.TOTAL); },
                },
                {
                    key: SortBy.ACCEPTED,
                    title: t('Accepted'),
                    align: 'right',
                    direction: getArrowDirection(SortBy.ACCEPTED),
                    onClick: function () { return _this.handleChangeSort(SortBy.ACCEPTED); },
                },
                {
                    key: SortBy.FILTERED,
                    title: t('Filtered'),
                    align: 'right',
                    direction: getArrowDirection(SortBy.FILTERED),
                    onClick: function () { return _this.handleChangeSort(SortBy.FILTERED); },
                },
                {
                    key: SortBy.DROPPED,
                    title: t('Dropped'),
                    align: 'right',
                    direction: getArrowDirection(SortBy.DROPPED),
                    onClick: function () { return _this.handleChangeSort(SortBy.DROPPED); },
                },
            ].map(function (h) {
                var Cell = h.key === SortBy.PROJECT ? CellProject : CellStat;
                return (<Cell key={h.key}>
          <SortLink canSort title={h.title} align={h.align} direction={h.direction} generateSortLink={h.onClick}/>
        </Cell>);
            });
        },
        enumerable: false,
        configurable: true
    });
    UsageStatsProjects.prototype.getTableLink = function (project) {
        var _a = this.props, dataCategory = _a.dataCategory, getNextLocations = _a.getNextLocations, organization = _a.organization;
        var _b = getNextLocations(project), performance = _b.performance, projectDetail = _b.projectDetail, settings = _b.settings;
        if (dataCategory === DataCategory.TRANSACTIONS &&
            organization.features.includes('performance-view')) {
            return {
                projectLink: performance,
                projectSettingsLink: settings,
            };
        }
        return {
            projectLink: projectDetail,
            projectSettingsLink: settings,
        };
    };
    UsageStatsProjects.prototype.mapSeriesToTable = function (projectStats) {
        var _a;
        var _this = this;
        if (!projectStats) {
            return { tableStats: [] };
        }
        var stats = {};
        try {
            var _b = this.props, dataCategory_1 = _b.dataCategory, projects = _b.projects;
            var baseStat_1 = (_a = {},
                _a[SortBy.TOTAL] = 0,
                _a[SortBy.ACCEPTED] = 0,
                _a[SortBy.FILTERED] = 0,
                _a[SortBy.DROPPED] = 0,
                _a);
            projectStats.groups.forEach(function (group) {
                var _a = group.by, outcome = _a.outcome, category = _a.category, project = _a.project;
                // Backend enum is singlar. Frontend enum is plural.
                if (!dataCategory_1.includes(category)) {
                    return;
                }
                if (!stats[project]) {
                    stats[project] = __assign({}, baseStat_1);
                }
                stats[project].total += group.totals['sum(quantity)'];
                // Combine invalid outcomes with dropped
                if (outcome !== SortBy.INVALID) {
                    stats[project][outcome] += group.totals['sum(quantity)'];
                }
                else {
                    stats[project][SortBy.DROPPED] += group.totals['sum(quantity)'];
                }
            });
            // For projects without stats, fill in with zero
            var tableStats = projects.map(function (proj) {
                var _a;
                var stat = (_a = stats[proj.id]) !== null && _a !== void 0 ? _a : __assign({}, baseStat_1);
                return __assign(__assign({ project: __assign({}, proj) }, _this.getTableLink(proj)), stat);
            });
            var _c = this.tableSort, key_1 = _c.key, direction_1 = _c.direction;
            tableStats.sort(function (a, b) {
                if (key_1 === SortBy.PROJECT) {
                    return b.project.slug.localeCompare(a.project.slug) * direction_1;
                }
                return a[key_1] !== b[key_1]
                    ? (b[key_1] - a[key_1]) * direction_1
                    : a.project.slug.localeCompare(b.project.slug);
            });
            return { tableStats: tableStats };
        }
        catch (err) {
            Sentry.withScope(function (scope) {
                scope.setContext('query', _this.endpointQuery);
                scope.setContext('body', projectStats);
                Sentry.captureException(err);
            });
            return {
                tableStats: [],
                error: err,
            };
        }
    };
    UsageStatsProjects.prototype.renderComponent = function () {
        var _a = this.state, error = _a.error, errors = _a.errors, loading = _a.loading, projectStats = _a.projectStats;
        var _b = this.props, dataCategory = _b.dataCategory, loadingProjects = _b.loadingProjects;
        var _c = this.tableData, headers = _c.headers, tableStats = _c.tableStats;
        return (<UsageTable isLoading={loading || loadingProjects} isError={error || !projectStats} errors={errors} // TODO(ts)
         isEmpty={tableStats.length === 0} headers={headers} dataCategory={dataCategory} usageStats={tableStats}/>);
    };
    return UsageStatsProjects;
}(AsyncComponent));
export default withProjects(UsageStatsProjects);
//# sourceMappingURL=usageStatsProjects.jsx.map