import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LineChart from 'app/components/charts/lineChart';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getSeriesSelection } from 'app/components/charts/utils';
import LoadingIndicator from 'app/components/loadingIndicator';
import Placeholder from 'app/components/placeholder';
import { IconWarning } from 'app/icons';
import getDynamicText from 'app/utils/getDynamicText';
import { sessionTerm } from 'app/views/releases/utils/sessionTerm';
function Chart(_a) {
    var timeseriesResults = _a.series, location = _a.location, errored = _a.errored, isLoading = _a.isLoading, selection = _a.selection, router = _a.router, theme = _a.theme, platform = _a.platform;
    var datetime = selection.datetime;
    var utc = datetime.utc, period = datetime.period, start = datetime.start, end = datetime.end;
    var filteredTimeseriesResults = timeseriesResults.filter(function (_a) {
        var seriesName = _a.seriesName;
        // There is no concept of Abnormal sessions in javascript
        if ((seriesName === sessionTerm.abnormal || seriesName === sessionTerm.otherAbnormal) &&
            platform &&
            ['javascript', 'node'].includes(platform)) {
            return false;
        }
        return true;
    });
    var legend = {
        right: 10,
        top: 0,
        selected: getSeriesSelection(location),
    };
    var colors = timeseriesResults
        ? theme.charts.getColorPalette(timeseriesResults.length - 2)
        : [];
    // Create a list of series based on the order of the fields,
    var series = filteredTimeseriesResults
        ? filteredTimeseriesResults.map(function (values, index) { return (__assign(__assign({}, values), { color: colors[index] })); })
        : [];
    return (<ChartZoom router={router} period={period} utc={utc} start={start} end={end}>
      {function (zoomRenderProps) {
            if (errored) {
                return (<ErrorPanel>
              <IconWarning color="gray300" size="lg"/>
            </ErrorPanel>);
            }
            return (<TransitionChart loading={isLoading} reloading={isLoading}>
            <LoadingScreen loading={isLoading}/>
            {getDynamicText({
                    value: (<LineChart {...zoomRenderProps} legend={legend} series={series} grid={{
                            left: '0px',
                            right: '10px',
                            top: '30px',
                            bottom: '0px',
                        }}/>),
                    fixed: <Placeholder height="200px" testId="skeleton-ui"/>,
                })}
          </TransitionChart>);
        }}
    </ChartZoom>);
}
export default withTheme(Chart);
var LoadingScreen = function (_a) {
    var loading = _a.loading;
    if (!loading) {
        return null;
    }
    return (<StyledTransparentLoadingMask visible={loading}>
      <LoadingIndicator mini/>
    </StyledTransparentLoadingMask>);
};
var StyledTransparentLoadingMask = styled(function (props) { return (<TransparentLoadingMask {...props} maskBackgroundColor="transparent"/>); })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"])));
var templateObject_1;
//# sourceMappingURL=chart.jsx.map