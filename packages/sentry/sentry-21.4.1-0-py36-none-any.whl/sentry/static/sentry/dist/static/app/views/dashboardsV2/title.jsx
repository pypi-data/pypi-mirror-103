import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import EditableText from 'app/components/editableText';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
function DashboardTitle(_a) {
    var dashboard = _a.dashboard, isEditing = _a.isEditing, onUpdate = _a.onUpdate;
    return (<Container>
      {!dashboard ? (t('Dashboards')) : (<StyledEditableText isDisabled={!isEditing} value={dashboard.title} onChange={function (newTitle) { return onUpdate(__assign(__assign({}, dashboard), { title: newTitle })); }} errorMessage={t('Please set a title for this dashboard')} successMessage={t('Dashboard title updated successfully')}/>)}
    </Container>);
}
export default DashboardTitle;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  margin-right: ", ";\n  margin-left: -11px;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  ", ";\n  margin-right: ", ";\n  margin-left: -11px;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), overflowEllipsis, space(1), function (p) { return p.theme.breakpoints[2]; }, space(2));
var StyledEditableText = styled(EditableText)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  width: calc(100% + 11px);\n"], ["\n  position: absolute;\n  width: calc(100% + 11px);\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=title.jsx.map