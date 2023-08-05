import { __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DateTime from 'app/components/dateTime';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import TimeSince from 'app/components/timeSince';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getShortEventId } from 'app/utils/events';
import { getDuration } from 'app/utils/formatters';
import { isTransaction } from 'app/utils/performance/quickTrace/utils';
import Projects from 'app/utils/projects';
import theme from 'app/utils/theme';
import QuickTraceMeta from './quickTraceMeta';
import { MetaData } from './styles';
/**
 * This should match the breakpoint chosen for the `EventDetailHeader` below
 */
var BREAKPOINT_MEDIA_QUERY = "(min-width: " + theme.breakpoints[2] + ")";
var EventMetas = /** @class */ (function (_super) {
    __extends(EventMetas, _super);
    function EventMetas() {
        var _a, _b, _c;
        var _this = _super.apply(this, __spreadArray([], __read(arguments))) || this;
        _this.state = {
            isLargeScreen: (_b = (_a = window.matchMedia) === null || _a === void 0 ? void 0 : _a.call(window, BREAKPOINT_MEDIA_QUERY)) === null || _b === void 0 ? void 0 : _b.matches,
        };
        _this.mq = (_c = window.matchMedia) === null || _c === void 0 ? void 0 : _c.call(window, BREAKPOINT_MEDIA_QUERY);
        _this.handleMediaQueryChange = function (changed) {
            _this.setState({
                isLargeScreen: changed.matches,
            });
        };
        return _this;
    }
    EventMetas.prototype.componentDidMount = function () {
        if (this.mq) {
            this.mq.addListener(this.handleMediaQueryChange);
        }
    };
    EventMetas.prototype.componentWillUnmount = function () {
        if (this.mq) {
            this.mq.removeListener(this.handleMediaQueryChange);
        }
    };
    EventMetas.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, event = _d.event, organization = _d.organization, projectId = _d.projectId, location = _d.location, quickTrace = _d.quickTrace, meta = _d.meta, errorDest = _d.errorDest, transactionDest = _d.transactionDest;
        var isLargeScreen = this.state.isLargeScreen;
        var type = isTransaction(event) ? 'transaction' : 'event';
        var projectBadge = (<Projects orgId={organization.slug} slugs={[projectId]}>
        {function (_a) {
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === projectId; });
                return (<ProjectBadge project={project ? project : { slug: projectId }} avatarSize={16}/>);
            }}
      </Projects>);
        var timestamp = (<TimeSince date={event.dateCreated || (event.endTimestamp || 0) * 1000}/>);
        var httpStatus = <HttpStatus event={event}/>;
        return (<EventDetailHeader type={type}>
        <MetaData headingText={t('Event ID')} tooltipText={t('The unique ID assigned to this %s.', type)} bodyText={getShortEventId(event.eventID)} subtext={projectBadge}/>
        {isTransaction(event) ? (<MetaData headingText={t('Event Duration')} tooltipText={t('The time elapsed between the start and end of this transaction.')} bodyText={getDuration(event.endTimestamp - event.startTimestamp, 2, true)} subtext={timestamp}/>) : (<MetaData headingText={t('Created')} tooltipText={t('The time at which this event was created.')} bodyText={timestamp} subtext={<DateTime date={event.dateCreated}/>}/>)}
        {isTransaction(event) && (<MetaData headingText={t('Status')} tooltipText={t('The status of this transaction indicating if it succeeded or otherwise.')} bodyText={(_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.status) !== null && _c !== void 0 ? _c : '\u2014'} subtext={httpStatus}/>)}
        <QuickTraceContainer>
          <QuickTraceMeta event={event} organization={organization} location={location} quickTrace={quickTrace} traceMeta={meta} anchor={isLargeScreen ? 'right' : 'left'} errorDest={errorDest} transactionDest={transactionDest}/>
        </QuickTraceContainer>
      </EventDetailHeader>);
    };
    return EventMetas;
}(React.Component));
var EventDetailHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n\n  /* This should match the breakpoint chosen for BREAKPOINT_MEDIA_QUERY above. */\n  @media (min-width: ", ") {\n    ", ";\n    grid-row-gap: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n\n  /* This should match the breakpoint chosen for BREAKPOINT_MEDIA_QUERY above. */\n  @media (min-width: ", ") {\n    ",
    ";\n    grid-row-gap: 0;\n  }\n"])), function (p) { return (p.type === 'transaction' ? 3 : 2); }, space(2), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; }, function (p) {
    return p.type === 'transaction'
        ? 'grid-template-columns: minmax(160px, 1fr) minmax(160px, 1fr) minmax(160px, 1fr) 6fr;'
        : 'grid-template-columns: minmax(160px, 1fr) minmax(200px, 1fr) 6fr;';
});
var QuickTraceContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1/4;\n\n  @media (min-width: ", ") {\n    justify-self: flex-end;\n    min-width: 325px;\n    grid-column: unset;\n  }\n"], ["\n  grid-column: 1/4;\n\n  @media (min-width: ", ") {\n    justify-self: flex-end;\n    min-width: 325px;\n    grid-column: unset;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
function HttpStatus(_a) {
    var event = _a.event;
    var tags = event.tags;
    var emptyStatus = <React.Fragment>{'\u2014'}</React.Fragment>;
    if (!Array.isArray(tags)) {
        return emptyStatus;
    }
    var tag = tags.find(function (tagObject) { return tagObject.key === 'http.status_code'; });
    if (!tag) {
        return emptyStatus;
    }
    return <React.Fragment>HTTP {tag.value}</React.Fragment>;
}
export default EventMetas;
var templateObject_1, templateObject_2;
//# sourceMappingURL=eventMetas.jsx.map