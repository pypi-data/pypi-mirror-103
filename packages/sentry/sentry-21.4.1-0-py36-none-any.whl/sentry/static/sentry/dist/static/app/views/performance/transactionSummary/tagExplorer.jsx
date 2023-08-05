import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import GridEditable from 'app/components/gridEditable';
import Link from 'app/components/links/link';
import Pagination from 'app/components/pagination';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { formatPercentage } from 'app/utils/formatters';
import SegmentExplorerQuery from 'app/utils/performance/segmentExplorer/segmentExplorerQuery';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import { PerformanceDuration } from '../utils';
var COLUMN_ORDER = [
    {
        key: 'key',
        name: 'Key',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'tagValue',
        name: 'Tag Values',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'aggregate',
        name: 'Avg Duration',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'frequency',
        name: 'Frequency',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'comparison',
        name: 'Comparison To Avg',
        width: -1,
        column: {
            kind: 'field',
        },
    },
    {
        key: 'totalTimeLost',
        name: 'Total Time Lost',
        width: -1,
        column: {
            kind: 'field',
        },
    },
];
var DURATION_OPTIONS = [
    {
        label: 'transaction.duration',
        value: 'duration',
    },
    {
        label: 'measurements.lcp',
        value: 'measurements[lcp]',
    },
    {
        label: 'spans.browser',
        value: 'span_op_breakdowns[ops.browser]',
    },
    {
        label: 'spans.db',
        value: 'span_op_breakdowns[ops.db]',
    },
    {
        label: 'spans.http',
        value: 'span_op_breakdowns[ops.http]',
    },
    {
        label: 'spans.resource',
        value: 'span_op_breakdowns[ops.resource]',
    },
];
var handleTagValueClick = function (location, tagKey, tagValue) {
    var queryString = decodeScalar(location.query.query);
    var conditions = tokenizeSearch(queryString || '');
    conditions.addTagValues(tagKey, [tagValue]);
    var query = stringifyQueryObject(conditions);
    browserHistory.push({
        pathname: location.pathname,
        query: __assign(__assign({}, location.query), { query: String(query).trim() }),
    });
};
var renderBodyCell = function (parentProps, column, dataRow) {
    var value = dataRow[column.key];
    var location = parentProps.location;
    if (column.key === 'tagValue') {
        var localValue_1 = dataRow.tagValue;
        return (<Link to="" onClick={function () { return handleTagValueClick(location, dataRow.key, localValue_1.value); }}>
        <TagValue value={localValue_1}/>
      </Link>);
    }
    if (column.key === 'frequency') {
        var localValue = dataRow.frequency;
        return formatPercentage(localValue, 0);
    }
    if (column.key === 'comparison') {
        var localValue = dataRow.comparison;
        var text = '';
        if (localValue > 1) {
            var pct = formatPercentage(localValue - 1, 0);
            text = "+" + pct + " slower";
        }
        else {
            var pct = formatPercentage(localValue - 1, 0);
            text = pct + " faster";
        }
        return (<Tooltip title={PerformanceDuration({ milliseconds: dataRow.aggregate })}>
        {t(text)}
      </Tooltip>);
    }
    if (column.key === 'aggregate') {
        return <PerformanceDuration abbreviation milliseconds={dataRow.aggregate}/>;
    }
    if (column.key === 'totalTimeLost') {
        return <PerformanceDuration abbreviation milliseconds={dataRow.totalTimeLost}/>;
    }
    return value;
};
var renderBodyCellWithData = function (parentProps) {
    return function (column, dataRow) { return renderBodyCell(parentProps, column, dataRow); };
};
function TagValue(props) {
    var value = props.value;
    return <div>{value.name}</div>;
}
var _TagExplorer = /** @class */ (function (_super) {
    __extends(_TagExplorer, _super);
    function _TagExplorer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            aggregateColumn: DURATION_OPTIONS[0].value,
        };
        return _this;
    }
    _TagExplorer.prototype.setAggregateColumn = function (value) {
        this.setState({
            aggregateColumn: value,
        });
    };
    _TagExplorer.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location;
        var aggregateColumn = this.state.aggregateColumn;
        var handleCursor = function () { };
        var columnDropdownOptions = DURATION_OPTIONS;
        var selectedColumn = columnDropdownOptions.find(function (o) { return o.value === aggregateColumn; }) ||
            columnDropdownOptions[0];
        return (<SegmentExplorerQuery eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} limit={5}>
        {function (_a) {
                var isLoading = _a.isLoading, tableData = _a.tableData, pageLinks = _a.pageLinks;
                return (<React.Fragment>
              <TagsHeader selectedColumn={selectedColumn} columnOptions={columnDropdownOptions} handleColumnDropdownChange={function (v) { return _this.setAggregateColumn(v); }}/>
              <GridEditable isLoading={isLoading} data={tableData ? tableData : []} columnOrder={COLUMN_ORDER} columnSortBy={[]} grid={{
                        renderBodyCell: renderBodyCellWithData(_this.props),
                    }} location={location}/>
              <StyledPagination pageLinks={pageLinks} onCursor={handleCursor} size="small"/>
            </React.Fragment>);
            }}
      </SegmentExplorerQuery>);
    };
    return _TagExplorer;
}(React.Component));
function TagsHeader(props) {
    var selectedColumn = props.selectedColumn, columnOptions = props.columnOptions, handleColumnDropdownChange = props.handleColumnDropdownChange;
    return (<Header>
      <SectionHeading>{t('Suspect Tags')}</SectionHeading>
      <DropdownControl data-test-id="tag-column-performance" button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} prefix={t('Column')} size="small">
            {selectedColumn.label}
          </StyledDropdownButton>);
        }}>
        {columnOptions.map(function (_a) {
            var value = _a.value, label = _a.label;
            return (<DropdownItem data-test-id={"option-" + value} key={value} onSelect={handleColumnDropdownChange} eventKey={value} isActive={value === selectedColumn.value}>
            {label}
          </DropdownItem>);
        })}
      </DropdownControl>
    </Header>);
}
export var SectionHeading = styled('h4')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  margin: ", " 0;\n  line-height: 1.3;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  margin: ", " 0;\n  line-height: 1.3;\n"])), space(1), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space(1));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"])), space(1));
var StyledDropdownButton = styled(DropdownButton)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  min-width: 145px;\n"], ["\n  min-width: 145px;\n"])));
var StyledPagination = styled(Pagination)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0 0 ", " 0;\n"], ["\n  margin: 0 0 ", " 0;\n"])), space(3));
export var TagExplorer = _TagExplorer;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=tagExplorer.jsx.map