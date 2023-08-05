import { __makeTemplateObject } from "tslib";
import React from 'react';
import { ClassNames } from '@emotion/core';
import memoize from 'lodash/memoize';
import SmartSearchBar from 'app/components/smartSearchBar';
import { NEGATION_OPERATOR, SEARCH_WILDCARD } from 'app/constants';
import { t } from 'app/locale';
var SEARCH_SPECIAL_CHARS_REGEXP = new RegExp("^" + NEGATION_OPERATOR + "|\\" + SEARCH_WILDCARD, 'g');
function SearchBar(_a) {
    var api = _a.api, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, metricName = _a.metricName, tags = _a.tags, onChange = _a.onChange, onBlur = _a.onBlur;
    /**
     * Prepare query string (e.g. strip special characters like negation operator)
     */
    function prepareQuery(query) {
        return query.replace(SEARCH_SPECIAL_CHARS_REGEXP, '');
    }
    function fetchTagValues(tagKey) {
        return api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/metrics/tags/" + metricName + "/" + tagKey + "/", {
            method: 'GET',
        });
    }
    function getTagValues(tag, _query) {
        return fetchTagValues(tag.key).then(function (tagValues) { return tagValues; }, function () {
            throw new Error('Unable to fetch tag values');
        });
    }
    var supportedTags = tags.reduce(function (acc, tag) {
        acc[tag] = { key: tag, name: tag };
        return acc;
    }, {});
    return (<ClassNames>
      {function (_a) {
            var css = _a.css;
            return (<SmartSearchBar placeholder={t('Search for tag')} onGetTagValues={memoize(getTagValues, function (_a, query) {
                var key = _a.key;
                return key + "-" + query;
            })} supportedTags={supportedTags} prepareQuery={prepareQuery} onChange={onChange} onBlur={onBlur} useFormWrapper={false} excludeEnvironment dropdownClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n            max-height: 300px;\n            overflow-y: auto;\n          "], ["\n            max-height: 300px;\n            overflow-y: auto;\n          "])))}/>);
        }}
    </ClassNames>);
}
export default SearchBar;
var templateObject_1;
//# sourceMappingURL=searchBar.jsx.map