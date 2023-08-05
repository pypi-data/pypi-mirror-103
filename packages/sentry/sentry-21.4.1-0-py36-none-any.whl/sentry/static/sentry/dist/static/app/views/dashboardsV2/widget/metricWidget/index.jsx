import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { components } from 'react-select';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import cloneDeep from 'lodash/cloneDeep';
import set from 'lodash/set';
import Highlight from 'app/components/highlight';
import * as Layout from 'app/components/layouts/thirds';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import PickProjectToContinue from 'app/components/pickProjectToContinue';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withProjects from 'app/utils/withProjects';
import AsyncView from 'app/views/asyncView';
import SelectField from 'app/views/settings/components/forms/selectField';
import BuildStep from '../buildStep';
import BuildSteps from '../buildSteps';
import ChooseDataSetStep from '../choseDataStep';
import Header from '../header';
import { DataSet, DisplayType, displayTypes } from '../utils';
import Card from './card';
import Queries from './queries';
var newQuery = {
    tags: '',
    groupBy: [],
    aggregation: '',
    legend: '',
};
var MetricWidget = /** @class */ (function (_super) {
    __extends(MetricWidget, _super);
    function MetricWidget() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFieldChange = function (field, value) {
            _this.setState(function (state) {
                var _a;
                return (__assign(__assign({}, state), (_a = {}, _a[field] = value, _a)));
            });
        };
        _this.handleMetricChange = function (metric) {
            _this.setState({ metric: metric, queries: [__assign(__assign({}, newQuery), { aggregation: metric.operations[0] })] });
        };
        _this.handleRemoveQuery = function (index) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                newState.queries.splice(index, index + 1);
                return newState;
            });
        };
        _this.handleAddQuery = function () {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                newState.queries.push(cloneDeep(newQuery));
                return newState;
            });
        };
        _this.handleChangeQuery = function (index, query) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                set(newState, "queries." + index, query);
                return newState;
            });
        };
        _this.handleProjectChange = function (selectedProjects) {
            var _a = _this.props, projects = _a.projects, router = _a.router, location = _a.location, organization = _a.organization;
            var newlySelectedProject = projects.find(function (p) { return p.id === String(selectedProjects[0]); });
            // if we change project in global header, we need to sync the project slug in the URL
            if (newlySelectedProject === null || newlySelectedProject === void 0 ? void 0 : newlySelectedProject.id) {
                router.replace({
                    pathname: "/organizations/" + organization.slug + "/dashboards/widget/new/",
                    query: __assign(__assign({}, location.query), { project: newlySelectedProject.id, environment: undefined }),
                });
            }
        };
        return _this;
    }
    MetricWidget.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { title: t('Custom Widget'), displayType: DisplayType.LINE, metrics: [], queries: [__assign({}, newQuery)] });
    };
    Object.defineProperty(MetricWidget.prototype, "project", {
        get: function () {
            var _a = this.props, projects = _a.projects, location = _a.location;
            var query = location.query;
            var projectId = query.project;
            return projects.find(function (project) { return project.id === projectId; });
        },
        enumerable: false,
        configurable: true
    });
    MetricWidget.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, loadingProjects = _a.loadingProjects;
        if (this.isProjectMissingInUrl() || loadingProjects || !this.project) {
            return [];
        }
        return [['metrics', "/projects/" + organization.slug + "/" + this.project.slug + "/metrics/"]];
    };
    MetricWidget.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (prevProps.loadingProjects && !this.props.loadingProjects) {
            this.reloadData();
        }
        if (!prevState.metrics.length && !!this.state.metrics.length) {
            this.handleMetricChange(this.state.metrics[0]);
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    MetricWidget.prototype.isProjectMissingInUrl = function () {
        var projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    };
    MetricWidget.prototype.handleSave = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2 /*return*/];
            });
        });
    };
    MetricWidget.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, router = _a.router, projects = _a.projects, onChangeDataSet = _a.onChangeDataSet, selection = _a.selection, location = _a.location, loadingProjects = _a.loadingProjects, params = _a.params, theme = _a.theme;
        var dashboardId = params.dashboardId;
        var _b = this.state, title = _b.title, metrics = _b.metrics, metric = _b.metric, queries = _b.queries, displayType = _b.displayType;
        var orgSlug = organization.slug;
        if (loadingProjects) {
            return this.renderLoading();
        }
        var project = this.project;
        if (this.isProjectMissingInUrl() || !project) {
            return (<PickProjectToContinue router={router} projects={projects.map(function (p) { return ({ id: p.id, slug: p.slug }); })} nextPath={"/organizations/" + orgSlug + "/dashboards/" + dashboardId + "/widget/new/?dataSet=metrics"} noProjectRedirectPath={"/organizations/" + orgSlug + "/dashboards/"}/>);
        }
        return (<GlobalSelectionHeader onUpdateProjects={this.handleProjectChange} disableMultipleProjectSelection skipLoadLastUsed>
        <StyledPageContent>
          <Header orgSlug={orgSlug} title={title} onChangeTitle={function (newTitle) { return _this.handleFieldChange('title', newTitle); }} onSave={this.handleSave}/>
          <Layout.Body>
            <BuildSteps>
              <BuildStep title={t('Choose your visualization')} description={t('This is a preview of how your widget will appear in the dashboard.')}>
                <VisualizationWrapper>
                  <StyledSelectField name="displayType" choices={Object.keys(displayTypes).map(function (value) { return [
                value,
                displayTypes[value],
            ]; })} value={displayType} onChange={function (option) {
                var isDisabled = option.value !== DisplayType.LINE;
                if (isDisabled) {
                    return;
                }
                _this.handleFieldChange('displayType', option.value);
            }} styles={{
                option: function (provided, state) {
                    if (state.isDisabled) {
                        return __assign(__assign({}, provided), { cursor: 'not-allowed', color: theme.disabled, ':hover': {
                                background: 'transparent',
                            } });
                    }
                    return provided;
                },
            }} components={{
                Option: function (_a) {
                    var label = _a.label, data = _a.data, optionProps = __rest(_a, ["label", "data"]);
                    var value = data.value;
                    var isDisabled = value !== DisplayType.LINE;
                    return (<Tooltip title={t('This option is not yet available')} containerDisplayMode="block" disabled={!isDisabled}>
                            <components.Option {...optionProps} label={label} data={data} isDisabled={isDisabled}>
                              {label}
                            </components.Option>
                          </Tooltip>);
                },
            }} inline={false} flexibleControlStateSize stacked/>

                  <Card router={router} location={location} selection={selection} organization={organization} api={this.api} project={project} widget={{
                title: title,
                queries: queries,
                yAxis: metric === null || metric === void 0 ? void 0 : metric.name,
            }}/>
                </VisualizationWrapper>
              </BuildStep>
              <ChooseDataSetStep value={DataSet.METRICS} onChange={onChangeDataSet}/>
              <BuildStep title={t('Choose your y-axis metric')} description={t('Determine what type of metric you want to graph by.')}>
                <StyledSelectField name="metric" choices={metrics.map(function (m) { return [m, m.name]; })} placeholder={t('Select metric')} onChange={this.handleMetricChange} value={metric} components={{
                Option: function (_a) {
                    var label = _a.label, optionProps = __rest(_a, ["label"]);
                    var selectProps = optionProps.selectProps;
                    var inputValue = selectProps.inputValue;
                    return (<components.Option label={label} {...optionProps}>
                          <Highlight text={inputValue !== null && inputValue !== void 0 ? inputValue : ''}>{label}</Highlight>
                        </components.Option>);
                },
            }} inline={false} flexibleControlStateSize stacked allowClear/>
              </BuildStep>
              <BuildStep title={t('Begin your search')} description={t('Add another query to compare projects, tags, etc.')}>
                <Queries api={this.api} orgSlug={orgSlug} projectSlug={project.slug} metrics={metrics} metric={metric} queries={queries} onAddQuery={this.handleAddQuery} onRemoveQuery={this.handleRemoveQuery} onChangeQuery={this.handleChangeQuery}/>
              </BuildStep>
            </BuildSteps>
          </Layout.Body>
        </StyledPageContent>
      </GlobalSelectionHeader>);
    };
    return MetricWidget;
}(AsyncView));
export default withTheme(withProjects(withGlobalSelection(MetricWidget)));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledSelectField = styled(SelectField)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var VisualizationWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map