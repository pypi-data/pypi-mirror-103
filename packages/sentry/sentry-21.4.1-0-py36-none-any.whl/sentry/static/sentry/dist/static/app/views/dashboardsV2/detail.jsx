import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { createDashboard, deleteDashboard, updateDashboard, } from 'app/actionCreators/dashboards';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import NotFound from 'app/components/errors/notFound';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import Controls from './controls';
import Dashboard from './dashboard';
import { DEFAULT_STATS_PERIOD, EMPTY_DASHBOARD } from './data';
import OrgDashboards from './orgDashboards';
import DashboardTitle from './title';
import { cloneDashboard } from './utils';
var UNSAVED_MESSAGE = t('You have unsaved changes, are you sure you want to leave?');
var DashboardDetail = /** @class */ (function (_super) {
    __extends(DashboardDetail, _super);
    function DashboardDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dashboardState: 'view',
            modifiedDashboard: null,
        };
        _this.onEdit = function (dashboard) { return function () {
            if (!dashboard) {
                return;
            }
            trackAnalyticsEvent({
                eventKey: 'dashboards2.edit.start',
                eventName: 'Dashboards2: Edit start',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState({
                dashboardState: 'edit',
                modifiedDashboard: cloneDashboard(dashboard),
            });
        }; };
        _this.onRouteLeave = function () {
            if (!['view', 'pending_delete'].includes(_this.state.dashboardState)) {
                return UNSAVED_MESSAGE;
            }
            return undefined;
        };
        _this.onUnload = function (event) {
            if (['view', 'pending_delete'].includes(_this.state.dashboardState)) {
                return;
            }
            event.preventDefault();
            event.returnValue = UNSAVED_MESSAGE;
        };
        _this.onCreate = function () {
            trackAnalyticsEvent({
                eventKey: 'dashboards2.create.start',
                eventName: 'Dashboards2: Create start',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState({
                dashboardState: 'create',
                modifiedDashboard: cloneDashboard(EMPTY_DASHBOARD),
            });
        };
        _this.onCancel = function () {
            if (_this.state.dashboardState === 'create') {
                trackAnalyticsEvent({
                    eventKey: 'dashboards2.create.cancel',
                    eventName: 'Dashboards2: Create cancel',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
            }
            else if (_this.state.dashboardState === 'edit') {
                trackAnalyticsEvent({
                    eventKey: 'dashboards2.edit.cancel',
                    eventName: 'Dashboards2: Edit cancel',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
            }
            _this.setState({
                dashboardState: 'view',
                modifiedDashboard: null,
            });
        };
        _this.onDelete = function (dashboard) { return function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location;
            if (!(dashboard === null || dashboard === void 0 ? void 0 : dashboard.id)) {
                return;
            }
            var previousDashboardState = _this.state.dashboardState;
            _this.setState({
                dashboardState: 'pending_delete',
            }, function () {
                trackAnalyticsEvent({
                    eventKey: 'dashboards2.delete',
                    eventName: 'Dashboards2: Delete',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
                deleteDashboard(api, organization.slug, dashboard.id)
                    .then(function () {
                    addSuccessMessage(t('Dashboard deleted'));
                    browserHistory.replace({
                        pathname: "/organizations/" + organization.slug + "/dashboards/",
                        query: __assign({}, location.query),
                    });
                })
                    .catch(function () {
                    _this.setState({
                        dashboardState: previousDashboardState,
                    });
                });
            });
        }; };
        _this.onCommit = function (_a) {
            var dashboard = _a.dashboard, reloadData = _a.reloadData;
            return function () {
                var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location;
                var _b = _this.state, dashboardState = _b.dashboardState, modifiedDashboard = _b.modifiedDashboard;
                switch (dashboardState) {
                    case 'create': {
                        if (modifiedDashboard) {
                            createDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                                addSuccessMessage(t('Dashboard created'));
                                trackAnalyticsEvent({
                                    eventKey: 'dashboards2.create.complete',
                                    eventName: 'Dashboards2: Create complete',
                                    organization_id: parseInt(organization.id, 10),
                                });
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                // redirect to new dashboard
                                browserHistory.replace({
                                    pathname: "/organizations/" + organization.slug + "/dashboards/" + newDashboard.id + "/",
                                    query: __assign({}, location.query),
                                });
                            });
                        }
                        break;
                    }
                    case 'edit': {
                        if (modifiedDashboard) {
                            // only update the dashboard if there are changes
                            if (isEqual(dashboard, modifiedDashboard)) {
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                return;
                            }
                            updateDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                                addSuccessMessage(t('Dashboard updated'));
                                trackAnalyticsEvent({
                                    eventKey: 'dashboards2.edit.complete',
                                    eventName: 'Dashboards2: Edit complete',
                                    organization_id: parseInt(organization.id, 10),
                                });
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                if (dashboard && newDashboard.id !== dashboard.id) {
                                    browserHistory.replace({
                                        pathname: "/organizations/" + organization.slug + "/dashboards/" + newDashboard.id + "/",
                                        query: __assign({}, location.query),
                                    });
                                    return;
                                }
                                reloadData();
                            });
                            return;
                        }
                        _this.setState({
                            dashboardState: 'view',
                            modifiedDashboard: null,
                        });
                        break;
                    }
                    case 'view':
                    default: {
                        _this.setState({
                            dashboardState: 'view',
                            modifiedDashboard: null,
                        });
                        break;
                    }
                }
            };
        };
        _this.onWidgetChange = function (widgets) {
            var modifiedDashboard = _this.state.modifiedDashboard;
            if (modifiedDashboard === null) {
                return;
            }
            _this.setState(function (prevState) {
                return __assign(__assign({}, prevState), { modifiedDashboard: __assign(__assign({}, prevState.modifiedDashboard), { widgets: widgets }) });
            });
        };
        _this.setModifiedDashboard = function (dashboard) {
            _this.setState({
                modifiedDashboard: dashboard,
            });
        };
        _this.onSaveWidget = function (widgets) {
            var modifiedDashboard = _this.state.modifiedDashboard;
            if (modifiedDashboard === null) {
                return;
            }
            _this.setState(function (state) { return (__assign(__assign({}, state), { modifiedDashboard: __assign(__assign({}, state.modifiedDashboard), { widgets: widgets }) })); }, _this.updateRouteAfterSavingWidget);
        };
        return _this;
    }
    DashboardDetail.prototype.componentDidMount = function () {
        var _a = this.props, route = _a.route, router = _a.router;
        this.checkStateRoute();
        router.setRouteLeaveHook(route, this.onRouteLeave);
        window.addEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.componentWillUnmount = function () {
        window.removeEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.checkStateRoute = function () {
        if (this.isWidgetBuilderRouter && !this.isEditing) {
            var _a = this.props, router = _a.router, organization = _a.organization, params = _a.params;
            var dashboardId = params.dashboardId;
            router.replace("/organizations/" + organization.slug + "/dashboards/" + dashboardId + "/");
        }
    };
    DashboardDetail.prototype.updateRouteAfterSavingWidget = function () {
        if (this.isWidgetBuilderRouter) {
            var _a = this.props, router = _a.router, organization = _a.organization, params = _a.params;
            var dashboardId = params.dashboardId;
            router.replace("/organizations/" + organization.slug + "/dashboards/" + dashboardId + "/");
        }
    };
    Object.defineProperty(DashboardDetail.prototype, "isEditing", {
        get: function () {
            var dashboardState = this.state.dashboardState;
            return ['edit', 'create', 'pending_delete'].includes(dashboardState);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DashboardDetail.prototype, "isWidgetBuilderRouter", {
        get: function () {
            var _a = this.props, location = _a.location, params = _a.params, organization = _a.organization;
            var dashboardId = params.dashboardId;
            return (location.pathname ===
                "/organizations/" + organization.slug + "/dashboards/" + dashboardId + "/widget/new/");
        },
        enumerable: false,
        configurable: true
    });
    DashboardDetail.prototype.renderDetails = function (_a) {
        var dashboard = _a.dashboard, dashboards = _a.dashboards, reloadData = _a.reloadData, error = _a.error;
        var _b = this.props, organization = _b.organization, params = _b.params;
        var _c = this.state, modifiedDashboard = _c.modifiedDashboard, dashboardState = _c.dashboardState;
        var dashboardId = params.dashboardId;
        return (<GlobalSelectionHeader skipLoadLastUsed={organization.features.includes('global-views')} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: DEFAULT_STATS_PERIOD,
                },
            }}>
        <PageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <StyledPageHeader>
              <DashboardTitle dashboard={modifiedDashboard || dashboard} onUpdate={this.setModifiedDashboard} isEditing={this.isEditing}/>
              <Controls organization={organization} dashboards={dashboards} dashboard={dashboard} onEdit={this.onEdit(dashboard)} onCreate={this.onCreate} onCancel={this.onCancel} onCommit={this.onCommit({ dashboard: dashboard, reloadData: reloadData })} onDelete={this.onDelete(dashboard)} dashboardState={dashboardState}/>
            </StyledPageHeader>
            {error ? (<NotFound />) : dashboard ? (<Dashboard dashboard={modifiedDashboard || dashboard} paramDashboardId={dashboardId} organization={organization} isEditing={this.isEditing} onUpdate={this.onWidgetChange}/>) : (<LoadingIndicator />)}
          </LightWeightNoProjectMessage>
        </PageContent>
      </GlobalSelectionHeader>);
    };
    DashboardDetail.prototype.renderWidgetBuilder = function (dashboard) {
        var children = this.props.children;
        var modifiedDashboard = this.state.modifiedDashboard;
        return React.isValidElement(children)
            ? React.cloneElement(children, {
                dashboard: modifiedDashboard || dashboard,
                onSave: this.onSaveWidget,
            })
            : children;
    };
    DashboardDetail.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, location = _a.location, params = _a.params, organization = _a.organization;
        return (<OrgDashboards api={api} location={location} params={params} organization={organization}>
        {function (_a) {
                var dashboard = _a.dashboard, dashboards = _a.dashboards, error = _a.error, reloadData = _a.reloadData;
                if (_this.isEditing && _this.isWidgetBuilderRouter) {
                    return _this.renderWidgetBuilder(dashboard);
                }
                return _this.renderDetails({ dashboard: dashboard, dashboards: dashboards, error: error, reloadData: reloadData });
            }}
      </OrgDashboards>);
    };
    return DashboardDetail;
}(React.Component));
var StyledPageHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: flex-start;\n    height: auto;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: flex-start;\n    height: auto;\n  }\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space(2), function (p) { return p.theme.breakpoints[2]; });
export default withApi(withOrganization(DashboardDetail));
var templateObject_1;
//# sourceMappingURL=detail.jsx.map