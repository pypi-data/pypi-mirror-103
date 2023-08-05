export function getBreakdownChartData(_a) {
    var response = _a.response, legend = _a.legend, groupBy = _a.groupBy;
    return response.groups.reduce(function (groups, group, index) {
        var key = groupBy ? group.by[groupBy] : index;
        groups[key] = {
            seriesName: legend,
            data: [],
        };
        return groups;
    }, {});
}
//# sourceMappingURL=utils.jsx.map