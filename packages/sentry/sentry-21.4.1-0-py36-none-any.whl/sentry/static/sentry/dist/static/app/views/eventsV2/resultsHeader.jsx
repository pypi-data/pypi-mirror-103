import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { fetchSavedQuery } from 'app/actionCreators/discoverSavedQueries';
import * as Layout from 'app/components/layouts/thirds';
import TimeSince from 'app/components/timeSince';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import DiscoverBreadcrumb from './breadcrumb';
import EventInputName from './eventInputName';
import SavedQueryButtonGroup from './savedQuery';
var ResultsHeader = /** @class */ (function (_super) {
    __extends(ResultsHeader, _super);
    function ResultsHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            savedQuery: undefined,
            loading: true,
        };
        return _this;
    }
    ResultsHeader.prototype.componentDidMount = function () {
        if (this.props.eventView.id) {
            this.fetchData();
        }
    };
    ResultsHeader.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.eventView &&
            this.props.eventView &&
            prevProps.eventView.id !== this.props.eventView.id) {
            this.fetchData();
        }
    };
    ResultsHeader.prototype.fetchData = function () {
        var _this = this;
        var _a = this.props, api = _a.api, eventView = _a.eventView, organization = _a.organization;
        if (typeof eventView.id === 'string') {
            this.setState({ loading: true });
            fetchSavedQuery(api, organization.slug, eventView.id).then(function (savedQuery) {
                _this.setState({ savedQuery: savedQuery, loading: false });
            });
        }
    };
    ResultsHeader.prototype.renderAuthor = function () {
        var _a;
        var eventView = this.props.eventView;
        var savedQuery = this.state.savedQuery;
        // No saved query in use.
        if (!eventView.id) {
            return null;
        }
        var createdBy = ' \u2014 ';
        var lastEdit = ' \u2014 ';
        if (savedQuery !== undefined) {
            createdBy = ((_a = savedQuery.createdBy) === null || _a === void 0 ? void 0 : _a.email) || '\u2014';
            lastEdit = <TimeSince date={savedQuery.dateUpdated}/>;
        }
        return (<Subtitle>
        {t('Created by:')} {createdBy} | {t('Last edited:')} {lastEdit}
      </Subtitle>);
    };
    ResultsHeader.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, errorCode = _a.errorCode, eventView = _a.eventView, onIncompatibleAlertQuery = _a.onIncompatibleAlertQuery;
        var _b = this.state, savedQuery = _b.savedQuery, loading = _b.loading;
        return (<StyledLayoutHeader>
        <StyledHeaderContent>
          <DiscoverBreadcrumb eventView={eventView} organization={organization} location={location}/>
          <EventInputName savedQuery={savedQuery} organization={organization} eventView={eventView}/>
          {this.renderAuthor()}
        </StyledHeaderContent>
        <StyledHeaderActions>
          <SavedQueryButtonGroup location={location} organization={organization} eventView={eventView} savedQuery={savedQuery} savedQueryLoading={loading} disabled={errorCode >= 400 && errorCode < 500} updateCallback={function () { return _this.fetchData(); }} onIncompatibleAlertQuery={onIncompatibleAlertQuery}/>
        </StyledHeaderActions>
      </StyledLayoutHeader>);
    };
    return ResultsHeader;
}(React.Component));
var Subtitle = styled('h4')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  line-height: 1.4;\n  color: ", ";\n  margin: 0;\n  margin-top: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  line-height: 1.4;\n  color: ", ";\n  margin: 0;\n  margin-top: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.gray300; }, space(2));
var StyledLayoutHeader = styled(Layout.Header)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-left: 0;\n  @media (min-width: ", ") {\n    padding-left: 0;\n  }\n"], ["\n  padding-left: 0;\n  @media (min-width: ", ") {\n    padding-left: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledHeaderContent = styled(Layout.HeaderContent)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-left: ", ";\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"], ["\n  padding-left: ", ";\n  @media (min-width: ", ") {\n    padding-left: ", ";\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; }, space(4));
var StyledHeaderActions = styled(Layout.HeaderActions)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding-left: ", ";\n  @media (min-width: ", ") {\n    padding-left: 0;\n  }\n"], ["\n  padding-left: ", ";\n  @media (min-width: ", ") {\n    padding-left: 0;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; });
export default withApi(ResultsHeader);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=resultsHeader.jsx.map