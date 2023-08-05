import React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
export function getRequestFunction(_props) {
    var aggregateColumn = _props.aggregateColumn;
    function getTagExplorerRequestPayload(props) {
        var eventView = props.eventView;
        var apiPayload = eventView.getEventsAPIPayload(props.location);
        apiPayload.aggregateColumn = aggregateColumn;
        return apiPayload;
    }
    return getTagExplorerRequestPayload;
}
function shouldRefetchData(prevProps, nextProps) {
    return prevProps.aggregateColumn !== nextProps.aggregateColumn;
}
function afterFetch(data) {
    var newData = data;
    return newData.map(function (row) {
        var firstItem = row.topValues[0];
        row.tagValue = firstItem;
        row.aggregate = firstItem.aggregate;
        row.frequency = firstItem.count;
        row.comparison = firstItem.comparison;
        row.totalTimeLost = firstItem.sumdelta;
        return row;
    });
}
function SegmentExplorerQuery(props) {
    return (<GenericDiscoverQuery route="events-facets-performance" getRequestPayload={getRequestFunction(props)} shouldRefetchData={shouldRefetchData} afterFetch={afterFetch} {...props}/>);
}
export default withApi(SegmentExplorerQuery);
//# sourceMappingURL=segmentExplorerQuery.jsx.map