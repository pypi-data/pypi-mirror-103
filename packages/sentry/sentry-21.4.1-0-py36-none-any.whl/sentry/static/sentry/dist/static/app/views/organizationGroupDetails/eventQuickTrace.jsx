import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import quickTraceExample from 'sentry-images/spot/performance-quick-trace.svg';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getDocsPlatform } from 'app/utils/docs';
import { snoozedDays } from 'app/utils/promptsActivity';
import withApi from 'app/utils/withApi';
var EventQuickTrace = /** @class */ (function (_super) {
    __extends(EventQuickTrace, _super);
    function EventQuickTrace() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldShow: undefined,
        };
        return _this;
    }
    EventQuickTrace.prototype.componentDidMount = function () {
        this.fetchData();
    };
    EventQuickTrace.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, group, organization, project, data;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, group = _a.group, organization = _a.organization;
                        project = group.project;
                        return [4 /*yield*/, promptsCheck(api, {
                                projectId: project.id,
                                organizationId: organization.id,
                                feature: 'distributed_tracing',
                            })];
                    case 1:
                        data = _b.sent();
                        this.setState({ shouldShow: this.shouldShow(data !== null && data !== void 0 ? data : {}) });
                        return [2 /*return*/];
                }
            });
        });
    };
    EventQuickTrace.prototype.shouldShow = function (_a) {
        var snoozedTime = _a.snoozedTime, dismissedTime = _a.dismissedTime;
        if (dismissedTime) {
            return false;
        }
        if (snoozedTime) {
            return snoozedDays(snoozedTime) > 7;
        }
        return true;
    };
    EventQuickTrace.prototype.trackAnalytics = function (_a) {
        var eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, group = _b.group, organization = _b.organization;
        var project = group.project;
        trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: parseInt(organization.id, 10),
            project_id: parseInt(project.id, 10),
            platform: project.platform,
        });
    };
    EventQuickTrace.prototype.handleClick = function (_a) {
        var _this = this;
        var action = _a.action, eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, api = _b.api, group = _b.group, organization = _b.organization;
        var project = group.project;
        var data = {
            projectId: project.id,
            organizationId: organization.id,
            feature: 'distributed_tracing',
            status: action,
        };
        promptsUpdate(api, data).then(function () { return _this.setState({ shouldShow: false }); });
        this.trackAnalytics({ eventKey: eventKey, eventName: eventName });
    };
    EventQuickTrace.prototype.createDocsLink = function () {
        var _a;
        var platform = (_a = this.props.group.project.platform) !== null && _a !== void 0 ? _a : null;
        var docsPlatform = platform ? getDocsPlatform(platform, true) : null;
        return docsPlatform === null
            ? 'https://docs.sentry.io/product/performance/getting-started/'
            : "https://docs.sentry.io/platforms/" + docsPlatform + "/performance/";
    };
    EventQuickTrace.prototype.render = function () {
        var _this = this;
        var shouldShow = this.state.shouldShow;
        if (!shouldShow) {
            return null;
        }
        return (<StyledPanel dashedBorder>
        <div>
          <Description>
            <h3>{t('Configure Distributed Tracing')}</h3>
            <p>{t('See what happened right before and after this error')}</p>
          </Description>
          <ButtonList>
            <Button size="small" priority="primary" href={this.createDocsLink()} onClick={function () {
                return _this.trackAnalytics({
                    eventKey: 'quick_trace.missing_instrumentation.docs',
                    eventName: 'Quick Trace: Missing Instrumentation Docs',
                });
            }}>
              {t('Read the docs')}
            </Button>
            <ButtonBar merged>
              <Button title={t('Remind me next week')} size="small" onClick={function () {
                return _this.handleClick({
                    action: 'snoozed',
                    eventKey: 'quick_trace.missing_instrumentation.snoozed',
                    eventName: 'Quick Trace: Missing Instrumentation Snoozed',
                });
            }}>
                {t('Snooze')}
              </Button>
              <Button title={t('Dismiss for this project')} size="small" onClick={function () {
                return _this.handleClick({
                    action: 'dismissed',
                    eventKey: 'quick_trace.missing_instrumentation.dismissed',
                    eventName: 'Quick Trace: Missing Instrumentation Dismissed',
                });
            }}>
                {t('Dismiss')}
              </Button>
            </ButtonBar>
          </ButtonList>
        </div>
        <div>
          <Image src={quickTraceExample} alt="configure distributed tracing"/>
        </div>
      </StyledPanel>);
    };
    return EventQuickTrace;
}(React.Component));
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  padding-bottom: ", ";\n  background: none;\n  margin-bottom: 0;\n  margin-top: ", ";\n  display: grid;\n  align-content: space-between;\n  align-items: start;\n  grid-template-columns: repeat(auto-fit, minmax(256px, 1fr));\n"], ["\n  padding: ", ";\n  padding-bottom: ", ";\n  background: none;\n  margin-bottom: 0;\n  margin-top: ", ";\n  display: grid;\n  align-content: space-between;\n  align-items: start;\n  grid-template-columns: repeat(auto-fit, minmax(256px, 1fr));\n"])), space(3), space(1), space(1));
var Description = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  h3 {\n    font-size: 14px;\n    text-transform: uppercase;\n    margin-bottom: ", ";\n    color: ", ";\n  }\n\n  p {\n    font-size: 13px;\n    font-weight: bold;\n    color: ", ";\n    margin-bottom: ", ";\n  }\n"], ["\n  h3 {\n    font-size: 14px;\n    text-transform: uppercase;\n    margin-bottom: ", ";\n    color: ", ";\n  }\n\n  p {\n    font-size: 13px;\n    font-weight: bold;\n    color: ", ";\n    margin-bottom: ", ";\n  }\n"])), space(0.25), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; }, space(1.5));
var ButtonList = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  justify-self: end;\n  margin-bottom: 16px;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  justify-self: end;\n  margin-bottom: 16px;\n"])), space(1));
var Image = styled('img')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  float: right;\n"], ["\n  float: right;\n"])));
export default withApi(EventQuickTrace);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=eventQuickTrace.jsx.map