import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Input from 'app/views/settings/components/forms/controls/input';
import SelectField from 'app/views/settings/components/forms/selectField';
import SearchBar from './searchBar';
function Queries(_a) {
    var _b, _c;
    var api = _a.api, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, metrics = _a.metrics, queries = _a.queries, onRemoveQuery = _a.onRemoveQuery, onAddQuery = _a.onAddQuery, onChangeQuery = _a.onChangeQuery, metric = _a.metric;
    function handleFieldChange(queryIndex, field) {
        var widgetQuery = queries[queryIndex];
        return function handleChange(value) {
            var _a;
            var newQuery = __assign(__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
            onChangeQuery(queryIndex, newQuery);
        };
    }
    var aggregations = metric
        ? (_c = (_b = metrics.find(function (m) { return m.name === metric.name; })) === null || _b === void 0 ? void 0 : _b.operations) !== null && _c !== void 0 ? _c : []
        : [];
    return (<Wrapper>
      {queries.map(function (query, queryIndex) {
            var _a, _b, _c;
            return (<Fields displayDeleteButton={queries.length > 1} key={queryIndex}>
            <SearchBar api={api} metricName={(_a = metric === null || metric === void 0 ? void 0 : metric.name) !== null && _a !== void 0 ? _a : ''} tags={(_b = metric === null || metric === void 0 ? void 0 : metric.tags) !== null && _b !== void 0 ? _b : []} orgSlug={orgSlug} projectSlug={projectSlug} query={query.tags} onBlur={function (value) { return handleFieldChange(queryIndex, 'tags')(value); }}/>
            <StyledSelectField name="groupBy" placeholder={t('Select Group By')} choices={((_c = metric === null || metric === void 0 ? void 0 : metric.tags) !== null && _c !== void 0 ? _c : []).map(function (tag) { return [tag, tag]; })} value={query.groupBy[0]} onChange={function (value) {
                    return handleFieldChange(queryIndex, 'groupBy')(value ? [value] : []);
                }} inline={false} allowClear={false} flexibleControlStateSize stacked/>
            <StyledSelectField name="aggregation" placeholder={t('Select Aggregation')} choices={aggregations.map(function (aggregation) { return [aggregation, aggregation]; })} value={query.aggregation} onChange={function (value) { return handleFieldChange(queryIndex, 'aggregation')(value); }} inline={false} allowClear={false} flexibleControlStateSize stacked/>
            <Input type="text" name="legend" value={query.legend} placeholder={t('Legend Alias')} onChange={function (event) {
                    return handleFieldChange(queryIndex, 'legend')(event.target.value);
                }} required/>
            {queries.length > 1 && (<React.Fragment>
                <ButtonDeleteWrapper>
                  <Button onClick={function () {
                        onRemoveQuery(queryIndex);
                    }} size="small">
                    {t('Delete Query')}
                  </Button>
                </ButtonDeleteWrapper>
                <IconDeleteWrapper onClick={function () {
                        onRemoveQuery(queryIndex);
                    }}>
                  <IconDelete aria-label={t('Delete Query')}/>
                </IconDeleteWrapper>
              </React.Fragment>)}
          </Fields>);
        })}
      <div>
        <Button size="small" icon={<IconAdd isCircled/>} onClick={onAddQuery}>
          {t('Add Query')}
        </Button>
      </div>
    </Wrapper>);
}
export default Queries;
var IconDeleteWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 40px;\n  cursor: pointer;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n  }\n"], ["\n  height: 40px;\n  cursor: pointer;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var Fields = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: ", ";\n    grid-gap: ", ";\n    align-items: center;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: ",
    ";\n    grid-gap: ", ";\n    align-items: center;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; }, function (p) {
    return p.displayDeleteButton
        ? '1fr 0.5fr 0.5fr 0.5fr max-content'
        : '1fr 0.5fr 0.5fr 0.5fr';
}, space(1));
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    ", " {\n      :not(:first-child) {\n        border-top: 1px solid ", ";\n        padding-top: ", ";\n      }\n    }\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    ", " {\n      :not(:first-child) {\n        border-top: 1px solid ", ";\n        padding-top: ", ";\n      }\n    }\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; }, Fields, function (p) { return p.theme.border; }, space(2));
var StyledSelectField = styled(SelectField)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding-right: 0;\n  padding-bottom: 0;\n"], ["\n  padding-right: 0;\n  padding-bottom: 0;\n"])));
var ButtonDeleteWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=queries.jsx.map