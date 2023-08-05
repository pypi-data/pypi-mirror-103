import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import EventTagsPill from 'app/components/events/eventTags/eventTagsPill';
import { SecondaryHeader } from 'app/components/events/interfaces/spans/header';
import { Panel } from 'app/components/panels';
import Pills from 'app/components/pills';
import SearchBar from 'app/components/searchBar';
import { IconFire } from 'app/icons';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { appendTagCondition } from 'app/utils/queryString';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
export { Row, SpanDetails as TransactionDetails, SpanDetailContainer as TransactionDetailsContainer, } from 'app/components/events/interfaces/spans/spanDetail';
export var SearchContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n"], ["\n  display: flex;\n  width: 100%;\n"])));
export var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
export var TraceViewHeaderContainer = styled(SecondaryHeader)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: static;\n  top: auto;\n  border-top: none;\n  border-bottom: 1px solid ", ";\n"], ["\n  position: static;\n  top: auto;\n  border-top: none;\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.border; });
export var TraceDetailHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(250px, 1fr) minmax(160px, 1fr) 6fr;\n    grid-row-gap: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(250px, 1fr) minmax(160px, 1fr) 6fr;\n    grid-row-gap: 0;\n  }\n"])), space(2), space(2), function (p) { return p.theme.breakpoints[1]; });
export var TraceDetailBody = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
export var TraceViewContainer = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"], ["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"])));
export var StyledPanel = styled(Panel)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
export var TransactionBarTitleContent = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.75));
export var DividerContainer = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var BadgeBorder = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  position: absolute;\n  margin: ", ";\n  left: -11.5px;\n  background: ", ";\n  width: ", ";\n  height: ", ";\n  border: 1px solid ", ";\n  border-radius: 50%;\n  z-index: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  position: absolute;\n  margin: ", ";\n  left: -11.5px;\n  background: ", ";\n  width: ", ";\n  height: ", ";\n  border: 1px solid ", ";\n  border-radius: 50%;\n  z-index: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), space(0.25), function (p) { return (p.showDetail ? p.theme.textColor : p.theme.background); }, space(3), space(3), function (p) { return p.theme.red300; }, function (p) { return p.theme.zIndex.traceView.dividerLine; });
export function ErrorBadge(_a) {
    var showDetail = _a.showDetail;
    return (<BadgeBorder showDetail={showDetail}>
      <IconFire color="red300" size="xs"/>
    </BadgeBorder>);
}
export var ErrorMessageTitle = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
export var ErrorMessageContent = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: 16px 72px auto;\n  grid-gap: ", ";\n  margin-top: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: 16px 72px auto;\n  grid-gap: ", ";\n  margin-top: ", ";\n"])), space(0.75), space(0.75));
export var ErrorDot = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  background-color: ", ";\n  content: '';\n  width: ", ";\n  min-width: ", ";\n  height: ", ";\n  margin-right: ", ";\n  border-radius: 100%;\n  flex: 1;\n"], ["\n  background-color: ", ";\n  content: '';\n  width: ", ";\n  min-width: ", ";\n  height: ", ";\n  margin-right: ", ";\n  border-radius: 100%;\n  flex: 1;\n"])), function (p) { return p.theme.level[p.level]; }, space(1), space(1), space(1), space(1));
export var ErrorLevel = styled('span')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  width: 80px;\n"], ["\n  width: 80px;\n"])));
export var ErrorTitle = styled('span')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var StyledPills = styled(Pills)(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space(1.5));
export function Tags(_a) {
    var location = _a.location, organization = _a.organization, transaction = _a.transaction;
    var tags = transaction.tags;
    if (!tags || tags.length <= 0) {
        return null;
    }
    var orgSlug = organization.slug;
    var releasesPath = "/organizations/" + orgSlug + "/releases/";
    return (<tr>
      <td className="key">Tags</td>
      <td className="value">
        <StyledPills>
          {tags.map(function (tag, index) {
            var _a = transactionSummaryRouteWithQuery({
                orgSlug: orgSlug,
                transaction: transaction.transaction,
                projectID: String(transaction.project_id),
                query: __assign(__assign({}, location.query), { query: appendTagCondition(location.query.query, tag.key, tag.value) }),
            }), streamPath = _a.pathname, query = _a.query;
            return (<EventTagsPill key={!defined(tag.key) ? "tag-pill-" + index : tag.key} tag={tag} projectId={transaction.project_slug} organization={organization} location={location} query={query} streamPath={streamPath} releasesPath={releasesPath} hasQueryFeature={false}/>);
        })}
        </StyledPills>
      </td>
    </tr>);
}
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=styles.jsx.map