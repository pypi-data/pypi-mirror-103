import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import DateTime from 'app/components/dateTime';
import Link from 'app/components/links/link';
import { generateIssueEventTarget } from 'app/components/quickTrace/utils';
import { PAGE_URL_PARAM } from 'app/constants/globalSelectionHeader';
import { IconChevron, IconWarning } from 'app/icons';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import { generateEventSlug } from 'app/utils/discover/urls';
import getDynamicText from 'app/utils/getDynamicText';
import { WEB_VITAL_DETAILS } from 'app/utils/performance/vitals/constants';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import { getTransactionDetailsUrl } from 'app/views/performance/utils';
import { ErrorDot, ErrorLevel, ErrorMessageContent, ErrorMessageTitle, ErrorTitle, Row, Tags, TransactionDetails, TransactionDetailsContainer, } from './styles';
var TransactionDetail = /** @class */ (function (_super) {
    __extends(TransactionDetail, _super);
    function TransactionDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorsOpened: false,
        };
        _this.toggleErrors = function () {
            _this.setState(function (_a) {
                var errorsOpened = _a.errorsOpened;
                return ({ errorsOpened: !errorsOpened });
            });
        };
        return _this;
    }
    TransactionDetail.prototype.renderTransactionErrors = function () {
        var _a = this.props, organization = _a.organization, transaction = _a.transaction;
        var errorsOpened = this.state.errorsOpened;
        var errors = transaction.errors;
        if (errors.length === 0) {
            return null;
        }
        return (<Alert system type="error" icon={<IconWarning size="md"/>}>
        <ErrorMessageTitle>
          {tn('An error event occurred in this transaction.', '%s error events occurred in this transaction.', errors.length)}
          <Toggle priority="link" onClick={this.toggleErrors}>
            <IconChevron direction={errorsOpened ? 'up' : 'down'}/>
          </Toggle>
        </ErrorMessageTitle>
        {errorsOpened && (<ErrorMessageContent>
            {errors.map(function (error) { return (<React.Fragment key={error.event_id}>
                <ErrorDot level={error.level}/>
                <ErrorLevel>{error.level}</ErrorLevel>
                <ErrorTitle>
                  <Link to={generateIssueEventTarget(error, organization)}>
                    {error.title}
                  </Link>
                </ErrorTitle>
              </React.Fragment>); })}
          </ErrorMessageContent>)}
      </Alert>);
    };
    TransactionDetail.prototype.renderGoToTransactionButton = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var eventSlug = generateEventSlug({
            id: transaction.event_id,
            project: transaction.project_slug,
        });
        var target = getTransactionDetailsUrl(organization, eventSlug, transaction.transaction, omit(location.query, Object.values(PAGE_URL_PARAM)));
        return (<StyledButton size="xsmall" to={target}>
        {t('View Transaction')}
      </StyledButton>);
    };
    TransactionDetail.prototype.renderGoToSummaryButton = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var target = transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transaction.transaction,
            query: omit(location.query, Object.values(PAGE_URL_PARAM)),
            projectID: String(transaction.project_id),
        });
        return (<StyledButton size="xsmall" to={target}>
        {t('View Summary')}
      </StyledButton>);
    };
    TransactionDetail.prototype.renderMeasurements = function () {
        var transaction = this.props.transaction;
        var _a = transaction.measurements, measurements = _a === void 0 ? {} : _a;
        var measurementKeys = Object.keys(measurements)
            .filter(function (name) { return Boolean(WEB_VITAL_DETAILS["measurements." + name]); })
            .sort();
        if (measurementKeys.length <= 0) {
            return null;
        }
        return (<React.Fragment>
        {measurementKeys.map(function (measurement) {
                var _a;
                return (<Row key={measurement} title={(_a = WEB_VITAL_DETAILS["measurements." + measurement]) === null || _a === void 0 ? void 0 : _a.name}>
            {Number(measurements[measurement].value.toFixed(3)).toLocaleString() + "ms"}
          </Row>);
            })}
      </React.Fragment>);
    };
    TransactionDetail.prototype.renderTransactionDetail = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction;
        var startTimestamp = Math.min(transaction.start_timestamp, transaction.timestamp);
        var endTimestamp = Math.max(transaction.start_timestamp, transaction.timestamp);
        var duration = (endTimestamp - startTimestamp) * 1000;
        var durationString = Number(duration.toFixed(3)).toLocaleString() + "ms";
        return (<TransactionDetails>
        <table className="table key-value">
          <tbody>
            <Row title="Transaction ID" extra={this.renderGoToTransactionButton()}>
              {transaction.event_id}
            </Row>
            <Row title="Transaction" extra={this.renderGoToSummaryButton()}>
              {transaction.transaction}
            </Row>
            <Row title="Transaction Status">{transaction['transaction.status']}</Row>
            <Row title="Span ID">{transaction.span_id}</Row>
            <Row title="Project">{transaction.project_slug}</Row>
            <Row title="Start Date">
              {getDynamicText({
                fixed: 'Mar 19, 2021 11:06:27 AM UTC',
                value: (<React.Fragment>
                    <DateTime date={startTimestamp * 1000}/>
                    {" (" + startTimestamp + ")"}
                  </React.Fragment>),
            })}
            </Row>
            <Row title="End Date">
              {getDynamicText({
                fixed: 'Mar 19, 2021 11:06:28 AM UTC',
                value: (<React.Fragment>
                    <DateTime date={endTimestamp * 1000}/>
                    {" (" + endTimestamp + ")"}
                  </React.Fragment>),
            })}
            </Row>
            <Row title="Duration">{durationString}</Row>
            <Row title="Operation">{transaction['transaction.op'] || ''}</Row>
            {this.renderMeasurements()}
            <Tags location={location} organization={organization} transaction={transaction}/>
          </tbody>
        </table>
      </TransactionDetails>);
    };
    TransactionDetail.prototype.render = function () {
        return (<TransactionDetailsContainer onClick={function (event) {
                // prevent toggling the transaction detail
                event.stopPropagation();
            }}>
        {this.renderTransactionErrors()}
        {this.renderTransactionDetail()}
      </TransactionDetailsContainer>);
    };
    return TransactionDetail;
}(React.Component));
var StyledButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space(0.75), space(0.5));
var Toggle = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  font-weight: bold;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; });
export default TransactionDetail;
var templateObject_1, templateObject_2;
//# sourceMappingURL=transactionDetail.jsx.map